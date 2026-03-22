from django.db import models
from django.conf import settings
from django_tenants.models import TenantMixin, DomainMixin


# ─────────────────────────────────────────────────────────────
#  Landing Page (public schema, editable via Django admin)
# ─────────────────────────────────────────────────────────────

class LandingPage(models.Model):
    """Singleton – only pk=1 is ever stored."""

    # Hero
    hero_badge       = models.CharField(max_length=120, default='Free Digital QR Menu Platform')
    hero_title       = models.CharField(max_length=200, default='Your Restaurant Menu,')
    hero_title_em    = models.CharField(max_length=100, default='Instantly Digital',
                                        verbose_name='Hero title (highlighted)',
                                        help_text='Displayed on the second line in amber colour.')
    hero_subtitle    = models.TextField(default='Create a beautiful QR menu for your restaurant in minutes. '
                                                'No app needed — guests scan and browse on their phone.')
    hero_btn_primary = models.CharField(max_length=60, default='Start for Free →')
    hero_btn_secondary = models.CharField(max_length=60, default='Sign In')

    # Features section
    features_label    = models.CharField(max_length=60, default='Features')
    features_title    = models.CharField(max_length=200, default='Everything your restaurant needs')
    features_subtitle = models.TextField(default='A fully-featured digital menu platform with a powerful management dashboard.')

    # How it works section
    steps_label    = models.CharField(max_length=60, default='How it works')
    steps_title    = models.CharField(max_length=200, default='Up and running in 3 steps')
    steps_subtitle = models.TextField(default='No technical knowledge required.')

    # CTA section
    cta_title    = models.CharField(max_length=200, default='Ready to go digital?')
    cta_subtitle = models.TextField(default="It's free, takes minutes to set up, and your guests will love it.")
    cta_btn      = models.CharField(max_length=60, default='Create Your Menu Now →')

    # Footer
    footer_text = models.CharField(max_length=300,
                                   default='© 2026 QRMenu. Built for restaurants.')

    class Meta:
        verbose_name = 'Landing Page'
        verbose_name_plural = 'Landing Page'

    def __str__(self):
        return 'Landing Page'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        if created:
            _seed_landing_defaults(obj)
        return obj


class LandingFeature(models.Model):
    """Feature card shown in the Features section."""
    page        = models.ForeignKey(LandingPage, on_delete=models.CASCADE, related_name='features')
    icon        = models.CharField(max_length=10, default='⚡', help_text='Paste an emoji')
    title       = models.CharField(max_length=100)
    description = models.TextField()
    sort_order  = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['sort_order']
        verbose_name = 'Feature Card'

    def __str__(self):
        return self.title


class LandingStep(models.Model):
    """Step in the "How it works" section."""
    page        = models.ForeignKey(LandingPage, on_delete=models.CASCADE, related_name='steps')
    number      = models.PositiveSmallIntegerField()
    title       = models.CharField(max_length=100)
    description = models.TextField()
    sort_order  = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'number']
        verbose_name = 'How-it-works Step'

    def __str__(self):
        return f'Step {self.number}: {self.title}'


def _seed_landing_defaults(page):
    """Populate default features and steps when the singleton is first created."""
    features = [
        ('⚡', 'Instant Updates',     'Change prices, add dishes or remove items in seconds. Your menu is live the moment you save.',          0),
        ('📱', 'No App Needed',        'Guests scan your QR code and see your menu in their browser. Works on any smartphone, instantly.',      1),
        ('🗂️', 'Multi-Category Menu', 'Organise dishes into categories — Burgers, Pizza, Drinks — with a clean filterable layout.',            2),
        ('🖼️', 'Beautiful Gallery',   'Showcase your restaurant with a stunning photo gallery. Upload images or paste URLs — your choice.',    3),
        ('🔗', 'Social Media Links',  'Connect Instagram, TikTok, WhatsApp and more. Let guests follow you with a single tap.',                4),
        ('🏷️', 'Discount Prices',    'Set original and discounted prices per dish. Crossed-out prices highlight your best deals.',            5),
    ]
    for icon, title, desc, order in features:
        LandingFeature.objects.create(page=page, icon=icon, title=title, description=desc, sort_order=order)

    steps = [
        (1, 'Register',        'Create your free account and choose a subdomain. Your restaurant gets its own isolated space.',    0),
        (2, 'Build Your Menu', 'Add categories, dishes, photos and prices from your personal dashboard. Takes under 10 minutes.', 1),
        (3, 'Share the QR',    'Print your QR code and put it on tables. Guests scan → they see your live digital menu.',         2),
    ]
    for num, title, desc, order in steps:
        LandingStep.objects.create(page=page, number=num, title=title, description=desc, sort_order=order)


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)

    auto_create_schema = True

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    pass


class TenantUser(models.Model):
    """Links a Django user to their tenant (restaurant)."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tenant_profile',
    )
    tenant = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='tenant_users',
    )

    def __str__(self):
        return f'{self.user.username} → {self.tenant.schema_name}'
