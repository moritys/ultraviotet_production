from django.shortcuts import render

from production.forms import ProductionForm
from production.models import Production, Board, Stage


def shopping(request):
    template_name = 'shopping.html'

    board = 'Круглая'
    stage = 'Сокращение зп'

    if request.method == 'POST':
        form = ProductionForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            existing_production = Production.objects.filter(
                board__name=form.cleaned_data['hidden_board'],
                stage__name=form.cleaned_data['hidden_stage']
            ).first()

            if existing_production:
                existing_production.quantity += quantity
                existing_production.save()
            else:
                production = Production()
                production.board = Board.objects.get(
                    name=form.cleaned_data['hidden_board']
                )
                production.stage = Stage.objects.get(
                    name=form.cleaned_data['hidden_stage']
                )
                production.quantity = quantity
                production.save()
    else:
        form = ProductionForm(initial={
            'hidden_board': board,
            'hidden_stage': stage
        })
    context = {
        'form': form,
    }
    return render(request, template_name, context)
