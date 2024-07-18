from django.urls import path

from . import views

app_name = 'production'

urlpatterns = [
    path('', views.production, name='production'),
    # path(
    #     'board_data/',
    #     views.board_data,
    #     name='board_data'
    # ),
    path(
        '<int:number>/<slug:slug>/update_quantity/',
        views.update_quantity,
        name='update_quantity'
    ),
    path(
        '<int:number>/<slug:slug>/',
        views.board_production,
        name='board_production'
    ),
    path(
        '<int:number>/',
        views.document_production,
        name='document_production'
    ),
]
