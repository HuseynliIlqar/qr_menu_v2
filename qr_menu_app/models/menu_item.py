from venv import create

from django.db import models


class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=False, null=False)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    price_save = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to="menu_items/", blank=False, null=False)
    # menu_item_tags = models.ManyToManyField("MenuItemTag", blank=True, related_name="menu_items_tags")
    menu_item_ingredients = models.CharField(max_length=300, blank=False, null=False)
    allergen_information = models.CharField(max_length=300, blank=False, null=False)
    category = models.ManyToManyField("ItemCategory",related_name="menu_items")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name