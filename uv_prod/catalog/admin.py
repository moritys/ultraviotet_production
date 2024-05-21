from django.contrib import admin

from .models import Component


class ComponentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'quantity',
        'critical_quantity',
    )
    list_editable = (
        'quantity',
        'critical_quantity',
    )
    search_fields = ('name',)
    list_display_links = ('name',)


admin.site.register(Component)
