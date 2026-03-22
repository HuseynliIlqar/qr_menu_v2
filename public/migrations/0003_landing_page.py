from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0002_tenantuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='LandingPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hero_badge', models.CharField(default='Free Digital QR Menu Platform', max_length=120)),
                ('hero_title', models.CharField(default='Your Restaurant Menu,', max_length=200)),
                ('hero_title_em', models.CharField(default='Instantly Digital', help_text='Displayed on the second line in amber colour.', max_length=100, verbose_name='Hero title (highlighted)')),
                ('hero_subtitle', models.TextField(default='Create a beautiful QR menu for your restaurant in minutes. No app needed — guests scan and browse on their phone.')),
                ('hero_btn_primary', models.CharField(default='Start for Free →', max_length=60)),
                ('hero_btn_secondary', models.CharField(default='Sign In', max_length=60)),
                ('features_label', models.CharField(default='Features', max_length=60)),
                ('features_title', models.CharField(default='Everything your restaurant needs', max_length=200)),
                ('features_subtitle', models.TextField(default='A fully-featured digital menu platform with a powerful management dashboard.')),
                ('steps_label', models.CharField(default='How it works', max_length=60)),
                ('steps_title', models.CharField(default='Up and running in 3 steps', max_length=200)),
                ('steps_subtitle', models.TextField(default='No technical knowledge required.')),
                ('cta_title', models.CharField(default='Ready to go digital?', max_length=200)),
                ('cta_subtitle', models.TextField(default="It's free, takes minutes to set up, and your guests will love it.")),
                ('cta_btn', models.CharField(default='Create Your Menu Now →', max_length=60)),
                ('footer_text', models.CharField(default='© 2026 QRMenu. Built for restaurants.', max_length=300)),
            ],
            options={
                'verbose_name': 'Landing Page',
                'verbose_name_plural': 'Landing Page',
            },
        ),
        migrations.CreateModel(
            name='LandingFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(default='⚡', help_text='Paste an emoji', max_length=10)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('sort_order', models.PositiveSmallIntegerField(default=0)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='public.landingpage')),
            ],
            options={
                'verbose_name': 'Feature Card',
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='LandingStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField()),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('sort_order', models.PositiveSmallIntegerField(default=0)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='public.landingpage')),
            ],
            options={
                'verbose_name': 'How-it-works Step',
                'ordering': ['sort_order', 'number'],
            },
        ),
    ]
