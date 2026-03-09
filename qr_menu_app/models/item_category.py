from django.db import models
from django.utils.text import slugify

class ItemCategory(models.Model):
    resetion_name = models.ForeignKey("MainSectionModel", on_delete=models.CASCADE, related_name="item_categories")
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "category_name"]

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.category_name) or "category"
            slug = base
            i = 2
            while ItemCategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)