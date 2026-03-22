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
    fields = ['sort_order', 'icon', 'title', 'description']
    ordering = ['sort_order']


class LandingStepInline(admin.TabularInline):
    model = LandingStep
    extra = 0
    fields = ['sort_order', 'number', 'title', 'description']
    ordering = ['sort_order']


@admin.register(LandingPage)
class LandingPageAdmin(admin.ModelAdmin):
    inlines = [LandingFeatureInline, LandingStepInline]

    fieldsets = [
        ('Hero Section', {
            'fields': [
                'hero_badge',
                'hero_title',
                'hero_title_em',
                'hero_subtitle',
                'hero_btn_primary',
                'hero_btn_secondary',
            ],
        }),
        ('Features Section', {
            'fields': ['features_label', 'features_title', 'features_subtitle'],
        }),
        ('"How It Works" Section', {
            'fields': ['steps_label', 'steps_title', 'steps_subtitle'],
        }),
        ('Call-to-Action Section', {
            'fields': ['cta_title', 'cta_subtitle', 'cta_btn'],
        }),
        ('Footer', {
            'fields': ['footer_text'],
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
