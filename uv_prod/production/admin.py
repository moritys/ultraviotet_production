from django.contrib import admin

from .models import Board, Production, Stage, StageComponentsQuantity


admin.site.register(Board)
admin.site.register(Production)
admin.site.register(Stage)
admin.site.register(StageComponentsQuantity)
