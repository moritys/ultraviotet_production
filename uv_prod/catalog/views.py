from django.shortcuts import render

from catalog.models import Component


def catalog(request):
    template_name = 'catalog.html'
    component_list = Component.objects.values(
        'name', 'quantity', 'critical_quantity'
    )
    context = {
        'component_list': component_list,
    }
    return render(request, template_name, context)
