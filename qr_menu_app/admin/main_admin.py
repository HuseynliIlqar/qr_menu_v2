from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.db import models

from qr_menu_app.models.index_slider import IndexSliderPhotoModel
from qr_menu_app.models.info_section_model import InfoSection
from qr_menu_app.models.main_model import MainSectionModel
from qr_menu_app.models.menu_item import MenuItem
from qr_menu_app.models.social_media_icon_model import SocialMediaIconModel
from qr_menu_app.models.item_category import ItemCategory
from qr_menu_app.models.restoran_galery import RestoranGaleryModel


class SocialMediaIconInline(admin.TabularInline):
    model = SocialMediaIconModel
    extra = 0
    min_num = 1
    max_num = 3


class IndexSliderPhotoInline(admin.TabularInline):
    model = IndexSliderPhotoModel
    extra = 0
    min_num = 1
    max_num = 3
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.slide_image:
            return format_html('<img src="{}" style="height:60px;object-fit:cover;border-radius:4px;">', obj.slide_image.url)
        return '-'
    preview.short_description = 'Preview'


class InfoSectionInline(admin.TabularInline):
    model = InfoSection
    extra = 0
    min_num = 1
    max_num = 4
    formfield_overrides = {
        models.TextField: {
            'widget': forms.Textarea(attrs={'rows': 2, 'cols': 30, 'style': 'resize:vertical;'})
        }
    }


class ItemCategoryInline(admin.TabularInline):
    model = ItemCategory
    extra = 0
    min_num = 0
    max_num = 10


class RestoranGaleryInline(admin.TabularInline):
    model = RestoranGaleryModel
    extra = 0
    min_num = 0
    max_num = 5
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.galery_image:
            return format_html('<img src="{}" style="height:60px;object-fit:cover;border-radius:4px;">', obj.galery_image.url)
        return '-'
    preview.short_description = 'Preview'


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'original_price', 'discount_price', 'image_preview', 'create_at')
    list_filter = ('category',)
    search_fields = ('name',)
    filter_horizontal = ('category',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;object-fit:cover;border-radius:4px;">', obj.image.url)
        return '-'
    image_preview.short_description = 'Photo'


@admin.register(MainSectionModel)
class MainSectionAdmin(admin.ModelAdmin):
    list_display = ('restoran_name', 'create_at', 'update_at')
    readonly_fields = ('about_main_preview', 'about_accent_preview', 'icon_preview')
    fieldsets = (
        ('Restaurant Info', {
            'fields': ('restoran_name', 'restoran_icon', 'icon_preview', 'restoran_reserve_url')
        }),
        ('Hero Section', {
            'fields': ('h1_text', 'h1_sub_text')
        }),
        ('About Section', {
            'fields': (
                'about_us_title', 'about_us',
                'about_us_image_main', 'about_main_preview',
                'about_us_image_accent', 'about_accent_preview',
            )
        }),
        ('Footer', {
            'fields': ('footer_text', 'footer_adress', 'footer_phone', 'footer_open_time')
        }),
    )
    inlines = [
        SocialMediaIconInline,
        IndexSliderPhotoInline,
        InfoSectionInline,
        ItemCategoryInline,
        RestoranGaleryInline,
    ]

    def icon_preview(self, obj):
        if obj.restoran_icon:
            return format_html('<img src="{}" style="height:50px;object-fit:contain;">', obj.restoran_icon.url)
        return '-'
    icon_preview.short_description = 'Icon Preview'

    def about_main_preview(self, obj):
        if obj.about_us_image_main:
            return format_html('<img src="{}" style="height:80px;object-fit:cover;border-radius:4px;">', obj.about_us_image_main.url)
        return '-'
    about_main_preview.short_description = 'Main Image Preview'

    def about_accent_preview(self, obj):
        if obj.about_us_image_accent:
            return format_html('<img src="{}" style="height:80px;object-fit:cover;border-radius:4px;">', obj.about_us_image_accent.url)
        return '-'
    about_accent_preview.short_description = 'Accent Image Preview'
