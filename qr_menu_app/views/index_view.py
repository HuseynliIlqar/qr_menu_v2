from django.shortcuts import render
from django.db.models import Prefetch

from qr_menu_app.models import (
    MainSectionModel,
    SocialMediaIconModel,
    IndexSliderPhotoModel,
    InfoSection,
    ItemCategory,
)
from qr_menu_app.models.menu_item import MenuItem
from qr_menu_app.models.restoran_galery import RestoranGaleryModel


def index_page(request):
    categories_qs = ItemCategory.objects.filter(is_active=True).prefetch_related(
        Prefetch(
            "menu_items",
            queryset=MenuItem.objects.only(
                "id", "name", "description",
                "original_price", "discount_price", "price_save",
                "image", "menu_item_ingredients", "allergen_information",
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
                    "id", "name", "description", "info_section_url"
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
            "id", "restoran_name", "restoran_icon",
            "h1_text", "h1_sub_text",
            "about_us_title", "about_us",
            "restoran_reserve_url",
            "footer_text", "footer_adress",
            "footer_phone", "footer_open_time",
        )
        .first()
    )

    context = {
        "main": main,
    }

    return render(request, "index.html", context)
