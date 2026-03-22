from django.db import models
from django.forms import ValidationError
from django.utils.translation import get_language


class InfoSection(models.Model):
    ICON_CHOICES = [
        ('location', 'Location (Address)'),
        ('clock', 'Clock (Hours)'),
        ('truck', 'Truck (Delivery)'),
        ('phone', 'Phone (Contact)'),
        ('link', 'Generic Link'),
    ]

    resetion_name = models.ForeignKey("MainSectionModel", on_delete=models.CASCADE, related_name="info_sections")
    icon = models.CharField(max_length=20, choices=ICON_CHOICES, default='link')
    name = models.CharField(max_length=255, blank=False, null=False)
    name_az = models.CharField(max_length=255, blank=True)
    name_ru = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, null=True)
    description_az = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)
    info_section_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def translated_name(self):
        lang = get_language()
        if lang == 'az' and self.name_az:
            return self.name_az
        if lang == 'ru' and self.name_ru:
            return self.name_ru
        return self.name

    @property
    def translated_description(self):
        lang = get_language()
        if lang == 'az' and self.description_az:
            return self.description_az
        if lang == 'ru' and self.description_ru:
            return self.description_ru
        return self.description or ''

    def clean(self):
        if not self.name:
            raise ValidationError('Name is required.')
        
    def save(self, *args, **kwargs):
        if not self.pk:
            if InfoSection.objects.count() >= 4:
                raise ValidationError("Yalnız 4 Info Section əlavə etməyə icazə verilir.")
        super().save(*args, **kwargs)