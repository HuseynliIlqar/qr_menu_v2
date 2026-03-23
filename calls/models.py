import secrets
from django.db import models


def _generate_token():
    """Generate a unique 12-char uppercase token."""
    return secrets.token_urlsafe(9).upper()[:12]


class CustomerCall(models.Model):
    NOTIFICATION_CHOICES = [
        ('webpush', 'WebPush'),
        ('whatsapp', 'WhatsApp'),
        ('unknown', 'Unknown'),
    ]
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('called', 'Called'),
        ('done', 'Done'),
    ]

    token = models.CharField(max_length=20, unique=True, default=_generate_token)
    name = models.CharField(max_length=100, blank=True)
    notification_type = models.CharField(
        max_length=10, choices=NOTIFICATION_CHOICES, default='unknown'
    )
    push_subscription = models.JSONField(null=True, blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='waiting'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Call {self.token} [{self.status}]"
