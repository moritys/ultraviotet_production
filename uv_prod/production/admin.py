from django.contrib import admin

from .models import Board, Production, Stage, StageComponentBoardQuantity


class StageComponentBoardQuantityInline(admin.TabularInline):
    model = StageComponentBoardQuantity


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


class StageAdmin(admin.ModelAdmin):
    inlines = [
        StageComponentBoardQuantityInline,
    ]


admin.site.register(Board)
admin.site.register(Stage, StageAdmin)
admin.site.register(StageComponentBoardQuantity)
admin.site.register(Production, ProductionAdmin)
