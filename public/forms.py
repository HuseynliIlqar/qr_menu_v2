import re

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

RESERVED_SUBDOMAINS = {'public', 'www', 'admin', 'api', 'mail', 'static', 'localhost', 'dashboard', 'media'}


class RegisterForm(forms.Form):
    restaurant_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'My Restaurant'}),
        label='Restaurant Name',
    )
    subdomain = forms.CharField(
        max_length=32,
        widget=forms.TextInput(attrs={'placeholder': 'myrestaurant', 'id': 'id_subdomain'}),
        label='Subdomain',
        help_text='Lowercase letters, numbers and hyphens only. Min 2 characters.',
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'johndoe', 'autocomplete': 'username'}),
        label='Username',
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com', 'autocomplete': 'email'}),
        label='Email',
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'autocomplete': 'new-password'}),
        label='Password',
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'autocomplete': 'new-password'}),
        label='Confirm Password',
    )

    def clean_subdomain(self):
        from public.models import Client
        sub = self.cleaned_data['subdomain'].lower().strip()
        if not re.match(r'^[a-z0-9][a-z0-9\-]*[a-z0-9]$', sub) and not re.match(r'^[a-z0-9]{2}$', sub):
            raise forms.ValidationError('Only lowercase letters, numbers, and hyphens. Min 2 chars.')
        if sub in RESERVED_SUBDOMAINS:
            raise forms.ValidationError('This subdomain is reserved. Please choose another.')
        if Client.objects.filter(schema_name=sub).exists():
            raise forms.ValidationError('This subdomain is already taken.')
        return sub

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Passwords do not match.')
        return cleaned


class PublicLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'autocomplete': 'username', 'autofocus': True}),
        label='Username',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'autocomplete': 'current-password'}),
        label='Password',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = None

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get('username')
        password = cleaned.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Invalid username or password.')
            if not user.is_active:
                raise forms.ValidationError('This account is disabled.')
            self._user = user
        return cleaned

    def get_user(self):
        return self._user
