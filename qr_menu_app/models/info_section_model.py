from django.db import models
from django.forms import ValidationError

class InfoSection(models.Model):
    resetion_name = models.ForeignKey("MainSectionModel", on_delete=models.CASCADE, related_name="info_sections")
    name = models.CharField(max_length=255,blank=False, null=False)
    description = models.TextField(blank=True, null=True)   
    info_section_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def clean(self):
        if not self.name:
            raise ValidationError('Name is required.')
        
    def save(self, *args, **kwargs):
        if not self.pk:
            if InfoSection.objects.count() >= 4:
                raise ValidationError("Yalnız 4 Info Section əlavə etməyə icazə verilir.")
        super().save(*args, **kwargs)