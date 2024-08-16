from django.urls import path

from . import views

app_name = 'shopping'

urlpatterns = [
    path('', views.shopping, name='shopping'),
    path(
        'generate-excel-report/',
        views.generate_excel_report,
        name='generate_excel_report'
    ),
]
