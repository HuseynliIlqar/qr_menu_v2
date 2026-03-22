from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qr_menu_app', '0012_about_images_and_info_icon'),
    ]

    operations = [
        # MainSectionModel — icon optional + url field
        migrations.AlterField(
            model_name='mainsectionmodel',
            name='restoran_icon',
            field=models.ImageField(blank=True, null=True, upload_to='restoran_icons/'),
        ),
        migrations.AddField(
            model_name='mainsectionmodel',
            name='restoran_icon_url',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='mainsectionmodel',
            name='about_us_image_main_url',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='mainsectionmodel',
            name='about_us_image_accent_url',
            field=models.CharField(blank=True, max_length=500),
        ),

        # IndexSliderPhotoModel — optional + url field
        migrations.AlterField(
            model_name='indexsliderphotomodel',
            name='slide_image',
            field=models.ImageField(blank=True, null=True, upload_to='index_slider_photos/'),
        ),
        migrations.AddField(
            model_name='indexsliderphotomodel',
            name='slide_image_url',
            field=models.CharField(blank=True, max_length=500),
        ),

        # RestoranGaleryModel — optional + url field
        migrations.AlterField(
            model_name='restorangalerymodel',
            name='galery_image',
            field=models.ImageField(blank=True, null=True, upload_to='restoran_galery_photos/'),
        ),
        migrations.AddField(
            model_name='restorangalerymodel',
            name='galery_image_url',
            field=models.CharField(blank=True, max_length=500),
        ),

        # MenuItem — optional + url field
        migrations.AlterField(
            model_name='menuitem',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='menu_items/'),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='image_url',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
