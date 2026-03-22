from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates test data using image URLs (no file uploads). Use --reset to wipe and recreate.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete all existing data before creating new test data.',
        )

    def handle(self, *args, **options):
        from qr_menu_app.models.main_model import MainSectionModel
        from qr_menu_app.models.social_media_icon_model import SocialMediaIconModel
        from qr_menu_app.models.index_slider import IndexSliderPhotoModel
        from qr_menu_app.models.info_section_model import InfoSection
        from qr_menu_app.models.item_category import ItemCategory
        from qr_menu_app.models.menu_item import MenuItem
        from qr_menu_app.models.restoran_galery import RestoranGaleryModel

        if options['reset']:
            MenuItem.objects.all().delete()
            MainSectionModel.objects.all().delete()  # cascades everything
            self.stdout.write(self.style.WARNING('[RESET] All data deleted.'))

        # ── 1. MAIN SECTION ───────────────────────────────────────
        if MainSectionModel.objects.exists():
            self.stdout.write(self.style.WARNING('MainSectionModel already exists, skipping. Use --reset to recreate.'))
            main = MainSectionModel.objects.first()
        else:
            main = MainSectionModel.objects.create(
                restoran_name='Delizioso',
                restoran_icon_url='https://img.icons8.com/color/96/restaurant.png',
                h1_text='Where Every Bite Tells a Story',
                h1_sub_text='Authentic flavors, fresh ingredients, unforgettable moments',
                about_us_title='Passion on Every Plate Since 2018',
                about_us=(
                    'We started Delizioso with a simple belief — that great food should bring people together. '
                    'Our chefs source only the freshest local ingredients, crafting each dish with care and a '
                    'respect for authentic flavors. From our wood-fired pizzas to our signature burgers, '
                    'every item on our menu is a labor of love — made to be shared, savored, and remembered.'
                ),
                about_us_image_main_url='https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=80',
                about_us_image_accent_url='https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&q=80',
                restoran_reserve_url='tel:+994501234567',
                footer_text='Where passion meets the plate. Authentic flavors, crafted with love since 2018.',
                footer_adress='123 Culinary Street, Baku, Azerbaijan',
                footer_phone='+994 50 123 45 67',
                footer_open_time='Mon-Sun: 10:00 - 22:00',
            )
            self.stdout.write(self.style.SUCCESS('[OK] MainSectionModel created'))

        # ── 2. SOCIAL MEDIA ───────────────────────────────────────
        if not SocialMediaIconModel.objects.filter(main_section_model_relaion=main).exists():
            for name, url in [
                ('Instagram', 'https://instagram.com'),
                ('TikTok',    'https://tiktok.com'),
                ('WhatsApp',  'https://wa.me/994501234567'),
            ]:
                SocialMediaIconModel.objects.create(
                    main_section_model_relaion=main,
                    social_media_name=name,
                    social_media_url=url,
                    is_active=True,
                )
            self.stdout.write(self.style.SUCCESS('[OK] Social media icons created'))

        # ── 3. HERO SLIDER ────────────────────────────────────────
        if not IndexSliderPhotoModel.objects.filter(resetion_name=main).exists():
            slide_urls = [
                'https://images.unsplash.com/photo-1632898658030-ead731d252d4?w=1080&q=80',
                'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=1080&q=80',
                'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=1080&q=80',
            ]
            for url in slide_urls:
                IndexSliderPhotoModel.objects.create(
                    resetion_name=main,
                    slide_image_url=url,
                )
            self.stdout.write(self.style.SUCCESS('[OK] Slider images created'))

        # ── 4. INFO SECTIONS ─────────────────────────────────────
        if not InfoSection.objects.filter(resetion_name=main).exists():
            for icon, name, desc, url in [
                ('location', 'Address',      '123 Culinary Street, Baku', 'https://maps.google.com'),
                ('clock',    'Hours',         'Mon-Sun: 10:00 - 22:00',   None),
                ('truck',    'Delivery',      '30-45 minutes',             None),
                ('phone',    'Reservations',  '+994 50 123 45 67',         'tel:+994501234567'),
            ]:
                InfoSection.objects.create(
                    resetion_name=main,
                    icon=icon, name=name, description=desc, info_section_url=url,
                )
            self.stdout.write(self.style.SUCCESS('[OK] Info sections created'))

        # ── 5. GALLERY ────────────────────────────────────────────
        if not RestoranGaleryModel.objects.filter(restoran_name=main).exists():
            gallery_urls = [
                'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=800&q=80',
                'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800&q=80',
                'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80',
                'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80',
                'https://images.unsplash.com/photo-1482049016688-2d3e1b311543?w=800&q=80',
            ]
            for url in gallery_urls:
                RestoranGaleryModel.objects.create(
                    restoran_name=main,
                    galery_image_url=url,
                )
            self.stdout.write(self.style.SUCCESS('[OK] Gallery photos created'))

        # ── 6. CATEGORIES ─────────────────────────────────────────
        cats = {}
        for name, slug, order in [
            ('Burgers',  'burgers',  1),
            ('Pizza',    'pizza',    2),
            ('Salads',   'salads',   3),
            ('Pasta',    'pasta',    4),
            ('Wings',    'wings',    5),
            ('Desserts', 'desserts', 6),
            ('Drinks',   'drinks',   7),
        ]:
            cat, _ = ItemCategory.objects.get_or_create(
                resetion_name=main, slug=slug,
                defaults={'category_name': name, 'sort_order': order, 'is_active': True},
            )
            cats[slug] = cat
        self.stdout.write(self.style.SUCCESS('[OK] Categories created'))

        # ── 7. MENU ITEMS ─────────────────────────────────────────
        if MenuItem.objects.exists():
            self.stdout.write(self.style.WARNING('MenuItems already exist, skipping. Use --reset to recreate.'))
        else:
            items = [
                {
                    'name': 'Classic Burger',
                    'description': 'Juicy beef patty with fresh lettuce, tomato, and special sauce. Served on a toasted brioche bun.',
                    'original_price': 15.99, 'discount_price': 12.99,
                    'ingredients': 'Beef patty, Brioche bun, Lettuce, Tomato, Pickles, Onions, Special sauce',
                    'allergens': 'Gluten, Eggs, Dairy',
                    'cats': ['burgers'],
                    'image_url': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600&q=80',
                },
                {
                    'name': 'Margherita Pizza',
                    'description': 'Traditional Italian pizza with fresh mozzarella and basil, cooked in a wood-fired oven.',
                    'original_price': 14.99, 'discount_price': None,
                    'ingredients': 'Pizza dough, San Marzano tomatoes, Fresh mozzarella, Basil, Olive oil',
                    'allergens': 'Gluten, Dairy',
                    'cats': ['pizza'],
                    'image_url': 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=600&q=80',
                },
                {
                    'name': 'Fresh Garden Salad',
                    'description': 'Mixed greens with seasonal vegetables and homemade balsamic vinaigrette.',
                    'original_price': 9.99, 'discount_price': None,
                    'ingredients': 'Mixed greens, Cherry tomatoes, Cucumbers, Carrots, Bell peppers, Balsamic vinaigrette',
                    'allergens': 'None',
                    'cats': ['salads'],
                    'image_url': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&q=80',
                },
                {
                    'name': 'Creamy Carbonara',
                    'description': 'Classic Roman pasta with crispy pancetta, farm-fresh eggs and aged Parmigiano-Reggiano.',
                    'original_price': 19.99, 'discount_price': 16.99,
                    'ingredients': 'Spaghetti, Pancetta, Eggs, Parmigiano-Reggiano, Black pepper',
                    'allergens': 'Gluten, Eggs, Dairy, Pork',
                    'cats': ['pasta'],
                    'image_url': 'https://images.unsplash.com/photo-1612874742237-6526221588e3?w=600&q=80',
                },
                {
                    'name': 'Spicy Buffalo Wings',
                    'description': 'Crispy chicken wings tossed in signature spicy buffalo sauce. Served with ranch dressing.',
                    'original_price': 13.99, 'discount_price': None,
                    'ingredients': 'Chicken wings, Buffalo sauce, Butter, Garlic, Ranch dressing, Celery',
                    'allergens': 'Dairy',
                    'cats': ['wings'],
                    'image_url': 'https://images.unsplash.com/photo-1527477396000-e27163b481c2?w=600&q=80',
                },
                {
                    'name': 'Truffle Fries',
                    'description': 'Golden hand-cut fries drizzled with premium truffle oil and freshly grated parmesan.',
                    'original_price': 9.99, 'discount_price': 7.99,
                    'ingredients': 'Potatoes, Truffle oil, Parmigiano-Reggiano, Parsley, Sea salt',
                    'allergens': 'Dairy',
                    'cats': ['wings'],
                    'image_url': 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=600&q=80',
                },
                {
                    'name': 'Chocolate Lava Cake',
                    'description': 'Warm chocolate cake with a gooey molten center. Served with vanilla ice cream.',
                    'original_price': 8.99, 'discount_price': None,
                    'ingredients': 'Dark chocolate, Butter, Eggs, Sugar, Flour, Vanilla ice cream',
                    'allergens': 'Gluten, Eggs, Dairy',
                    'cats': ['desserts'],
                    'image_url': 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=600&q=80',
                },
                {
                    'name': 'Craft Lemonade',
                    'description': 'Freshly squeezed lemonade with mint and a hint of ginger. Refreshing and natural.',
                    'original_price': 5.99, 'discount_price': None,
                    'ingredients': 'Lemon juice, Water, Sugar, Mint, Ginger',
                    'allergens': 'None',
                    'cats': ['drinks'],
                    'image_url': 'https://images.unsplash.com/photo-1621263764928-df1444c5e859?w=600&q=80',
                },
            ]

            for data in items:
                item = MenuItem.objects.create(
                    name=data['name'],
                    description=data['description'],
                    original_price=data['original_price'],
                    discount_price=data['discount_price'],
                    image_url=data['image_url'],
                    menu_item_ingredients=data['ingredients'],
                    allergen_information=data['allergens'],
                )
                for slug in data['cats']:
                    if slug in cats:
                        item.category.add(cats[slug])

            self.stdout.write(self.style.SUCCESS('[OK] Menu items created'))

        self.stdout.write(self.style.SUCCESS('\n[DONE] All test data created successfully!'))
