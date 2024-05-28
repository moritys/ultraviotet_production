from django.shortcuts import render

from production.forms import ProductionForm


def shopping(request):
    template_name = 'shopping.html'
    form = ProductionForm()
    context = {
        'form': form,
    }
    return render(request, template_name, context)
