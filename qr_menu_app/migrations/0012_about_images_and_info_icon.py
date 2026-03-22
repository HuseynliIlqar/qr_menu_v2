from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qr_menu_app', '0011_mainsectionmodel_footer_adress_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainsectionmodel',
            name='about_us_image_main',
            field=models.ImageField(blank=True, null=True, upload_to='about_images/'),
        ),
        migrations.AddField(
            model_name='mainsectionmodel',
            name='about_us_image_accent',
            field=models.ImageField(blank=True, null=True, upload_to='about_images/'),
        ),
        migrations.AddField(
            model_name='infosection',
            name='icon',
            field=models.CharField(
                choices=[
                    ('location', 'Location (Address)'),
                    ('clock', 'Clock (Hours)'),
                    ('truck', 'Truck (Delivery)'),
                    ('phone', 'Phone (Contact)'),
                    ('link', 'Generic Link'),
                ],
                default='link',
                max_length=20,
            ),
        ),
    ]
