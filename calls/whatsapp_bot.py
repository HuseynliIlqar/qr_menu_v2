"""
WhatsApp Web Selenium bot.

Runs as a daemon thread when Django starts. Keeps a persistent Chrome profile
so the WhatsApp QR scan is only done once. Polls for incoming messages every 3 s,
extracts customer tokens, and can send outgoing messages on demand.

CSS SELECTOR NOTE: WhatsApp Web updates its DOM periodically. If the bot stops
detecting messages, the selectors below (prefixed with SEL_) may need updating.
Last verified: March 2026.
"""

import logging
import re
import threading
import time
import urllib.parse
from pathlib import Path

logger = logging.getLogger('calls.whatsapp_bot')

# ── Singleton ─────────────────────────────────────────────────────────────────
_bot: 'WhatsAppBot | None' = None
_started = False
_start_lock = threading.Lock()


def start_bot(profile_dir: str) -> None:
    """Start the singleton WhatsApp bot in a background thread (idempotent)."""
    global _bot, _started
    with _start_lock:
        if _started:
            return
        _started = True
        _bot = WhatsAppBot(profile_dir)
        _bot.start()


def send_whatsapp_message(phone: str, message: str) -> bool:
    """Send a WhatsApp message. Returns False if bot is not running."""
    if _bot is None or not _bot.running:
        logger.warning('WhatsApp bot is not running — cannot send message')
        return False
    _bot.send_message(phone, message)
    return True


# ── CSS Selectors ──────────────────────────────────────────────────────────────
SEL_CHAT_LIST = '[data-testid="chat-list"]'
SEL_UNREAD_BADGE = 'span[data-testid="icon-unread-count"]'
SEL_CELL_CONTAINER = '[data-testid="cell-frame-container"]'
SEL_MSG_IN = 'div.message-in'
SEL_MSG_TEXT = 'span.selectable-text.copyable-text'
SEL_COMPOSE_BOX = '[data-testid="conversation-compose-box-input"]'
SEL_CHAT_TITLE = '[data-testid="conversation-info-header-chat-title"] span'


