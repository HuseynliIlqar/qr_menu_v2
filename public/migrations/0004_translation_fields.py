from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0003_landing_page'),
    ]

    operations = [
        # LandingPage translation fields
        migrations.AddField('LandingPage', 'hero_badge_az',        models.CharField(blank=True, default='', max_length=120)),
        migrations.AddField('LandingPage', 'hero_badge_ru',        models.CharField(blank=True, default='', max_length=120)),
        migrations.AddField('LandingPage', 'hero_title_az',        models.CharField(blank=True, default='', max_length=200)),
        migrations.AddField('LandingPage', 'hero_title_ru',        models.CharField(blank=True, default='', max_length=200)),
        migrations.AddField('LandingPage', 'hero_title_em_az',     models.CharField(blank=True, default='', max_length=100)),
        migrations.AddField('LandingPage', 'hero_title_em_ru',     models.CharField(blank=True, default='', max_length=100)),
        migrations.AddField('LandingPage', 'hero_subtitle_az',     models.TextField(blank=True, default='')),
        migrations.AddField('LandingPage', 'hero_subtitle_ru',     models.TextField(blank=True, default='')),
        migrations.AddField('LandingPage', 'hero_btn_primary_az',  models.CharField(blank=True, default='', max_length=60)),
        migrations.AddField('LandingPage', 'hero_btn_primary_ru',  models.CharField(blank=True, default='', max_length=60)),
        migrations.AddField('LandingPage', 'hero_btn_secondary_az', models.CharField(blank=True, default='', max_length=60)),
        migrations.AddField('LandingPage', 'hero_btn_secondary_ru', models.CharField(blank=True, default='', max_length=60)),
        migrations.AddField('LandingPage', 'features_label_az',    models.CharField(blank=True, default='', max_length=60)),
        migrations.AddField('LandingPage', 'features_label_ru',    models.CharField(blank=True, default='', max_length=60)),
        migrations.AddField('LandingPage', 'features_title_az',    models.CharField(blank=True, default='', max_length=200)),
        migrations.AddField('LandingPage', 'features_title_ru',    models.CharField(blank=True, default='', max_length=200)),
        migrations.AddField('LandingPage', 'features_subtitle_az', models.TextField(blank=True, default='')),
        migrations.AddField('LandingPage', 'features_subtitle_ru', models.TextField(blank=True, default='')),
        migrations.AddField('LandingPage', 'steps_label_az',       models.CharField(blank=True, default='', max_length=60)),
        migrations.AddField('LandingPage', 'steps_label_ru',       models.CharField(blank=True, default='', max_length=60)),
        migrations.AddField('LandingPage', 'steps_title_az',       models.CharField(blank=True, default='', max_length=200)),
        migrations.AddField('LandingPage', 'steps_title_ru',       models.CharField(blank=True, default='', max_length=200)),
        migrations.AddField('LandingPage', 'steps_subtitle_az',    models.TextField(blank=True, default='')),
        migrations.AddField('LandingPage', 'steps_subtitle_ru',    models.TextField(blank=True, default='')),
        migrations.AddField('LandingPage', 'cta_title_az',         models.CharField(blank=True, default='', max_length=200)),
        migrations.AddField('LandingPage', 'cta_title_ru',         models.CharField(blank=True, default='', max_length=200)),
        migrations.AddField('LandingPage', 'cta_subtitle_az',      models.TextField(blank=True, default='')),
        migrations.AddField('LandingPage', 'cta_subtitle_ru',      models.TextField(blank=True, default='')),
        migrations.AddField('LandingPage', 'cta_btn_az',           models.CharField(blank=True, default='', max_length=60)),
        migrations.AddField('LandingPage', 'cta_btn_ru',           models.CharField(blank=True, default='', max_length=60)),
        migrations.AddField('LandingPage', 'footer_text_az',       models.CharField(blank=True, default='', max_length=300)),
        migrations.AddField('LandingPage', 'footer_text_ru',       models.CharField(blank=True, default='', max_length=300)),

        # LandingFeature translation fields
        migrations.AddField('LandingFeature', 'title_az',       models.CharField(blank=True, default='', max_length=100)),
        migrations.AddField('LandingFeature', 'title_ru',       models.CharField(blank=True, default='', max_length=100)),
        migrations.AddField('LandingFeature', 'description_az', models.TextField(blank=True, default='')),
        migrations.AddField('LandingFeature', 'description_ru', models.TextField(blank=True, default='')),

        # LandingStep translation fields
        migrations.AddField('LandingStep', 'title_az',       models.CharField(blank=True, default='', max_length=100)),
        migrations.AddField('LandingStep', 'title_ru',       models.CharField(blank=True, default='', max_length=100)),
        migrations.AddField('LandingStep', 'description_az', models.TextField(blank=True, default='')),
        migrations.AddField('LandingStep', 'description_ru', models.TextField(blank=True, default='')),
    ]
