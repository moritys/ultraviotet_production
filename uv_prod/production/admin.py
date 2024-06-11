from django.contrib import admin

from .models import (
    Board, Document, Production, Stage, StageComponentBoardQuantity
)


class ProductionAdmin(admin.ModelAdmin):
    list_display = (
        'board',
        'stage',
        'quantity',
        'document',
    )
    list_editable = (
        'quantity',
        'document',
    )
    search_fields = ('board', 'document',)
    list_filter = ('stage', 'document',)
    list_display_links = ('board',)


class BoardAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    list_editable = (
        'slug',
    )
    list_display_links = ('name',)


class StageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'order',
        'cable_stage',
    )
    list_editable = (
        'order',
        'cable_stage',
    )
    search_fields = ('name',)
    list_filter = ('cable_stage',)
    list_display_links = ('name',)


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


class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'board',
        'board_quantity',
    )
    list_editable = (
        'board_quantity',
    )
    search_fields = ('number',)
    list_filter = ('board',)
    list_display_links = ('number',)


admin.site.register(Board, BoardAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(
    StageComponentBoardQuantity, StageComponentBoardQuantityAdmin
)
admin.site.register(Production, ProductionAdmin)
