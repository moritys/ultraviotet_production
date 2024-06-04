from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

from production.models import (
    Board, Production, Stage, StageComponentBoardQuantity
)
from production.forms import ProductionForm
from production.utils import decrease_previous_stage_quantity


def process_db_data(slug):
    '''
    Функция для получения данных из БД.
    '''
    board = get_object_or_404(Board, slug=slug)
    board_list = Board.objects.values('slug', 'name')
    production_data = Production.objects.filter(board=board)

    combined_data = []
    stage_components = StageComponentBoardQuantity.objects.filter(
        board=board
    ).select_related('stage')

    for stage in stage_components:
        production = production_data.filter(stage=stage.stage).first()
        quantity = production.quantity if production else 0
        combined_data.append(
            {
                'stage': stage.stage,
                'quantity': quantity,
                'cable': stage.stage.cable_stage,
            }
        )

    total_quantity = sum(data['quantity'] for data in combined_data)
    context = {
        'board_list': board_list,
        'slug': slug,
        'board': board,
        'combined_data': combined_data,
        'total_quantity': total_quantity,
    }
    return context


def process_production_form(request, board, stage):
    '''
    Функция для обработки формы.
    '''

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
                if decrease_previous_stage_quantity(
                    existing_production, quantity
                ):
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
                if decrease_previous_stage_quantity(
                    production, quantity
                ):
                    production.save()

        form = ProductionForm()
    else:
        form = ProductionForm(initial={
            'hidden_board': board,
            'hidden_stage': stage,
        })
    return form


def production(request):
    template_name = 'production/production.html'
    board_list = Board.objects.values('slug', 'name')
    production_data = Production.objects.select_related(
        'board'
    ).values('board__slug', 'quantity')

    for board in board_list:
        production_quantity = sum(
            data['quantity'] for data in production_data if (
                data['board__slug'] == board['slug'])
        )
        board['total_production_quantity'] = production_quantity
    context = {
        'board_list': board_list,
    }

    board = 'Круглая'
    stage = 'Сокращение зп'
    form = process_production_form(request, board, stage)
    context['form'] = form
    return render(request, template_name, context)


def board_production(request, slug):
    template_name = 'production/board-base.html'

    context = process_db_data(slug)

    board = context['board']
    stage = 'Сокращение зп'
    form = process_production_form(request, board, stage)
    context['form'] = form

    return render(request, template_name, context)


def production_data(request):
    production_data = Production.objects.all()

    data = {
        'production_data': [{
            'board': production.board.name,
            'stage': production.stage.name,
            'quantity': production.quantity,
        } for production in production_data]
    }

    return JsonResponse(data)
