from django.db import models
from django.forms import ValidationError


class RestoranGaleryModel(models.Model):
    restoran_name = models.ForeignKey("MainSectionModel", on_delete=models.CASCADE, related_name="restoran_galery_photos")
    galery_image = models.ImageField(upload_to='restoran_galery_photos/', blank=True, null=True)
    galery_image_url = models.CharField(max_length=500, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Restoran Galery Image {self.restoran_name}"

    def save(self, *args, **kwargs):
        if not self.pk:
            if RestoranGaleryModel.objects.filter(restoran_name=self.restoran_name).count() >= 5:
                raise ValidationError("Yalnız 5 Restoran Galery Photo əlavə etməyə icazə verilir.")
        super().save(*args, **kwargs)

    @property
    def galery_image_src(self):
        if self.galery_image:
            return self.galery_image.url
        return self.galery_image_url or ''
