from django.db import models
from django.forms import ValidationError


class IndexSliderPhotoModel(models.Model):
    resetion_name = models.ForeignKey("MainSectionModel", on_delete=models.CASCADE, related_name="index_slider_photos")
    slide_image= models.ImageField(upload_to='index_slider_photos/')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Slide Image {self.resetion_name}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            if IndexSliderPhotoModel.objects.count() >= 3:
                raise ValidationError("Yalnız 3 Index Slider Photo əlavə etməyə icazə verilir.")
        super().save(*args, **kwargs)