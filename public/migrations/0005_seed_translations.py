"""
Data migration: populate AZ/RU translations for the existing LandingPage singleton
and its related LandingFeature / LandingStep objects.
"""
from django.db import migrations


FEATURE_TRANSLATIONS = {
    'Instant Updates': (
        'Anında Yeniləmə', 'Мгновенные обновления',
        'Qiymətləri dəyişin, yeməklər əlavə edin və ya silin — menyu dərhal yayımlanır.',
        'Изменяйте цены, добавляйте блюда — меню обновляется мгновенно.',
    ),
    'No App Needed': (
        'Tətbiq Lazım Deyil', 'Приложение не нужно',
        'Qonaqlar QR kodunuzu skan edib brauzerdə menyunu görürlər. İstənilən smartfonda işləyir.',
        'Гости сканируют QR-код и видят меню в браузере. Работает на любом смартфоне.',
    ),
    'Multi-Category Menu': (
        'Çox Kateqoriyalı Menyu', 'Мульти-категорийное меню',
        'Yeməkləri kateqoriyalara bölün — Burgerlər, Pizza, İçkilər — süzgəcli dizaynla.',
        'Организуйте блюда по категориям — Бургеры, Пицца, Напитки — с удобной фильтрацией.',
    ),
    'Beautiful Gallery': (
        'Gözəl Qalerya', 'Красивая галерея',
        'Restoranınızı gözəl fotolarla nümayiş etdirin. Şəkil yükləyin və ya URL əlavə edin.',
        'Покажите ваш ресторан в красивой фотогалерее. Загружайте фото или вставляйте URL.',
    ),
    'Social Media Links': (
        'Sosial Media Bağlantıları', 'Ссылки на соцсети',
        'Instagram, TikTok, WhatsApp və daha çoxunu əlavə edin. Qonaqlar tək kliklə sizi izləsin.',
        'Подключите Instagram, TikTok, WhatsApp. Гости подпишутся одним касанием.',
    ),
    'Discount Prices': (
        'Endirim Qiymətləri', 'Скидочные цены',
        'Hər yemək üçün orijinal və endirimli qiymət təyin edin. Üstündən xətt çəkilmiş qiymətlər.',
        'Установите обычную и скидочную цену. Зачёркнутые цены выделяют лучшие предложения.',
    ),
}

STEP_TRANSLATIONS = {
    'Register': (
        'Qeydiyyatdan keç', 'Зарегистрируйтесь',
        'Pulsuz hesabınızı yaradın və subdomen seçin. Restoranınız öz ayrıca məkanına sahib olur.',
        'Создайте бесплатный аккаунт и выберите поддомен. Ваш ресторан получит своё пространство.',
    ),
    'Build Your Menu': (
        'Menyunuzu Qurun', 'Создайте меню',
        'Kateqoriyalar, yeməklər, fotolar və qiymətləri panelinizden əlavə edin. 10 dəqiqədən az.',
        'Добавьте категории, блюда, фото и цены в панели управления. Займёт менее 10 минут.',
    ),
    'Share the QR': (
        'QR Kodunu Paylaşın', 'Поделитесь QR-кодом',
        'QR kodunuzu çap edib masalara qoyun. Qonaqlar skan edir → canlı rəqəmsal menyunuzu görürlər.',
        'Распечатайте QR-код и разместите на столах. Гости сканируют → видят ваше живое меню.',
    ),
}


def populate_translations(apps, schema_editor):
    LandingPage = apps.get_model('public', 'LandingPage')
    LandingFeature = apps.get_model('public', 'LandingFeature')
    LandingStep = apps.get_model('public', 'LandingStep')

    page = LandingPage.objects.filter(pk=1).first()
    if not page:
        return

    page.hero_badge_az = 'Pulsuz Rəqəmsal QR Menyu Platforması'
    page.hero_badge_ru = 'Бесплатная Цифровая QR Меню Платформа'
    page.hero_title_az = 'Restoranınızın Menyusu,'
    page.hero_title_ru = 'Меню вашего ресторана,'
    page.hero_title_em_az = 'Dərhal Rəqəmsal'
    page.hero_title_em_ru = 'Мгновенно Цифровое'
    page.hero_subtitle_az = (
        'Dəqiqələr içərisində restoranınız üçün gözəl QR menyu yaradın. '
        'Tətbiq lazım deyil — qonaqlar skan edib telefonlarında baxır.'
    )
    page.hero_subtitle_ru = (
        'Создайте красивое QR меню для вашего ресторана за несколько минут. '
        'Приложение не нужно — гости сканируют и просматривают на телефоне.'
    )
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

    for feature in LandingFeature.objects.filter(page=page):
        if feature.title in FEATURE_TRANSLATIONS:
            t = FEATURE_TRANSLATIONS[feature.title]
            feature.title_az, feature.title_ru = t[0], t[1]
            feature.description_az, feature.description_ru = t[2], t[3]
            feature.save()

    for step in LandingStep.objects.filter(page=page):
        if step.title in STEP_TRANSLATIONS:
            t = STEP_TRANSLATIONS[step.title]
            step.title_az, step.title_ru = t[0], t[1]
            step.description_az, step.description_ru = t[2], t[3]
            step.save()


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0004_translation_fields'),
    ]

    operations = [
        migrations.RunPython(populate_translations, migrations.RunPython.noop),
    ]
