from django.db import models
from django.forms import ValidationError


class MainSectionModel(models.Model):
    restoran_name = models.CharField(max_length=20,unique=True)
    restoran_icon = models.ImageField(upload_to='restoran_icons/')
    h1_text = models.CharField(max_length=100)
    h1_sub_text = models.CharField(max_length=200)
    about_us_title = models.CharField(max_length=100)
    about_us = models.TextField(max_length=500)
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
