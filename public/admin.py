from django.contrib import admin
from django.utils.html import format_html

from .models import Client, Domain, TenantUser, LandingPage, LandingFeature, LandingStep


# ── Tenant admin ──────────────────────────────────────────────

class DomainInLineAdmin(admin.TabularInline):
    model = Domain
    min_num = 1
    max_num = 1
    extra = 0


class TenantUserInlineAdmin(admin.TabularInline):
    model = TenantUser
    extra = 0
    readonly_fields = ['user']
    can_delete = False
    verbose_name = 'Linked User'
    verbose_name_plural = 'Linked Users'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'schema_name', 'created_on', 'user_count']
    inlines = [DomainInLineAdmin, TenantUserInlineAdmin]

    def user_count(self, obj):
        return obj.tenant_users.count()
    user_count.short_description = 'Users'


# ── Landing Page admin ────────────────────────────────────────

class LandingFeatureInline(admin.TabularInline):
    model = LandingFeature
    extra = 0
    fields = [
        'sort_order', 'icon',
        'title', 'title_az', 'title_ru',
        'description', 'description_az', 'description_ru',
    ]
    ordering = ['sort_order']


class LandingStepInline(admin.TabularInline):
    model = LandingStep
    extra = 0
    fields = [
        'sort_order', 'number',
        'title', 'title_az', 'title_ru',
        'description', 'description_az', 'description_ru',
    ]
    ordering = ['sort_order']


@admin.register(LandingPage)
class LandingPageAdmin(admin.ModelAdmin):
    inlines = [LandingFeatureInline, LandingStepInline]

    fieldsets = [
        ('Hero Section — EN', {
            'fields': [
                'hero_badge', 'hero_title', 'hero_title_em',
                'hero_subtitle', 'hero_btn_primary', 'hero_btn_secondary',
            ],
        }),
        ('Hero Section — AZ', {
            'classes': ['collapse'],
            'fields': [
                'hero_badge_az', 'hero_title_az', 'hero_title_em_az',
                'hero_subtitle_az', 'hero_btn_primary_az', 'hero_btn_secondary_az',
            ],
        }),
        ('Hero Section — RU', {
            'classes': ['collapse'],
            'fields': [
                'hero_badge_ru', 'hero_title_ru', 'hero_title_em_ru',
                'hero_subtitle_ru', 'hero_btn_primary_ru', 'hero_btn_secondary_ru',
            ],
        }),
        ('Features Section — EN', {
            'fields': ['features_label', 'features_title', 'features_subtitle'],
        }),
        ('Features Section — AZ', {
            'classes': ['collapse'],
            'fields': ['features_label_az', 'features_title_az', 'features_subtitle_az'],
        }),
        ('Features Section — RU', {
            'classes': ['collapse'],
            'fields': ['features_label_ru', 'features_title_ru', 'features_subtitle_ru'],
        }),
        ('"How It Works" Section — EN', {
            'fields': ['steps_label', 'steps_title', 'steps_subtitle'],
        }),
        ('"How It Works" Section — AZ', {
            'classes': ['collapse'],
            'fields': ['steps_label_az', 'steps_title_az', 'steps_subtitle_az'],
        }),
        ('"How It Works" Section — RU', {
            'classes': ['collapse'],
            'fields': ['steps_label_ru', 'steps_title_ru', 'steps_subtitle_ru'],
        }),
        ('Call-to-Action Section — EN', {
            'fields': ['cta_title', 'cta_subtitle', 'cta_btn'],
        }),
        ('Call-to-Action Section — AZ', {
            'classes': ['collapse'],
            'fields': ['cta_title_az', 'cta_subtitle_az', 'cta_btn_az'],
        }),
        ('Call-to-Action Section — RU', {
            'classes': ['collapse'],
            'fields': ['cta_title_ru', 'cta_subtitle_ru', 'cta_btn_ru'],
        }),
        ('Footer — EN', {
            'fields': ['footer_text'],
        }),
        ('Footer — AZ / RU', {
            'classes': ['collapse'],
            'fields': ['footer_text_az', 'footer_text_ru'],
        }),
    ]

    def has_add_permission(self, request):
        # Only allow one instance
        return not LandingPage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        """Redirect the list view straight to the single object."""
        from django.shortcuts import redirect
        obj, _ = LandingPage.objects.get_or_create(pk=1)
        return redirect(f'/admin/public/landingpage/{obj.pk}/change/')
