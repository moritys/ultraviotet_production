from django.contrib import admin

from .models import Board, Production, Stage, StageComponentBoardQuantity


class ProductionAdmin(admin.ModelAdmin):
    list_display = (
        'board',
        'stage',
        'quantity',
    )
    list_editable = (
        'quantity',
    )
    search_fields = ('board',)
    list_filter = ('stage',)
    list_display_links = ('board',)


class StageComponentBoardQuantityAdmin(admin.ModelAdmin):
    list_display = (
        'board',
        'stage',
        'component',
        'quantity',
    )
    list_editable = (
        'quantity',
    )
    search_fields = ('board',)
    list_filter = ('stage', 'board',)
    list_display_links = ('board',)


admin.site.register(Board)
admin.site.register(Stage)
admin.site.register(
    StageComponentBoardQuantity, StageComponentBoardQuantityAdmin
)
admin.site.register(Production, ProductionAdmin)
