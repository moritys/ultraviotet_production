from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.db.models import Sum

from production.models import (
    Board, Document, Production, Stage, StageComponentBoardQuantity
)
from production.forms import ProductionForm
from production.utils import decrease_previous_stage_quantity


def process_db_data(slug, doc_number):
    '''
    Функция для получения данных из БД.
    '''
    board = get_object_or_404(Board, slug=slug)
    document = get_object_or_404(Document, number=doc_number, board=board)
    board_list = Board.objects.values('slug', 'name')
    production_data = Production.objects.filter(
        board=board, document=document
    )

    combined_data = []
    stage_components = StageComponentBoardQuantity.objects.filter(
        board=board, document=document
    ).order_by('stage__order').select_related('stage')

    for stage in stage_components:
        production = production_data.filter(stage=stage.stage).first()
        quantity = production.quantity if production else 0
        combined_data.append(
            {
                'production_id': production.id if production else 0,
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


def process_production_form(request, board, stage, document):
    '''
    Функция для обработки формы.
    '''
    if request.method == 'POST':
        form = ProductionForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            existing_production = Production.objects.filter(
                board__name=form.cleaned_data['hidden_board'],
                stage__name=form.cleaned_data['hidden_stage'],
                document__number=form.changed_data['hidden_document']
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
                production.document = Document.objects.get(
                    number=form.cleaned_data['hidden_document']
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
            'hidden_document': document
        })
    return form


def get_production_quantity():
    '''
    Функция для подсчета количества каждой платы для каждого документа.
    нужно взять все строки производства
    для каждого документа
    и для каждой платы
    и суммировать количество
    '''

    productions = Production.objects.all()
    summary_dict = {}

    for production in productions:
        document_number = production.document.number
        board = production.board
        quantity = production.quantity
        if document_number not in summary_dict:
            summary_dict[document_number] = {}
        if board not in summary_dict[document_number]:
            summary_dict[document_number][board] = 0
        summary_dict[document_number][board] += quantity

    return summary_dict


def production(request):
    '''Функция общей страницы производства.'''
    template_name = 'production/production.html'

    documents = Document.objects.filter(is_done=False)
    data = []

    for document in documents:
        boards = Production.objects.filter(
            document=document
        ).values('board__name').annotate(total_quantity=Sum('quantity'))
        data.append({
            'document': document,
            'boards': boards
        })

    context = {'data': data}
    board = 'Круглая'
    stage = 'Сокращение зп'
    form = process_production_form(request, board, stage)
    context['form'] = form
    return render(request, template_name, context)


def board_production(request, number, slug):
    '''Функция конкретной страницы производства.'''
    template_name = 'production/board-base.html'

    context = process_db_data(slug, number)

    board = context['board']
    stage = 'Сокращение зп'
    form = process_production_form(request, board, stage)
    context['form'] = form

    return render(request, template_name, context)


def update_quantity(request, slug, number):
    '''
    Функция для обновления данных по количеству
    на странице конкретной платы через ajax.
    '''
    production_data_cabel = Production.objects.filter(
        stage__cable_stage=True, board__slug=slug
    )
    production_data_not_cabel = Production.objects.filter(
        stage__cable_stage=False, board__slug=slug
    )
    db_data = process_db_data(slug, number)
    board_name = db_data['board'].name
    board_total_quantity = db_data['total_quantity']

    data = {
        'production_data_cabel': [{
            'id': production.id,
            'board': production.board.name,
            'stage': production.stage.name,
            'quantity': production.quantity,
        } for production in production_data_cabel],
        'production_data_not_cabel': [{
            'id': production.id,
            'board': production.board.name,
            'stage': production.stage.name,
            'quantity': production.quantity,
        } for production in production_data_not_cabel],
        'production_count': {
            'name': board_name,
            'total_quantity': board_total_quantity
        }
    }
    return JsonResponse(data)


def board_data(request):
    '''
    Функция для обновления данных по количеству
    на общей странице производства через ajax.
    '''
    board_list = Board.objects.values('id', 'slug', 'name')
    production_data = Production.objects.select_related(
        'board'
    ).values('board__slug', 'quantity')

    get_production_quantity(board_list, production_data)
    data = {
        'board_data': [{
            'id': board['id'],
            'board': board['name'],
            'total_production_quantity': board['total_production_quantity'],
        } for board in board_list],
    }

    return JsonResponse(data)
