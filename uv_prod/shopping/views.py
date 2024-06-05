from django.shortcuts import render

from production.forms import ProductionForm
from production.models import Production, Board, Stage


def shopping(request):
    template_name = 'shopping.html'
    
    return render(request, template_name)
