from django.urls import path

from . import views

app_name = 'production'

urlpatterns = [
    path('', views.production, name='production'),
    path(
        'board_data/',
        views.board_data,
        name='board_data'
    ),
    path(
        '<slug:slug>/update_quantity/',
        views.update_quantity,
        name='update_quantity'
    ),
    path('<slug:slug>/', views.board_production, name='board_production'),
]
