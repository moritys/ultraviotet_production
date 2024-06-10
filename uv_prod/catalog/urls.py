from django.urls import path

from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('catalog-data/', views.catalog_data, name='catalog_data'),
]
