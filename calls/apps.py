import logging
import os
import sys
import threading

from django.apps import AppConfig

logger = logging.getLogger(__name__)

_bot_started = False
_start_lock = threading.Lock()

# Management commands that should NOT start the Selenium bot
_SKIP_COMMANDS = {
    'makemigrations', 'migrate', 'migrate_schemas',
    'collectstatic', 'shell', 'shell_plus', 'test',
    'createsuperuser', 'create_tenant', 'create_test_data',
    'compile_translations', 'check',
}


class CallsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calls'
    verbose_name = 'Customer Calls'

    def ready(self):
        global _bot_started

        # Skip during management commands that don't need the bot
        if any(cmd in sys.argv for cmd in _SKIP_COMMANDS):
            return

        # Django's dev server spawns two processes; only start in the child
        # (RUN_MAIN=true). In production (gunicorn etc.) RUN_MAIN is unset
        # so we start unconditionally there.
        if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') != 'true':
            return

        with _start_lock:
            if _bot_started:
                return
            _bot_started = True

        self._start_bot()

    def _start_bot(self):
        from django.conf import settings

        if not getattr(settings, 'WHATSAPP_BOT_ENABLED', False):
            logger.info(
                'WhatsApp bot disabled (WHATSAPP_BOT_ENABLED=False in settings)'
            )
            return

        try:
            from pathlib import Path
            from .whatsapp_bot import start_bot

            profile_dir = str(Path(settings.BASE_DIR) / 'selenium_profile')
            start_bot(profile_dir)
        except ImportError as exc:
            logger.warning(
                'WhatsApp bot not started — selenium not installed? %s', exc
            )
        except Exception:
            logger.exception('Failed to start WhatsApp bot')
