from django.shortcuts import render

from production.models import Board, Production


def production(request):
    template_name = 'production/production.html'

    board_list = Board.objects.all()
    production_list = Production.objects.all()
    context = {
        'board_list': board_list,
        'production_list': production_list,
    }
    return render(request, template_name, context)
