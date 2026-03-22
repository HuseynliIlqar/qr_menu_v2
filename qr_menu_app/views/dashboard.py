from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.views import LoginView
from django.core import signing

from qr_menu_app.models import MainSectionModel, MenuItem
from qr_menu_app.forms import (
    RestaurantForm,
    MenuItemForm,
    SliderFormSet,
    SocialFormSet,
    InfoFormSet,
    GalleryFormSet,
    CategoryFormSet,
)

LOGIN = '/dashboard/login/'


# ──────────────────────────────────────────────────
#  Tenant-aware auth
# ──────────────────────────────────────────────────

def tenant_required(view_func):
    """Requires the user to be logged in AND belong to this tenant."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(LOGIN)
        if not request.user.is_superuser:
            from public.models import TenantUser
            if not TenantUser.objects.filter(user=request.user, tenant=request.tenant).exists():
                auth_logout(request)
                return redirect(LOGIN)
        return view_func(request, *args, **kwargs)
    return _wrapped


class TenantLoginView(LoginView):
    """Standard LoginView that also checks the user belongs to this tenant."""
    template_name = 'dashboard/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_superuser:
            from public.models import TenantUser
            if not TenantUser.objects.filter(user=user, tenant=self.request.tenant).exists():
                form.add_error(None, 'This account does not have access to this restaurant.')
                return self.form_invalid(form)
        return super().form_valid(form)


def auto_login(request):
    """
    Verifies a short-lived signed token (generated on the public domain after
    register/login) and logs the user into this tenant's session.
    """
    token = request.GET.get('token', '')
    try:
        data = signing.loads(token, salt='tenant-auto-login', max_age=300)
        User = get_user_model()
        user = User.objects.get(pk=data['user_id'])
        if not user.is_superuser:
            from public.models import TenantUser
            if not TenantUser.objects.filter(user=user, tenant=request.tenant).exists():
                messages.error(request, 'Access denied.')
                return redirect(LOGIN)
        auth_login(request, user)
        return redirect('/dashboard/')
    except Exception:
        return redirect(LOGIN)


# ──────────────────────────────────────────────────
#  Helpers
# ──────────────────────────────────────────────────

def _get_main():
    """Return the single MainSectionModel instance or None."""
    return MainSectionModel.objects.first()


# ──────────────────────────────────────────────────
#  Dashboard Home
# ──────────────────────────────────────────────────

@tenant_required
def dashboard_home(request):
    main = _get_main()
    context = {'main': main, 'page_title': 'Dashboard Overview'}
    if main:
        context.update({
            'slider_count': main.index_slider_photos.count(),
            'social_count': main.social_media_icons.count(),
            'info_count': main.info_sections.count(),
            'gallery_count': main.restoran_galery_photos.count(),
            'category_count': main.item_categories.count(),
            'menu_count': MenuItem.objects.count(),
        })
    return render(request, 'dashboard/home.html', context)


# ──────────────────────────────────────────────────
#  Restaurant / Main Section
# ──────────────────────────────────────────────────

@tenant_required
def edit_restaurant(request):
    main = _get_main()
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES, instance=main)
        if form.is_valid():
            form.save()
            messages.success(request, 'Restaurant information saved successfully.')
            return redirect('dashboard:restaurant')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RestaurantForm(instance=main)

    return render(request, 'dashboard/restaurant.html', {
        'form': form,
        'main': main,
        'page_title': 'Restaurant Info',
    })


# ──────────────────────────────────────────────────
#  Hero Sliders
# ──────────────────────────────────────────────────

@tenant_required
def edit_sliders(request):
    main = _get_main()
    if request.method == 'POST':
        formset = SliderFormSet(request.POST, request.FILES, instance=main)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Sliders saved successfully.')
            return redirect('dashboard:sliders')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        formset = SliderFormSet(instance=main)

    return render(request, 'dashboard/sliders.html', {
        'formset': formset,
        'main': main,
        'page_title': 'Hero Sliders',
    })


# ──────────────────────────────────────────────────
#  Social Media
# ──────────────────────────────────────────────────

@tenant_required
def edit_social(request):
    main = _get_main()
    if request.method == 'POST':
        formset = SocialFormSet(request.POST, request.FILES, instance=main)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Social media links saved successfully.')
            return redirect('dashboard:social')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        formset = SocialFormSet(instance=main)

    return render(request, 'dashboard/social.html', {
        'formset': formset,
        'main': main,
        'page_title': 'Social Media',
    })


# ──────────────────────────────────────────────────
#  Info Strip
# ──────────────────────────────────────────────────

@tenant_required
def edit_info(request):
    main = _get_main()
    if request.method == 'POST':
        formset = InfoFormSet(request.POST, request.FILES, instance=main)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Info sections saved successfully.')
            return redirect('dashboard:info')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        formset = InfoFormSet(instance=main)

    return render(request, 'dashboard/info.html', {
        'formset': formset,
        'main': main,
        'page_title': 'Info Strip',
    })


# ──────────────────────────────────────────────────
#  Gallery
# ──────────────────────────────────────────────────

@tenant_required
def edit_gallery(request):
    main = _get_main()
    if request.method == 'POST':
        formset = GalleryFormSet(request.POST, request.FILES, instance=main)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Gallery photos saved successfully.')
            return redirect('dashboard:gallery')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        formset = GalleryFormSet(instance=main)

    return render(request, 'dashboard/gallery.html', {
        'formset': formset,
        'main': main,
        'page_title': 'Restaurant Gallery',
    })


# ──────────────────────────────────────────────────
#  Categories
# ──────────────────────────────────────────────────

@tenant_required
def edit_categories(request):
    main = _get_main()
    if request.method == 'POST':
        formset = CategoryFormSet(request.POST, request.FILES, instance=main)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Categories saved successfully.')
            return redirect('dashboard:categories')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        formset = CategoryFormSet(instance=main)

    return render(request, 'dashboard/categories.html', {
        'formset': formset,
        'main': main,
        'page_title': 'Menu Categories',
    })


# ──────────────────────────────────────────────────
#  Menu Items
# ──────────────────────────────────────────────────

@tenant_required
def menu_list(request):
    items = MenuItem.objects.prefetch_related('category').order_by('-create_at')
    return render(request, 'dashboard/menu_list.html', {
        'items': items,
        'page_title': 'Menu Items',
    })


@tenant_required
def menu_add(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item added successfully.')
            return redirect('dashboard:menu_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = MenuItemForm()

    return render(request, 'dashboard/menu_form.html', {
        'form': form,
        'page_title': 'Add Menu Item',
        'action_label': 'Add Item',
    })


@tenant_required
def menu_edit(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{item.name}" updated successfully.')
            return redirect('dashboard:menu_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = MenuItemForm(instance=item)

    return render(request, 'dashboard/menu_form.html', {
        'form': form,
        'item': item,
        'page_title': f'Edit — {item.name}',
        'action_label': 'Save Changes',
    })


@tenant_required
def menu_delete(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        name = item.name
        item.delete()
        messages.success(request, f'"{name}" deleted.')
    return redirect('dashboard:menu_list')
