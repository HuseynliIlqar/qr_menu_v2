from django.contrib import admin
from django import forms
from django.db import models
from qr_menu_app.models.index_slider import IndexSliderPhotoModel
from qr_menu_app.models.info_section_model import InfoSection
from qr_menu_app.models.main_model import MainSectionModel
from qr_menu_app.models.menu_item import MenuItem
from qr_menu_app.models.social_media_icon_model import SocialMediaIconModel


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

class InfoSectionInline(admin.TabularInline):
    model = InfoSection
    extra = 0
    min_num = 1
    max_num = 4
    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(attrs={
                "rows": 2,
                "cols": 30,
                "style": "resize: vertical;"
            })
        }
    }


class ItemCategoryInline(admin.TabularInline):
    from qr_menu_app.models.item_category import ItemCategory
    model = ItemCategory
    extra = 0
    min_num = 0
    max_num = 10

class RestoranGaleryInline(admin.TabularInline):
    from qr_menu_app.models.restoran_galery import RestoranGaleryModel
    model = RestoranGaleryModel
    extra = 0
    min_num = 0
    max_num = 5


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "original_price", "discount_price", "create_at", "update_at")

@admin.register(MainSectionModel)
class MainSectionAdmin(admin.ModelAdmin):
    list_display = ("restoran_name", "create_at", "update_at")
    inlines = [SocialMediaIconInline, IndexSliderPhotoInline, InfoSectionInline,ItemCategoryInline, RestoranGaleryInline]
