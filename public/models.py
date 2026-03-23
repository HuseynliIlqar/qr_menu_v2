from django.db import models
from django.conf import settings
from django.utils.translation import get_language
from django_tenants.models import TenantMixin, DomainMixin


# ─────────────────────────────────────────────────────────────
#  Landing Page (public schema, editable via Django admin)
# ─────────────────────────────────────────────────────────────

class LandingPage(models.Model):
    """Singleton – only pk=1 is ever stored."""

    # Hero
    hero_badge       = models.CharField(max_length=120, default='Free Digital QR Menu Platform')
    hero_badge_az    = models.CharField(max_length=120, blank=True, default='')
    hero_badge_ru    = models.CharField(max_length=120, blank=True, default='')

    hero_title       = models.CharField(max_length=200, default='Your Restaurant Menu,')
    hero_title_az    = models.CharField(max_length=200, blank=True, default='')
    hero_title_ru    = models.CharField(max_length=200, blank=True, default='')

    hero_title_em    = models.CharField(max_length=100, default='Instantly Digital',
                                        verbose_name='Hero title (highlighted)',
                                        help_text='Displayed on the second line in amber colour.')
    hero_title_em_az = models.CharField(max_length=100, blank=True, default='')
    hero_title_em_ru = models.CharField(max_length=100, blank=True, default='')

    hero_subtitle    = models.TextField(default='Create a beautiful QR menu for your restaurant in minutes. '
                                                'No app needed — guests scan and browse on their phone.')
    hero_subtitle_az = models.TextField(blank=True, default='')
    hero_subtitle_ru = models.TextField(blank=True, default='')

    hero_btn_primary    = models.CharField(max_length=60, default='Start for Free →')
    hero_btn_primary_az = models.CharField(max_length=60, blank=True, default='')
    hero_btn_primary_ru = models.CharField(max_length=60, blank=True, default='')

    hero_btn_secondary    = models.CharField(max_length=60, default='Sign In')
    hero_btn_secondary_az = models.CharField(max_length=60, blank=True, default='')
    hero_btn_secondary_ru = models.CharField(max_length=60, blank=True, default='')

    # Features section
    features_label       = models.CharField(max_length=60, default='Features')
    features_label_az    = models.CharField(max_length=60, blank=True, default='')
    features_label_ru    = models.CharField(max_length=60, blank=True, default='')

    features_title       = models.CharField(max_length=200, default='Everything your restaurant needs')
    features_title_az    = models.CharField(max_length=200, blank=True, default='')
    features_title_ru    = models.CharField(max_length=200, blank=True, default='')

    features_subtitle    = models.TextField(default='A fully-featured digital menu platform with a powerful management dashboard.')
    features_subtitle_az = models.TextField(blank=True, default='')
    features_subtitle_ru = models.TextField(blank=True, default='')

    # How it works section
    steps_label       = models.CharField(max_length=60, default='How it works')
    steps_label_az    = models.CharField(max_length=60, blank=True, default='')
    steps_label_ru    = models.CharField(max_length=60, blank=True, default='')

    steps_title       = models.CharField(max_length=200, default='Up and running in 3 steps')
    steps_title_az    = models.CharField(max_length=200, blank=True, default='')
    steps_title_ru    = models.CharField(max_length=200, blank=True, default='')

    steps_subtitle    = models.TextField(default='No technical knowledge required.')
    steps_subtitle_az = models.TextField(blank=True, default='')
    steps_subtitle_ru = models.TextField(blank=True, default='')

    # CTA section
    cta_title       = models.CharField(max_length=200, default='Ready to go digital?')
    cta_title_az    = models.CharField(max_length=200, blank=True, default='')
    cta_title_ru    = models.CharField(max_length=200, blank=True, default='')

    cta_subtitle    = models.TextField(default="It's free, takes minutes to set up, and your guests will love it.")
    cta_subtitle_az = models.TextField(blank=True, default='')
    cta_subtitle_ru = models.TextField(blank=True, default='')

    cta_btn       = models.CharField(max_length=60, default='Create Your Menu Now →')
    cta_btn_az    = models.CharField(max_length=60, blank=True, default='')
    cta_btn_ru    = models.CharField(max_length=60, blank=True, default='')

    # Footer
    footer_text    = models.CharField(max_length=300, default='© 2026 QRMenu. Built for restaurants.')
    footer_text_az = models.CharField(max_length=300, blank=True, default='')
    footer_text_ru = models.CharField(max_length=300, blank=True, default='')

    def _t(self, field):
        """Return the translated value of a field, falling back to English."""
        lang = get_language()
        if lang and lang != 'en':
            val = getattr(self, f'{field}_{lang}', None)
            if val:
                return val
        return getattr(self, field, '')

    @property
    def translated_hero_badge(self):        return self._t('hero_badge')
    @property
    def translated_hero_title(self):        return self._t('hero_title')
    @property
    def translated_hero_title_em(self):     return self._t('hero_title_em')
    @property
    def translated_hero_subtitle(self):     return self._t('hero_subtitle')
    @property
    def translated_hero_btn_primary(self):  return self._t('hero_btn_primary')
    @property
    def translated_hero_btn_secondary(self): return self._t('hero_btn_secondary')
    @property
    def translated_features_label(self):    return self._t('features_label')
    @property
    def translated_features_title(self):    return self._t('features_title')
    @property
    def translated_features_subtitle(self): return self._t('features_subtitle')
    @property
    def translated_steps_label(self):       return self._t('steps_label')
    @property
    def translated_steps_title(self):       return self._t('steps_title')
    @property
    def translated_steps_subtitle(self):    return self._t('steps_subtitle')
    @property
    def translated_cta_title(self):         return self._t('cta_title')
    @property
    def translated_cta_subtitle(self):      return self._t('cta_subtitle')
    @property
    def translated_cta_btn(self):           return self._t('cta_btn')
    @property
    def translated_footer_text(self):       return self._t('footer_text')

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
    page           = models.ForeignKey(LandingPage, on_delete=models.CASCADE, related_name='features')
    icon           = models.CharField(max_length=10, default='⚡', help_text='Paste an emoji')
    title          = models.CharField(max_length=100)
    title_az       = models.CharField(max_length=100, blank=True, default='')
    title_ru       = models.CharField(max_length=100, blank=True, default='')
    description    = models.TextField()
    description_az = models.TextField(blank=True, default='')
    description_ru = models.TextField(blank=True, default='')
    sort_order     = models.PositiveSmallIntegerField(default=0)

    def _t(self, field):
        lang = get_language()
        if lang and lang != 'en':
            val = getattr(self, f'{field}_{lang}', None)
            if val:
                return val
        return getattr(self, field, '')

    @property
    def translated_title(self):       return self._t('title')
    @property
    def translated_description(self): return self._t('description')

    class Meta:
        ordering = ['sort_order']
        verbose_name = 'Feature Card'

    def __str__(self):
        return self.title


