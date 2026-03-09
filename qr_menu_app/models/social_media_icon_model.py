from django.db import models
from django.forms import ValidationError

class SocialMediaIconModel(models.Model):
    main_section_model_relaion = models.ForeignKey("MainSectionModel", on_delete=models.CASCADE, related_name="social_media_icons")
    social_media_name = models.CharField(max_length=20)
    social_media_url = models.URLField()
    is_active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            if SocialMediaIconModel.objects.count() >= 3:
                raise ValidationError("Yalnız 3 Social Media Icon əlavə etməyə icazə verilir.")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.social_media_name