from django.urls import path

from . import views

app_name = 'production'

urlpatterns = [
    path('', views.production, name='production'),
]
