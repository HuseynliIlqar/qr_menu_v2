from django import forms
from django.forms import inlineformset_factory

from qr_menu_app.models import (
    MainSectionModel,
    SocialMediaIconModel,
    IndexSliderPhotoModel,
    InfoSection,
    RestoranGaleryModel,
    ItemCategory,
    MenuItem,
)


# ─────────────────────────────────────────────
#  Widget helpers
# ─────────────────────────────────────────────

class _StyledTextInput(forms.TextInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].setdefault('class', 'db-input')
        super().__init__(*args, **kwargs)


class _StyledURLInput(forms.URLInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].setdefault('class', 'db-input')
        super().__init__(*args, **kwargs)


class _StyledTextarea(forms.Textarea):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].setdefault('class', 'db-textarea')
        kwargs['attrs'].setdefault('rows', '4')
        super().__init__(*args, **kwargs)


class _StyledSelect(forms.Select):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].setdefault('class', 'db-select')
        super().__init__(*args, **kwargs)


class _StyledFileInput(forms.ClearableFileInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].setdefault('class', 'db-file-input')
        super().__init__(*args, **kwargs)


class _StyledNumberInput(forms.NumberInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].setdefault('class', 'db-input')
        super().__init__(*args, **kwargs)


# ─────────────────────────────────────────────
#  Restaurant / Main Section Form
# ─────────────────────────────────────────────

class RestaurantForm(forms.ModelForm):
    """
    Edits MainSectionModel.
    Fieldsets are logical groupings defined as class attributes so templates
    can render them in separate <fieldset> blocks.
    """

    FIELDSET_INFO = [
        'restoran_name',
        'restoran_icon', 'restoran_icon_url',
        'h1_text', 'h1_text_az', 'h1_text_ru',
        'h1_sub_text', 'h1_sub_text_az', 'h1_sub_text_ru',
        'restoran_reserve_url',
    ]

    FIELDSET_ABOUT = [
        'about_us_title', 'about_us_title_az', 'about_us_title_ru',
        'about_us', 'about_us_az', 'about_us_ru',
        'about_us_image_main', 'about_us_image_main_url',
        'about_us_image_accent', 'about_us_image_accent_url',
    ]

    FIELDSET_FOOTER = [
        'footer_text',
        'footer_adress',
        'footer_phone',
        'footer_open_time',
    ]

    class Meta:
        model = MainSectionModel
        exclude = ['create_at', 'update_at']
        widgets = {
            'restoran_name': _StyledTextInput(attrs={'placeholder': 'e.g. The Golden Fork'}),
            'restoran_icon': _StyledFileInput(),
            'restoran_icon_url': _StyledURLInput(attrs={'placeholder': 'https://example.com/icon.png'}),
            'h1_text': _StyledTextInput(attrs={'placeholder': 'Hero headline (EN)'}),
            'h1_text_az': _StyledTextInput(attrs={'placeholder': 'Hero headline (AZ)'}),
            'h1_text_ru': _StyledTextInput(attrs={'placeholder': 'Hero headline (RU)'}),
            'h1_sub_text': _StyledTextInput(attrs={'placeholder': 'Hero sub-headline (EN)'}),
            'h1_sub_text_az': _StyledTextInput(attrs={'placeholder': 'Hero sub-headline (AZ)'}),
            'h1_sub_text_ru': _StyledTextInput(attrs={'placeholder': 'Hero sub-headline (RU)'}),
            'restoran_reserve_url': _StyledURLInput(attrs={'placeholder': 'https://...'}),
            'about_us_title': _StyledTextInput(attrs={'placeholder': 'About section heading (EN)'}),
            'about_us_title_az': _StyledTextInput(attrs={'placeholder': 'About section heading (AZ)'}),
            'about_us_title_ru': _StyledTextInput(attrs={'placeholder': 'About section heading (RU)'}),
            'about_us': _StyledTextarea(attrs={'rows': '5', 'placeholder': 'Write about your restaurant… (EN)'}),
            'about_us_az': _StyledTextarea(attrs={'rows': '5', 'placeholder': 'Write about your restaurant… (AZ)'}),
            'about_us_ru': _StyledTextarea(attrs={'rows': '5', 'placeholder': 'Write about your restaurant… (RU)'}),
            'about_us_image_main': _StyledFileInput(),
            'about_us_image_main_url': _StyledURLInput(attrs={'placeholder': 'https://example.com/image.jpg'}),
            'about_us_image_accent': _StyledFileInput(),
            'about_us_image_accent_url': _StyledURLInput(attrs={'placeholder': 'https://example.com/image.jpg'}),
            'footer_text': _StyledTextInput(attrs={'placeholder': 'Footer tagline'}),
            'footer_adress': _StyledTextInput(attrs={'placeholder': 'Full address'}),
            'footer_phone': _StyledTextInput(attrs={'placeholder': '+994 …'}),
            'footer_open_time': _StyledTextInput(attrs={'placeholder': 'Mon–Sun 10:00–22:00'}),
        }


