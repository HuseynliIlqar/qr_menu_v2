import json

from django.shortcuts import render
from django.db.models import Prefetch

from qr_menu_app.models import (
    MainSectionModel,
    SocialMediaIconModel,
    IndexSliderPhotoModel,
    InfoSection,
    ItemCategory,
    MenuItem,
)
from qr_menu_app.models.restoran_galery import RestoranGaleryModel


def index_page(request):
    categories_qs = ItemCategory.objects.filter(is_active=True).prefetch_related(
        Prefetch(
            "menu_items",
            queryset=MenuItem.objects.only(
                "id", "name", "name_az", "name_ru",
                "description", "description_az", "description_ru",
                "original_price", "discount_price",
                "image", "image_url",
                "menu_item_ingredients", "menu_item_ingredients_az", "menu_item_ingredients_ru",
                "allergen_information", "allergen_information_az", "allergen_information_ru",
            ),
            to_attr="items",
        )
    )

    main = (
        MainSectionModel.objects.prefetch_related(
            Prefetch(
                "social_media_icons",
                queryset=SocialMediaIconModel.objects.filter(is_active=True).only(
                    "id", "social_media_name", "social_media_url"
                ),
                to_attr="socials",
            ),
            Prefetch(
                "index_slider_photos",
                queryset=IndexSliderPhotoModel.objects.only("id", "slide_image"),
                to_attr="sliders",
            ),
            Prefetch(
                "restoran_galery_photos",
                queryset=RestoranGaleryModel.objects.only("id", "galery_image"),
                to_attr="gallery",
            ),
            Prefetch(
                "info_sections",
                queryset=InfoSection.objects.only(
                    "id", "icon", "name", "description", "info_section_url"
                ),
                to_attr="infos",
            ),
            Prefetch(
                "item_categories",
                queryset=categories_qs,
                to_attr="categories",
            ),
        )
        .only(
            "id", "restoran_name", "restoran_icon", "restoran_icon_url",
            "h1_text", "h1_text_az", "h1_text_ru",
            "h1_sub_text", "h1_sub_text_az", "h1_sub_text_ru",
            "about_us_title", "about_us_title_az", "about_us_title_ru",
            "about_us", "about_us_az", "about_us_ru",
            "about_us_image_main", "about_us_image_main_url",
            "about_us_image_accent", "about_us_image_accent_url",
            "restoran_reserve_url",
            "footer_text", "footer_adress",
            "footer_phone", "footer_open_time",
        )
        .first()
    )

    # Build flat foods list for JS
    foods = []
    if main:
        seen_ids = set()
        for cat in main.categories:
            for item in cat.items:
                if item.id not in seen_ids:
                    seen_ids.add(item.id)
                    # Collect all category slugs for this item
                    item_cats = [cat.slug]
                else:
                    # Item already added; append this cat slug
                    for f in foods:
                        if f['id'] == str(item.id):
                            if cat.slug not in f['cats']:
                                f['cats'].append(cat.slug)
                                f['cat'] = f['cats'][0]
                            break
                    continue

                foods.append({
                    'id': str(item.id),
                    'name': item.translated_name,
                    'desc': item.translated_description,
                    'long': item.translated_description,
                    'price': float(item.discount_price) if item.discount_price else float(item.original_price),
                    'origPrice': float(item.original_price) if item.discount_price else None,
                    'img': request.build_absolute_uri(item.image.url) if item.image else (item.image_url or ''),
                    'cat': item_cats[0],
                    'cats': item_cats,
                    'tags': [],
                    'ingredients': [i.strip() for i in item.translated_ingredients.split(',')] if item.translated_ingredients else [],
                    'allergens': [a.strip() for a in item.translated_allergens.split(',')] if item.translated_allergens else [],
                })

    context = {
        "main": main,
        "foods_json": json.dumps(foods, ensure_ascii=False),
    }

    return render(request, "index.html", context)
