from django.http import JsonResponse
from django.shortcuts import render

from .models import Component


def catalog(request):
    template_name = 'catalog.html'

    return render(request, template_name)


def catalog_data(request):
    catalog_data = Component.objects.all()

    data = {
        'catalog_data': [{
            'name': component.name,
            'quantity': component.quantity,
            'critical_quantity': component.critical_quantity,
            'description': component.description,
            'part_number': component.part_number,
        } for component in catalog_data]
    }

    return JsonResponse(data)
