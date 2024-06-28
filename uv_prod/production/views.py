from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.db.models import Sum

from production.models import (
    Board, Document, Production, Stage, StageComponentBoardQuantity
)
from production.forms import ProductionForm
from production.utils import decrease_previous_stage_quantity


def process_db_data(doc_number, slug):
    '''
    Функция для получения данных из БД.
    '''
    board = get_object_or_404(Board, slug=slug)
    document = get_object_or_404(Document, number=doc_number)

    board_list = Production.objects.filter(
        document=document
    ).values('board__slug', 'board__name').distinct()
    production_data = Production.objects.filter(
        board=board, document=document
    )
    document_list = Document.objects.all().values('number')

    combined_data = []
    stage_components = StageComponentBoardQuantity.objects.filter(
        board=board
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
        'slug': slug if slug else None,
        'document': document,
        'board': board,
        'combined_data': combined_data,
        'total_quantity': total_quantity,
        'document_list': document_list,
    }
    return context


def process_db_data_document(doc_number):
    '''
    Функция для получения данных из БД для приложения.
    '''
    document = get_object_or_404(Document, number=doc_number)

    board_list = Production.objects.filter(
        document=document
    ).values('board__slug', 'board__name').distinct()

    context = {
        'board_list': board_list,
        'document': document,
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
                document__number=form.cleaned_data['hidden_document']
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


def get_production_quantity(document_number=None):
    '''
    Функция для подсчета количества каждой платы для каждого документа.
    '''

    if document_number:
        documents = Document.objects.filter(
            number=document_number, is_done=False
        )
    else:
        documents = Document.objects.filter(is_done=False)
    data = []

    for document in documents:
        boards = Production.objects.filter(
            document=document
        ).values('board__slug', 'board__name', 'board__id').annotate(
            total_quantity=Sum('quantity')
        ).order_by('board__id')
        data.append({
            'document': document,
            'boards': boards
        })

    return {'data': data}


def production(request):
    '''Функция общей страницы производства.'''
    template_name = 'production/production.html'

    context = get_production_quantity()
    board = 'Круглая'
    stage = 'Сокращение зп'
    document = '1'
    form = process_production_form(request, board, stage, document)
    context['form'] = form
    context['document_list'] = Document.objects.all().values('number')
    return render(request, template_name, context)


def document_production(request, number):
    '''Функция для приложения.'''
    template_name = 'production/document.html'
    document_list = Document.objects.all().values('number')

    context = process_db_data_document(number)
    context['document_list'] = document_list

    return render(request, template_name, context)


def board_production(request, number, slug):
    '''Функция конкретной страницы производства для плат.'''
    template_name = 'production/board-base.html'

    context = process_db_data(number, slug)

    board = context['board']
    stage = 'Новый заказ'
    document = 1
    form = process_production_form(request, board, stage, document)
    context['form'] = form

    return render(request, template_name, context)


# def update_quantity(request, slug, number):
#     '''
#     Функция для обновления данных по количеству
#     на странице конкретной платы через ajax.
#     '''
#     production_data_cabel = Production.objects.filter(
#         stage__cable_stage=True, board__slug=slug
#     )
#     production_data_not_cabel = Production.objects.filter(
#         stage__cable_stage=False, board__slug=slug
#     )
#     db_data = process_db_data(number, slug)
#     board_name = db_data['board'].name
#     board_total_quantity = db_data['total_quantity']

#     data = {
#         'production_data_cabel': [{
#             'id': production.id,
#             'board': production.board.name,
#             'stage': production.stage.name,
#             'quantity': production.quantity,
#         } for production in production_data_cabel],
#         'production_data_not_cabel': [{
#             'id': production.id,
#             'board': production.board.name,
#             'stage': production.stage.name,
#             'quantity': production.quantity,
#         } for production in production_data_not_cabel],
#         'production_count': {
#             'name': board_name,
#             'total_quantity': board_total_quantity
#         }
#     }
#     return JsonResponse(data)


# def board_data(request):
#     '''
#     Функция для обновления данных по количеству
#     на общей странице производства через ajax.
#     '''
#     document_number = request.GET.get('document_number')
#     data = get_production_quantity(document_number)

#     board_list = []
#     for document_data in data['data']:
#         for board_data in document_data['boards']:
#             board_list.append(board_data)

#     data = {
#         'board_data': [{
#             'id': board['board__id'],
#             'board': board['board__name'],
#             'total_quantity': board['total_quantity'],
#         } for board in board_list],
#     }

#     return JsonResponse(data)