# ─────────────────────────────────────────────
#  Menu Item Form
# ─────────────────────────────────────────────

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = [
            'name', 'name_az', 'name_ru',
            'description', 'description_az', 'description_ru',
            'original_price',
            'discount_price',
            'image', 'image_url',
            'menu_item_ingredients', 'menu_item_ingredients_az', 'menu_item_ingredients_ru',
            'allergen_information', 'allergen_information_az', 'allergen_information_ru',
            'category',
        ]
        widgets = {
            'name': _StyledTextInput(attrs={'placeholder': 'Dish name (EN)'}),
            'name_az': _StyledTextInput(attrs={'placeholder': 'Dish name (AZ)'}),
            'name_ru': _StyledTextInput(attrs={'placeholder': 'Dish name (RU)'}),
            'description': _StyledTextarea(attrs={'rows': '3', 'placeholder': 'Describe the dish… (EN)'}),
            'description_az': _StyledTextarea(attrs={'rows': '3', 'placeholder': 'Describe the dish… (AZ)'}),
            'description_ru': _StyledTextarea(attrs={'rows': '3', 'placeholder': 'Describe the dish… (RU)'}),
            'original_price': _StyledNumberInput(attrs={'step': '0.01', 'min': '0', 'placeholder': '0.00'}),
            'discount_price': _StyledNumberInput(attrs={'step': '0.01', 'min': '0', 'placeholder': '0.00 (optional)'}),
            'image': _StyledFileInput(),
            'image_url': _StyledURLInput(attrs={'placeholder': 'https://example.com/food.jpg'}),
            'menu_item_ingredients': _StyledTextarea(attrs={'rows': '2', 'placeholder': 'List ingredients… (EN)'}),
            'menu_item_ingredients_az': _StyledTextarea(attrs={'rows': '2', 'placeholder': 'List ingredients… (AZ)'}),
            'menu_item_ingredients_ru': _StyledTextarea(attrs={'rows': '2', 'placeholder': 'List ingredients… (RU)'}),
            'allergen_information': _StyledTextarea(attrs={'rows': '2', 'placeholder': 'e.g. Gluten, Dairy… (EN)'}),
            'allergen_information_az': _StyledTextarea(attrs={'rows': '2', 'placeholder': 'e.g. Gluten, Dairy… (AZ)'}),
            'allergen_information_ru': _StyledTextarea(attrs={'rows': '2', 'placeholder': 'e.g. Gluten, Dairy… (RU)'}),
            'category': forms.CheckboxSelectMultiple(),
        }


# ─────────────────────────────────────────────
#  Inline FormSets
# ─────────────────────────────────────────────

def _apply_widget_class(form_class, field_widget_map):
    """Patch widget classes onto a dynamically generated formset form."""
    for field_name, widget in field_widget_map.items():
        if field_name in form_class.base_fields:
            form_class.base_fields[field_name].widget = widget
    return form_class


# Slider
SliderFormSet = inlineformset_factory(
    MainSectionModel,
    IndexSliderPhotoModel,
    fields=['slide_image', 'slide_image_url'],
    extra=1,
    can_delete=True,
    max_num=3,
    fk_name='resetion_name',
)
_apply_widget_class(SliderFormSet.form, {
    'slide_image': _StyledFileInput(),
    'slide_image_url': _StyledURLInput(attrs={'placeholder': 'https://example.com/slide.jpg'}),
})

# Social Media
SocialFormSet = inlineformset_factory(
    MainSectionModel,
    SocialMediaIconModel,
    fields=['social_media_name', 'social_media_url', 'is_active'],
    extra=1,
    can_delete=True,
    max_num=3,
    fk_name='main_section_model_relaion',
)
_apply_widget_class(SocialFormSet.form, {
    'social_media_name': _StyledTextInput(attrs={'placeholder': 'e.g. Instagram'}),
    'social_media_url': _StyledURLInput(attrs={'placeholder': 'https://instagram.com/…'}),
})

# Info Section
InfoFormSet = inlineformset_factory(
    MainSectionModel,
    InfoSection,
    fields=['icon', 'name', 'name_az', 'name_ru', 'description', 'description_az', 'description_ru', 'info_section_url'],
    extra=1,
    can_delete=True,
    max_num=4,
    fk_name='resetion_name',
)
_apply_widget_class(InfoFormSet.form, {
    'icon': _StyledSelect(),
    'name': _StyledTextInput(attrs={'placeholder': 'Label (EN)'}),
    'name_az': _StyledTextInput(attrs={'placeholder': 'Label (AZ)'}),
    'name_ru': _StyledTextInput(attrs={'placeholder': 'Label (RU)'}),
    'description': _StyledTextarea(attrs={'rows': '2', 'placeholder': 'Short description (EN)'}),
    'description_az': _StyledTextarea(attrs={'rows': '2', 'placeholder': 'Short description (AZ)'}),
    'description_ru': _StyledTextarea(attrs={'rows': '2', 'placeholder': 'Short description (RU)'}),
    'info_section_url': _StyledURLInput(attrs={'placeholder': 'https://… (optional)'}),
})

# Gallery
GalleryFormSet = inlineformset_factory(
    MainSectionModel,
    RestoranGaleryModel,
    fields=['galery_image', 'galery_image_url'],
    extra=1,
    can_delete=True,
    max_num=5,
    fk_name='restoran_name',
)
_apply_widget_class(GalleryFormSet.form, {
    'galery_image': _StyledFileInput(),
    'galery_image_url': _StyledURLInput(attrs={'placeholder': 'https://example.com/photo.jpg'}),
})

# Categories
CategoryFormSet = inlineformset_factory(
    MainSectionModel,
    ItemCategory,
    fields=['category_name', 'category_name_az', 'category_name_ru', 'sort_order', 'is_active'],
    extra=1,
    can_delete=True,
    max_num=10,
    fk_name='resetion_name',
)
_apply_widget_class(CategoryFormSet.form, {
    'category_name': _StyledTextInput(attrs={'placeholder': 'Category name (EN)'}),
    'category_name_az': _StyledTextInput(attrs={'placeholder': 'Category name (AZ)'}),
    'category_name_ru': _StyledTextInput(attrs={'placeholder': 'Category name (RU)'}),
    'sort_order': _StyledNumberInput(attrs={'min': '0', 'placeholder': '0'}),
})
