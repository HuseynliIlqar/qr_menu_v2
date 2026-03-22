from django.db import models
from django.forms import ValidationError
from django.utils.translation import get_language


class MainSectionModel(models.Model):
    restoran_name = models.CharField(max_length=20, unique=True)
    restoran_icon = models.ImageField(upload_to='restoran_icons/', blank=True, null=True)
    restoran_icon_url = models.CharField(max_length=500, blank=True)
    h1_text = models.CharField(max_length=100)
    h1_text_az = models.CharField(max_length=100, blank=True)
    h1_text_ru = models.CharField(max_length=100, blank=True)
    h1_sub_text = models.CharField(max_length=200)
    h1_sub_text_az = models.CharField(max_length=200, blank=True)
    h1_sub_text_ru = models.CharField(max_length=200, blank=True)
    about_us_title = models.CharField(max_length=100)
    about_us_title_az = models.CharField(max_length=100, blank=True)
    about_us_title_ru = models.CharField(max_length=100, blank=True)
    about_us = models.TextField(max_length=500)
    about_us_az = models.TextField(max_length=500, blank=True)
    about_us_ru = models.TextField(max_length=500, blank=True)
    about_us_image_main = models.ImageField(upload_to='about_images/', blank=True, null=True)
    about_us_image_main_url = models.CharField(max_length=500, blank=True)
    about_us_image_accent = models.ImageField(upload_to='about_images/', blank=True, null=True)
    about_us_image_accent_url = models.CharField(max_length=500, blank=True)
    restoran_reserve_url = models.URLField()
    footer_text = models.CharField(max_length=200)
    footer_adress = models.CharField(max_length=200)
    footer_phone = models.CharField(max_length=20)
    footer_open_time = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.restoran_name

    def save(self, *args, **kwargs):
        if not self.pk:
            if MainSectionModel.objects.count() >= 1:
                raise ValidationError("Yalnız 1 Main Section əlavə etməyə icazə verilir.")
        super().save(*args, **kwargs)

    @property
    def translated_h1_text(self):
        lang = get_language()
        if lang == 'az' and self.h1_text_az:
            return self.h1_text_az
        if lang == 'ru' and self.h1_text_ru:
            return self.h1_text_ru
        return self.h1_text

    @property
    def translated_h1_sub_text(self):
        lang = get_language()
        if lang == 'az' and self.h1_sub_text_az:
            return self.h1_sub_text_az
        if lang == 'ru' and self.h1_sub_text_ru:
            return self.h1_sub_text_ru
        return self.h1_sub_text

    @property
    def translated_about_us_title(self):
        lang = get_language()
        if lang == 'az' and self.about_us_title_az:
            return self.about_us_title_az
        if lang == 'ru' and self.about_us_title_ru:
            return self.about_us_title_ru
        return self.about_us_title

    @property
    def translated_about_us(self):
        lang = get_language()
        if lang == 'az' and self.about_us_az:
            return self.about_us_az
        if lang == 'ru' and self.about_us_ru:
            return self.about_us_ru
        return self.about_us

    @property
    def restoran_icon_src(self):
        if self.restoran_icon:
            return self.restoran_icon.url
        return self.restoran_icon_url or ''

    @property
    def about_us_image_main_src(self):
        if self.about_us_image_main:
            return self.about_us_image_main.url
        return self.about_us_image_main_url or ''

    @property
    def about_us_image_accent_src(self):
        if self.about_us_image_accent:
            return self.about_us_image_accent.url
        return self.about_us_image_accent_url or ''
