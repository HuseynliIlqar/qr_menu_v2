from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core import signing
from decouple import config

from public.models import Client, Domain, TenantUser
from public.forms import RegisterForm, PublicLoginForm


def _tenant_url(request, domain_str, path):
    """Build full URL to a tenant domain, preserving the dev server port."""
    host = request.get_host()
    port = ':' + host.split(':')[1] if ':' in host else ''
    return f'http://{domain_str}{port}{path}'


def landing(request):
    from public.models import LandingPage
    page = LandingPage.load()
    return render(request, 'public/landing.html', {'page': page})


def register_view(request):
    base_domain = config('BASE_DOMAIN', default='localhost')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            subdomain = d['subdomain']

            # 1. Create tenant — auto_create_schema=True runs migrations automatically
            tenant = Client(schema_name=subdomain, name=d['restaurant_name'])
            tenant.save()

            # 2. Create primary domain
            domain_str = f'{subdomain}.{base_domain}'
            Domain.objects.create(domain=domain_str, tenant=tenant, is_primary=True)

            # 3. Create Django user
            user = User.objects.create_user(
                username=d['username'],
                email=d['email'],
                password=d['password1'],
            )

            # 4. Link user to tenant
            TenantUser.objects.create(user=user, tenant=tenant)

            # 5. Auto-login via signed token (5 min TTL)
            token = signing.dumps({'user_id': user.pk}, salt='tenant-auto-login')
            return redirect(_tenant_url(request, domain_str, f'/dashboard/auto-login/?token={token}'))
    else:
        form = RegisterForm()

    return render(request, 'public/register.html', {
        'form': form,
        'base_domain': base_domain,
    })


def login_view(request):
    if request.method == 'POST':
        form = PublicLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            try:
                tu = TenantUser.objects.select_related('tenant').get(user=user)
                domain = tu.tenant.domains.filter(is_primary=True).first()
                if not domain:
                    form.add_error(None, 'No domain configured for this account. Contact support.')
                else:
                    token = signing.dumps({'user_id': user.pk}, salt='tenant-auto-login')
                    return redirect(_tenant_url(request, domain.domain, f'/dashboard/auto-login/?token={token}'))
            except TenantUser.DoesNotExist:
                form.add_error(None, 'No restaurant account found for this user.')
    else:
        form = PublicLoginForm()

    return render(request, 'public/login.html', {'form': form})
