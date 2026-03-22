"""
Generates binary .mo translation files from inline Python dicts.
No external gettext tools required.

Usage:
    python manage.py compile_translations
"""

import os
import struct
from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings


# ─────────────────────────────────────────────────────────────
#  All UI translations
# ─────────────────────────────────────────────────────────────

TRANSLATIONS = {

    # ── Azerbaijani ───────────────────────────────────────────
    'az': {
        # Public nav
        'Log in':          'Daxil ol',
        'Get Started':     'Başla',
        'Register':        'Qeydiyyat',

        # Public login page
        'Welcome back':                              'Xoş gəldiniz',
        'Sign in to manage your restaurant':         'Restoranınızı idarə etmək üçün daxil olun',
        'Sign In →':                                 'Daxil ol →',
        'New here?':                                 'Yeni istifadəçisiniz?',
        'Create your restaurant':                    'Restoranınızı yaradın',

        # Public register page
        'Create your restaurant account':            'Restoran hesabınızı yaradın',
        'Takes less than 2 minutes. No credit card required.': '2 dəqiqədən az vaxt aparır. Kredit kartı tələb olunmur.',
        'Restaurant Name':       'Restoran adı',
        'Your Menu URL':         'Menyu URL-niz',
        'Email':                 'E-poçt',
        'Password':              'Şifrə',
        'Confirm Password':      'Şifrəni təsdiqlə',
        'Create My Restaurant →': 'Restoranımı yarat →',
        'Already have an account?': 'Artıq hesabınız var?',
        'Sign in':               'Daxil ol',
        'lowercase letters, numbers and hyphens only. Min 2 characters.':
            'Yalnız kiçik hərflər, rəqəmlər və tire. Min 2 simvol.',

        # Form labels (shared)
        'Username': 'İstifadəçi adı',

        # Dashboard sidebar
        'Overview':        'Ümumi baxış',
        'Content':         'Məzmun',
        'Dashboard':       'İdarə Paneli',
        'Restaurant Info': 'Restoran Məlumatları',
        'Hero Sliders':    'Slaydlar',
        'Social Media':    'Sosial Media',
        'Info Strip':      'Məlumat Bölməsi',
        'Gallery':         'Qalerya',
        'Menu':            'Menyu',
        'Categories':      'Kateqoriyalar',
        'Menu Items':      'Menyu Elementləri',
        'Logout':          'Çıxış',

        # Dashboard buttons / messages
        'Save Changes':       'Dəyişiklikləri saxla',
        'Save Gallery':       'Qalereyayı saxla',
        'Save Sliders':       'Slaydları saxla',
        'Save':               'Saxla',
        'Back':               'Geri',
        'Cancel':             'Ləğv et',
        'Delete Item':        'Elementi sil',
        'Add Item':           'Əlavə et',
        '← Back to Menu':    '← Menyuya qayıt',
        'Back to Menu':       'Menyuya qayıt',

        # Dashboard page titles
        'Dashboard Overview':    'İdarə Paneli',
        'Restaurant Gallery':    'Restoran Qalereyası',
        'Menu Categories':       'Menyu Kateqoriyaları',

        # QR menu navbar
        'About':    'Haqqında',
        'Contact':  'Əlaqə',

        # QR menu hero
        'View Menu':         'Menyuya bax',
        'Reserve a Table':   'Masa sifariş et',
        'Open Now':          'İndi açıqdır',
        'Closed':            'Bağlıdır',

        # QR menu sections
        'All':              'Hamısı',
        'Ingredients:':     'İnqrediyentlər:',
        'Allergens:':       'Allergenlər:',
        'Our Menu':         'Menyumuz',
        'Our Gallery':      'Qalereyamız',
        'About Us':         'Haqqımızda',
    },

    # ── Russian ───────────────────────────────────────────────
    'ru': {
        # Public nav
        'Log in':      'Войти',
        'Get Started': 'Начать',
        'Register':    'Регистрация',

        # Public login page
        'Welcome back':                              'Добро пожаловать',
        'Sign in to manage your restaurant':         'Войдите для управления рестораном',
        'Sign In →':                                 'Войти →',
        'New here?':                                 'Впервые здесь?',
        'Create your restaurant':                    'Создайте ресторан',

        # Public register page
        'Create your restaurant account':            'Создайте аккаунт ресторана',
        'Takes less than 2 minutes. No credit card required.': 'Займет менее 2 минут. Кредитная карта не требуется.',
        'Restaurant Name':       'Название ресторана',
        'Your Menu URL':         'URL вашего меню',
        'Email':                 'Эл. почта',
        'Password':              'Пароль',
        'Confirm Password':      'Подтвердите пароль',
        'Create My Restaurant →': 'Создать мой ресторан →',
        'Already have an account?': 'Уже есть аккаунт?',
        'Sign in':               'Войти',
        'lowercase letters, numbers and hyphens only. Min 2 characters.':
            'Только строчные буквы, цифры и дефисы. Мин. 2 символа.',

        # Form labels (shared)
        'Username': 'Имя пользователя',

        # Dashboard sidebar
        'Overview':        'Обзор',
        'Content':         'Контент',
        'Dashboard':       'Панель управления',
        'Restaurant Info': 'Информация о ресторане',
        'Hero Sliders':    'Слайдер',
        'Social Media':    'Социальные сети',
        'Info Strip':      'Информационная полоса',
        'Gallery':         'Галерея',
        'Menu':            'Меню',
        'Categories':      'Категории',
        'Menu Items':      'Пункты меню',
        'Logout':          'Выход',

        # Dashboard buttons / messages
        'Save Changes':       'Сохранить изменения',
        'Save Gallery':       'Сохранить галерею',
        'Save Sliders':       'Сохранить слайдер',
        'Save':               'Сохранить',
        'Back':               'Назад',
        'Cancel':             'Отмена',
        'Delete Item':        'Удалить',
        'Add Item':           'Добавить',
        '← Back to Menu':    '← К меню',
        'Back to Menu':       'К меню',

        # Dashboard page titles
        'Dashboard Overview':    'Панель управления',
        'Restaurant Gallery':    'Галерея ресторана',
        'Menu Categories':       'Категории меню',

        # QR menu navbar
        'About':    'О нас',
        'Contact':  'Контакт',

        # QR menu hero
        'View Menu':         'Смотреть меню',
        'Reserve a Table':   'Забронировать стол',
        'Open Now':          'Сейчас открыто',
        'Closed':            'Закрыто',

        # QR menu sections
        'All':              'Все',
        'Ingredients:':     'Ингредиенты:',
        'Allergens:':       'Аллергены:',
        'Our Menu':         'Наше меню',
        'Our Gallery':      'Наша галерея',
        'About Us':         'О нас',
    },
}


