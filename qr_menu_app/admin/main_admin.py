from django.contrib import admin
from django import forms
from django.db import models
from qr_menu_app.models.index_slider import IndexSliderPhotoModel
from qr_menu_app.models.info_section_model import InfoSection
from qr_menu_app.models.main_model import MainSectionModel
from qr_menu_app.models.social_media_icon_model import SocialMediaIconModel


class SocialMediaIconInline(admin.TabularInline):
    model = SocialMediaIconModel
    min_num = 1
    max_num = 3

class IndexSliderPhotoInline(admin.TabularInline):
    model = IndexSliderPhotoModel
    min_num = 1
    max_num = 3

class InfoSectionInline(admin.TabularInline):
    model = InfoSection
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




@admin.register(MainSectionModel)
class MainSectionAdmin(admin.ModelAdmin):
    list_display = ("restoran_name", "create_at", "update_at")
    inlines = [SocialMediaIconInline, IndexSliderPhotoInline, InfoSectionInline]
