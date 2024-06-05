from django.urls import path

from . import views

app_name = 'production'

urlpatterns = [
    path('', views.production, name='production'),
    path('production-data/', views.production_data, name='production_data'),
    path('<slug:slug>/', views.board_production, name='board_production'),
]