# ─────────────────────────────────────────────────────────────
#  Pure-Python .mo file writer (no gettext binary needed)
# ─────────────────────────────────────────────────────────────

def _write_mo(translations: dict, path: str) -> None:
    """Write a GNU .mo binary file from a {msgid: msgstr} dict."""
    # Metadata entry (empty msgid → content-type header)
    all_trans = {
        '': 'Content-Type: text/plain; charset=UTF-8\nContent-Transfer-Encoding: 8bit\n',
        **translations,
    }

    keys = sorted(all_trans.keys())
    vals = [all_trans[k] for k in keys]
    N = len(keys)

    kenc = [k.encode('utf-8') for k in keys]
    venc = [v.encode('utf-8') for v in vals]

    # 28-byte header + two N×8-byte tables
    data_start = 28 + N * 16

    ktable = b''
    kdata  = b''
    pos = data_start
    for k in kenc:
        ktable += struct.pack('<II', len(k), pos)
        kdata  += k + b'\x00'
        pos    += len(k) + 1

    vtable = b''
    vdata  = b''
    for v in venc:
        vtable += struct.pack('<II', len(v), pos)
        vdata  += v + b'\x00'
        pos    += len(v) + 1

    # magic, revision, N, orig-table-offset, trans-table-offset, hash-size, hash-offset
    header = struct.pack('<IIIIIII',
                         0x950412de, 0, N,
                         28, 28 + N * 8,
                         0, 0)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(header + ktable + vtable + kdata + vdata)


# ─────────────────────────────────────────────────────────────
#  Management command
# ─────────────────────────────────────────────────────────────

class Command(BaseCommand):
    help = 'Compile inline Python translations to binary .mo files (no gettext required).'

    def handle(self, *args, **options):
        locale_root = Path(settings.BASE_DIR) / 'locale'

        for lang, trans in TRANSLATIONS.items():
            mo_path = str(locale_root / lang / 'LC_MESSAGES' / 'django.mo')
            _write_mo(trans, mo_path)
            self.stdout.write(self.style.SUCCESS(
                f'[OK] locale/{lang}/LC_MESSAGES/django.mo  ({len(trans)} strings)'
            ))

        self.stdout.write(self.style.SUCCESS('\n[DONE] Translation files compiled.'))
