import base64
import json
import logging
from io import BytesIO

import qrcode
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import CustomerCall
from .whatsapp_bot import send_whatsapp_message

logger = logging.getLogger(__name__)


# ── Helpers ────────────────────────────────────────────────────────────────────

def _qr_base64(url: str) -> str:
    img = qrcode.make(url)
    buf = BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode()


def _bot_number() -> str:
    return getattr(settings, 'WHATSAPP_BOT_NUMBER', '994XXXXXXXXX')


def _whatsapp_url(token: str) -> str:
    number = _bot_number()
    text = f'Sifariş kodim: {token}'
    return f'https://wa.me/{number}?text={text}'


# ── Service Worker (must be served at /sw.js — root level) ────────────────────

def service_worker_view(request):
    js = """
self.addEventListener('push', function(event) {
    const data = event.data ? event.data.json() : {};
    const title = data.title || 'Bildiriş';
    const options = {
        body: data.body || 'Sifarişiniz hazırdır!',
        requireInteraction: true,
        vibrate: [200, 100, 200],
    };
    event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    event.waitUntil(clients.openWindow('/'));
});
""".strip()
    return HttpResponse(js, content_type='application/javascript')


# ── Cashier ────────────────────────────────────────────────────────────────────

@login_required
def generate_view(request):
    call = None
    qr_b64 = None
    wait_url = None
    wa_url = None

    if request.method == 'POST':
        # Ensure uniqueness (extremely unlikely collision but safe)
        token = CustomerCall._meta.get_field('token').default()
        while CustomerCall.objects.filter(token=token).exists():
            token = CustomerCall._meta.get_field('token').default()

        call = CustomerCall.objects.create(token=token)

        scheme = 'https' if request.is_secure() else 'http'
        wait_url = f"{scheme}://{request.get_host()}/customer/wait/{token}/"
        wa_url = _whatsapp_url(token)
        qr_b64 = _qr_base64(wait_url)

    return render(request, 'calls/generate.html', {
        'call': call,
        'wait_url': wait_url,
        'wa_url': wa_url,
        'qr_b64': qr_b64,
    })


# ── Customer ───────────────────────────────────────────────────────────────────

def wait_view(request, token):
    call = get_object_or_404(CustomerCall, token=token)
    return render(request, 'calls/wait.html', {
        'call': call,
        'wa_url': _whatsapp_url(token),
        'vapid_public_key': getattr(settings, 'VAPID_PUBLIC_KEY', ''),
        'subscribe_url': f'/customer/subscribe/{token}/',
    })


@csrf_exempt
@require_POST
def subscribe_view(request, token):
    """Store WebPush subscription JSON sent from wait.html."""
    call = get_object_or_404(CustomerCall, token=token)
    try:
        data = json.loads(request.body)
        call.push_subscription = data
        call.notification_type = 'webpush'
        call.save()
        return JsonResponse({'ok': True})
    except Exception as exc:
        logger.exception('subscribe_view error for token %s', token)
        return JsonResponse({'ok': False, 'error': str(exc)}, status=400)


# ── Barman dashboard ───────────────────────────────────────────────────────────

@login_required
def dashboard_view(request):
    calls = CustomerCall.objects.filter(
        status__in=['waiting', 'called']
    ).order_by('-created_at')
    return render(request, 'calls/dashboard.html', {'calls': calls})


@login_required
def dashboard_data_view(request):
    """Polling endpoint — returns active calls as JSON every 5 s."""
    calls = (
        CustomerCall.objects
        .filter(status__in=['waiting', 'called'])
        .order_by('-created_at')
        .values('id', 'token', 'name', 'notification_type',
                'whatsapp_number', 'status', 'created_at')
    )
    rows = []
    for c in calls:
        rows.append({
            'id': c['id'],
            'token': c['token'],
            'name': c['name'],
            'notification_type': c['notification_type'],
            'whatsapp_number': c['whatsapp_number'],
            'status': c['status'],
            'created_at': c['created_at'].strftime('%H:%M:%S'),
        })
    return JsonResponse({'calls': rows})


@login_required
@require_POST
def update_name_view(request, token):
    call = get_object_or_404(CustomerCall, token=token)
    try:
        data = json.loads(request.body)
        call.name = data.get('name', '').strip()[:100]
        call.save()
        return JsonResponse({'ok': True})
    except Exception as exc:
        return JsonResponse({'ok': False, 'error': str(exc)}, status=400)


@login_required
@require_POST
def call_customer_view(request, token):
    """Trigger the notification for a waiting customer."""
    call = get_object_or_404(CustomerCall, token=token)

    if call.status == 'done':
        return JsonResponse({'ok': False, 'error': 'Already done'})

    ok = False
    if call.notification_type == 'webpush' and call.push_subscription:
        ok = _send_push(call)
    elif call.notification_type == 'whatsapp' and call.whatsapp_number:
        msg = 'Sifarişiniz hazırdır, zəhmət olmasa kassaya yaxınlaşın.'
        ok = send_whatsapp_message(call.whatsapp_number, msg)
    else:
        return JsonResponse({'ok': False, 'error': 'No notification method set'})

    if ok:
        call.status = 'called'
        call.save()

    return JsonResponse({'ok': ok})


@login_required
@require_POST
def mark_done_view(request, token):
    call = get_object_or_404(CustomerCall, token=token)
    call.status = 'done'
    call.save()
    return JsonResponse({'ok': True})


# ── Push helper ────────────────────────────────────────────────────────────────

def _send_push(call: CustomerCall) -> bool:
    try:
        from pathlib import Path
        from pywebpush import webpush

        # pywebpush checks os.path.isfile() — pass the absolute path so it
        # calls Vapid.from_file() which correctly handles PEM format.
        key_path = str(Path(settings.BASE_DIR) / settings.VAPID_PRIVATE_KEY)

        webpush(
            subscription_info=call.push_subscription,
            data=json.dumps({
                'title': 'Sifarişiniz hazırdır!',
                'body': 'Zəhmət olmasa kassaya yaxınlaşın.',
            }),
            vapid_private_key=key_path,
            vapid_claims={'sub': f'mailto:{settings.VAPID_ADMIN_EMAIL}'},
        )
        return True
    except Exception:
        logger.exception('Push notification failed for %s', call.token)
        return False