class LandingStep(models.Model):
    """Step in the "How it works" section."""
    page           = models.ForeignKey(LandingPage, on_delete=models.CASCADE, related_name='steps')
    number         = models.PositiveSmallIntegerField()
    title          = models.CharField(max_length=100)
    title_az       = models.CharField(max_length=100, blank=True, default='')
    title_ru       = models.CharField(max_length=100, blank=True, default='')
    description    = models.TextField()
    description_az = models.TextField(blank=True, default='')
    description_ru = models.TextField(blank=True, default='')
    sort_order     = models.PositiveSmallIntegerField(default=0)

    def _t(self, field):
        lang = get_language()
        if lang and lang != 'en':
            val = getattr(self, f'{field}_{lang}', None)
            if val:
                return val
        return getattr(self, field, '')

    @property
    def translated_title(self):       return self._t('title')
    @property
    def translated_description(self): return self._t('description')

    class Meta:
        ordering = ['sort_order', 'number']
        verbose_name = 'How-it-works Step'

    def __str__(self):
        return f'Step {self.number}: {self.title}'


def _seed_landing_defaults(page):
    """Populate default features, steps and AZ/RU translations when the singleton is first created."""
    page.hero_badge_az = 'Pulsuz Rəqəmsal QR Menyu Platforması'
    page.hero_badge_ru = 'Бесплатная Цифровая QR Меню Платформа'
    page.hero_title_az = 'Restoranınızın Menyusu,'
    page.hero_title_ru = 'Меню вашего ресторана,'
    page.hero_title_em_az = 'Dərhal Rəqəmsal'
    page.hero_title_em_ru = 'Мгновенно Цифровое'
    page.hero_subtitle_az = 'Dəqiqələr içərisində restoranınız üçün gözəl QR menyu yaradın. Tətbiq lazım deyil — qonaqlar skan edib telefonlarında baxır.'
    page.hero_subtitle_ru = 'Создайте красивое QR меню для вашего ресторана за несколько минут. Приложение не нужно — гости сканируют и просматривают на телефоне.'
    page.hero_btn_primary_az = 'Pulsuz Başla →'
    page.hero_btn_primary_ru = 'Начать бесплатно →'
    page.hero_btn_secondary_az = 'Daxil ol'
    page.hero_btn_secondary_ru = 'Войти'
    page.features_label_az = 'Xüsusiyyətlər'
    page.features_label_ru = 'Возможности'
    page.features_title_az = 'Restoranınızın ehtiyac duyduğu hər şey'
    page.features_title_ru = 'Всё, что нужно вашему ресторану'
    page.features_subtitle_az = 'Güclü idarəetmə paneli ilə tam funksiyalı rəqəmsal menyu platforması.'
    page.features_subtitle_ru = 'Полнофункциональная платформа цифрового меню с мощной панелью управления.'
    page.steps_label_az = 'Necə işləyir'
    page.steps_label_ru = 'Как это работает'
    page.steps_title_az = '3 addımda hazır'
    page.steps_title_ru = 'Готово за 3 шага'
    page.steps_subtitle_az = 'Texniki bilik tələb olunmur.'
    page.steps_subtitle_ru = 'Технические знания не требуются.'
    page.cta_title_az = 'Rəqəmsallaşmağa hazırsınız?'
    page.cta_title_ru = 'Готовы перейти на цифровое?'
    page.cta_subtitle_az = 'Pulsuzdur, qurulması bir neçə dəqiqə çəkir və qonaqlarınız sevinəcək.'
    page.cta_subtitle_ru = 'Это бесплатно, займёт несколько минут, и ваши гости будут в восторге.'
    page.cta_btn_az = 'İndi Menyunuzu Yaradın →'
    page.cta_btn_ru = 'Создать меню сейчас →'
    page.footer_text_az = '© 2026 QRMenu. Restoranlar üçün yaradılıb.'
    page.footer_text_ru = '© 2026 QRMenu. Создано для ресторанов.'
    page.save()

    features = [
        # (icon, title_en, title_az, title_ru, desc_en, desc_az, desc_ru, order)
        ('⚡', 'Instant Updates',
         'Anında Yeniləmə', 'Мгновенные обновления',
         'Change prices, add dishes or remove items in seconds. Your menu is live the moment you save.',
         'Qiymətləri dəyişin, yeməklər əlavə edin və ya silin — menyu dərhal yayımlanır.',
         'Изменяйте цены, добавляйте блюда — меню обновляется мгновенно.', 0),
        ('📱', 'No App Needed',
         'Tətbiq Lazım Deyil', 'Приложение не нужно',
         'Guests scan your QR code and see your menu in their browser. Works on any smartphone, instantly.',
         'Qonaqlar QR kodunuzu skan edib brauzerdə menyunu görürlər. İstənilən smartfonda işləyir.',
         'Гости сканируют QR-код и видят меню в браузере. Работает на любом смартфоне.', 1),
        ('🗂️', 'Multi-Category Menu',
         'Çox Kateqoriyalı Menyu', 'Мульти-категорийное меню',
         'Organise dishes into categories — Burgers, Pizza, Drinks — with a clean filterable layout.',
         'Yeməkləri kateqoriyalara bölün — Burgerlər, Pizza, İçkilər — süzgəcli dizaynla.',
         'Организуйте блюда по категориям — Бургеры, Пицца, Напитки — с удобной фильтрацией.', 2),
        ('🖼️', 'Beautiful Gallery',
         'Gözəl Qalerya', 'Красивая галерея',
         'Showcase your restaurant with a stunning photo gallery. Upload images or paste URLs — your choice.',
         'Restoranınızı gözəl fotolarla nümayiş etdirin. Şəkil yükləyin və ya URL əlavə edin.',
         'Покажите ваш ресторан в красивой фотогалерее. Загружайте фото или вставляйте URL.', 3),
        ('🔗', 'Social Media Links',
         'Sosial Media Bağlantıları', 'Ссылки на соцсети',
         'Connect Instagram, TikTok, WhatsApp and more. Let guests follow you with a single tap.',
         'Instagram, TikTok, WhatsApp və daha çoxunu əlavə edin. Qonaqlar tək kliklə sizi izləsin.',
         'Подключите Instagram, TikTok, WhatsApp. Гости подпишутся одним касанием.', 4),
        ('🏷️', 'Discount Prices',
         'Endirim Qiymətləri', 'Скидочные цены',
         'Set original and discounted prices per dish. Crossed-out prices highlight your best deals.',
         'Hər yemək üçün orijinal və endirimli qiymət təyin edin. Üstündən xətt çəkilmiş qiymətlər.',
         'Установите обычную и скидочную цену. Зачёркнутые цены выделяют лучшие предложения.', 5),
    ]
    for icon, title, title_az, title_ru, desc, desc_az, desc_ru, order in features:
        LandingFeature.objects.create(
            page=page, icon=icon,
            title=title, title_az=title_az, title_ru=title_ru,
            description=desc, description_az=desc_az, description_ru=desc_ru,
            sort_order=order,
        )

    steps = [
        # (num, title_en, title_az, title_ru, desc_en, desc_az, desc_ru, order)
        (1, 'Register',
         'Qeydiyyatdan keç', 'Зарегистрируйтесь',
         'Create your free account and choose a subdomain. Your restaurant gets its own isolated space.',
         'Pulsuz hesabınızı yaradın və subdomen seçin. Restoranınız öz ayrıca məkanına sahib olur.',
         'Создайте бесплатный аккаунт и выберите поддомен. Ваш ресторан получит своё пространство.', 0),
        (2, 'Build Your Menu',
         'Menyunuzu Qurun', 'Создайте меню',
         'Add categories, dishes, photos and prices from your personal dashboard. Takes under 10 minutes.',
         'Kateqoriyalar, yeməklər, fotolar və qiymətləri panelinizden əlavə edin. 10 dəqiqədən az.',
         'Добавьте категории, блюда, фото и цены в панели управления. Займёт менее 10 минут.', 1),
        (3, 'Share the QR',
         'QR Kodunu Paylaşın', 'Поделитесь QR-кодом',
         'Print your QR code and put it on tables. Guests scan → they see your live digital menu.',
         'QR kodunuzu çap edib masalara qoyun. Qonaqlar skan edir → canlı rəqəmsal menyunuzu görürlər.',
         'Распечатайте QR-код и разместите на столах. Гости сканируют → видят ваше живое меню.', 2),
    ]
    for num, title, title_az, title_ru, desc, desc_az, desc_ru, order in steps:
        LandingStep.objects.create(
            page=page, number=num,
            title=title, title_az=title_az, title_ru=title_ru,
            description=desc, description_az=desc_az, description_ru=desc_ru,
            sort_order=order,
        )


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
