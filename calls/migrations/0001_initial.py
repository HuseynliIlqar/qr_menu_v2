import calls.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='CustomerCall',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'token',
                    models.CharField(
                        default=calls.models._generate_token,
                        max_length=20,
                        unique=True,
                    ),
                ),
                ('name', models.CharField(blank=True, max_length=100)),
                (
                    'notification_type',
                    models.CharField(
                        choices=[
                            ('webpush', 'WebPush'),
                            ('whatsapp', 'WhatsApp'),
                            ('unknown', 'Unknown'),
                        ],
                        default='unknown',
                        max_length=10,
                    ),
                ),
                ('push_subscription', models.JSONField(blank=True, null=True)),
                ('whatsapp_number', models.CharField(blank=True, max_length=20)),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('waiting', 'Waiting'),
                            ('called', 'Called'),
                            ('done', 'Done'),
                        ],
                        default='waiting',
                        max_length=10,
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
