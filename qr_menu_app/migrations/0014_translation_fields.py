from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qr_menu_app', '0013_image_url_fields'),
    ]

    operations = [
        # MainSectionModel translation fields
        migrations.AddField(
            model_name='mainsectionmodel',
            name='h1_text_az',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='mainsectionmodel',
            name='h1_text_ru',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='mainsectionmodel',
            name='h1_sub_text_az',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='mainsectionmodel',
            name='h1_sub_text_ru',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='mainsectionmodel',
            name='about_us_title_az',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='mainsectionmodel',
            name='about_us_title_ru',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='mainsectionmodel',
            name='about_us_az',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='mainsectionmodel',
            name='about_us_ru',
            field=models.TextField(blank=True, max_length=500),
        ),
        # MenuItem translation fields
        migrations.AddField(
            model_name='menuitem',
            name='name_az',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='name_ru',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='description_az',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='description_ru',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='menu_item_ingredients_az',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='menu_item_ingredients_ru',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='allergen_information_az',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='allergen_information_ru',
            field=models.CharField(blank=True, max_length=300),
        ),
        # ItemCategory translation fields
        migrations.AddField(
            model_name='itemcategory',
            name='category_name_az',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='itemcategory',
            name='category_name_ru',
            field=models.CharField(blank=True, max_length=50),
        ),
        # InfoSection translation fields
        migrations.AddField(
            model_name='infosection',
            name='name_az',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='infosection',
            name='name_ru',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='infosection',
            name='description_az',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='infosection',
            name='description_ru',
            field=models.TextField(blank=True),
        ),
    ]