class WhatsAppBot:
    def __init__(self, profile_dir: str):
        self.profile_dir = str(Path(profile_dir).resolve())
        self.driver = None
        self.running = False
        self._send_lock = threading.Lock()
        self._processed: set[str] = set()

    # ── Lifecycle ──────────────────────────────────────────────────────────────

    def start(self) -> None:
        t = threading.Thread(target=self._run, name='WhatsAppBot', daemon=True)
        t.start()
        logger.info('WhatsApp bot thread started')

    def _run(self) -> None:
        from django.db import close_old_connections

        self.running = True
        try:
            self._init_driver()
            self._open_whatsapp()
            self._wait_for_ready()
            logger.info('WhatsApp Web ready — polling for messages')
            self._poll_loop()
        except Exception:
            logger.exception('WhatsApp bot crashed')
        finally:
            self.running = False
            close_old_connections()
            if self.driver:
                try:
                    self.driver.quit()
                except Exception:
                    pass

    # ── Driver setup ───────────────────────────────────────────────────────────

    def _init_driver(self) -> None:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        Path(self.profile_dir).mkdir(parents=True, exist_ok=True)

        opts = Options()
        opts.add_argument(f'--user-data-dir={self.profile_dir}')
        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-dev-shm-usage')
        opts.add_argument('--disable-gpu')
        opts.add_argument('--window-size=1366,768')
        # NOTE: Do NOT add --headless — WhatsApp Web blocks headless sessions.

        self.driver = webdriver.Chrome(options=opts)
        logger.info('Chrome started, profile: %s', self.profile_dir)

    def _open_whatsapp(self) -> None:
        self.driver.get('https://web.whatsapp.com')

    def _wait_for_ready(self, timeout: int = 120) -> None:
        """Block until chat list appears (user may need to scan QR first)."""
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait

        logger.info('Waiting for WhatsApp Web (scan QR if prompted) …')
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, SEL_CHAT_LIST))
        )
        logger.info('WhatsApp Web authenticated ✓')

    # ── Polling ────────────────────────────────────────────────────────────────

    def _poll_loop(self) -> None:
        while self.running:
            try:
                self._check_unread()
            except Exception as exc:
                logger.warning('Polling error: %s', exc)
            time.sleep(3)

    def _check_unread(self) -> None:
        from selenium.webdriver.common.by import By

        badges = self.driver.find_elements(By.CSS_SELECTOR, SEL_UNREAD_BADGE)
        for badge in badges:
            try:
                # Walk up to the conversation row and click it
                convo = badge.find_element(
                    By.XPATH,
                    f'./ancestor::*[@data-testid="cell-frame-container"]',
                )
                convo.click()
                time.sleep(1.5)
                self._read_open_chat()
            except Exception as exc:
                logger.debug('Error clicking conversation: %s', exc)

    def _read_open_chat(self) -> None:
        from selenium.webdriver.common.by import By

        messages = self.driver.find_elements(By.CSS_SELECTOR, SEL_MSG_IN)
        for msg in messages[-5:]:  # only check the last 5 incoming messages
            try:
                msg_id = msg.get_attribute('data-id') or ''
                if not msg_id or msg_id in self._processed:
                    continue
                self._processed.add(msg_id)

                spans = msg.find_elements(By.CSS_SELECTOR, SEL_MSG_TEXT)
                text = ' '.join(s.text for s in spans).strip()
                if not text:
                    continue

                match = re.search(
                    r'Sifari[şs]\s+kodim[:\s]+([A-Z0-9]+)', text, re.IGNORECASE
                )
                if match:
                    token = match.group(1).upper()
                    phone = self._get_open_chat_phone()
                    logger.info('Token detected: %s  phone: %s', token, phone)
                    self._handle_token(token, phone)

            except Exception as exc:
                logger.debug('Error reading message: %s', exc)

    def _get_open_chat_phone(self) -> str:
        """Best-effort extraction of the sender's phone number."""
        from selenium.webdriver.common.by import By

        # 1. Try URL query param (?phone=...)
        url = self.driver.current_url
        m = re.search(r'[?&]phone=(\d+)', url)
        if m:
            return m.group(1)

        # 2. Try chat header title (often a phone number for unknown contacts)
        try:
            header = self.driver.find_element(By.CSS_SELECTOR, SEL_CHAT_TITLE)
            digits = re.sub(r'\D', '', header.text.strip())
            if len(digits) >= 10:
                return digits
        except Exception:
            pass

        return ''

    def _handle_token(self, token: str, phone: str) -> None:
        """Find CustomerCall across all tenant schemas and mark it as whatsapp."""
        from django.db import close_old_connections
        from django_tenants.utils import get_tenant_model, schema_context

        close_old_connections()
        try:
            TenantModel = get_tenant_model()
            for tenant in TenantModel.objects.all():
                with schema_context(tenant.schema_name):
                    from calls.models import CustomerCall

                    try:
                        call = CustomerCall.objects.get(token=token)
                        if call.notification_type == 'unknown':
                            call.notification_type = 'whatsapp'
                        call.whatsapp_number = phone
                        call.save()
                        logger.info(
                            'CustomerCall %s updated (schema=%s)',
                            token,
                            tenant.schema_name,
                        )
                        return
                    except CustomerCall.DoesNotExist:
                        continue
        except Exception:
            logger.exception('Error handling token %s', token)
        finally:
            close_old_connections()

    # ── Sending ────────────────────────────────────────────────────────────────

    def send_message(self, phone: str, message: str) -> None:
        """Send a WhatsApp message. Blocks until sent. Thread-safe."""
        with self._send_lock:
            try:
                self._do_send(phone, message)
            except Exception:
                logger.exception('Failed to send WhatsApp to %s', phone)

    def _do_send(self, phone: str, message: str) -> None:
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait

        phone_clean = re.sub(r'\D', '', phone)
        encoded = urllib.parse.quote(message)
        self.driver.get(
            f'https://web.whatsapp.com/send?phone={phone_clean}&text={encoded}'
        )

        wait = WebDriverWait(self.driver, 30)
        box = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, SEL_COMPOSE_BOX))
        )
        time.sleep(2)  # let the page settle
        box.send_keys(Keys.ENTER)
        time.sleep(1)
        logger.info('Message sent to %s', phone_clean)
