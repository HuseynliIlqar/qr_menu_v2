from django.db import models
from django.utils.translation import get_language


class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    name_az = models.CharField(max_length=50, blank=True)
    name_ru = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=False, null=False)
    description_az = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    price_save = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to="menu_items/", blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True)
    menu_item_ingredients = models.CharField(max_length=300, blank=False, null=False)
    menu_item_ingredients_az = models.CharField(max_length=300, blank=True)
    menu_item_ingredients_ru = models.CharField(max_length=300, blank=True)
    allergen_information = models.CharField(max_length=300, blank=False, null=False)
    allergen_information_az = models.CharField(max_length=300, blank=True)
    allergen_information_ru = models.CharField(max_length=300, blank=True)
    category = models.ManyToManyField("ItemCategory", related_name="menu_items")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

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
        return self.description

    @property
    def translated_ingredients(self):
        lang = get_language()
        if lang == 'az' and self.menu_item_ingredients_az:
            return self.menu_item_ingredients_az
        if lang == 'ru' and self.menu_item_ingredients_ru:
            return self.menu_item_ingredients_ru
        return self.menu_item_ingredients

    @property
    def translated_allergens(self):
        lang = get_language()
        if lang == 'az' and self.allergen_information_az:
            return self.allergen_information_az
        if lang == 'ru' and self.allergen_information_ru:
            return self.allergen_information_ru
        return self.allergen_information

    @property
    def image_src(self):
        if self.image:
            return self.image.url
        return self.image_url or ''
