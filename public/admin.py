from django.contrib import admin
from .models import Client, Domain

class DomainInLineAdmin(admin.TabularInline):
    model= Domain
    min_num =1
    max_num =1


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name','created_on']
    inlines = [DomainInLineAdmin]
