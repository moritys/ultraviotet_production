from catalog.models import Component
from django.db.models import F
from django.shortcuts import render


def index(request):
    template_name = 'index.html'
    component_list = Component.objects.values(
        'name', 'quantity', 'critical_quantity', 'description',
    ).filter(quantity__lte=F('critical_quantity'))
    context = {
        'component_list': component_list,
    }
    return render(request, template_name, context)
