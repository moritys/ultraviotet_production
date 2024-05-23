from django.shortcuts import get_object_or_404, render

from production.models import Board, Production, StageComponentBoardQuantity


def production(request):
    template_name = 'production/production.html'

    board_list = Board.objects.all()

    round_production_list = Production.objects.filter(
        board__name__contains='Круглая'
    )
    indicator_production_list = Production.objects.filter(
        board__name__contains='Индикаторная'
    )
    central_production_list = Production.objects.filter(
        board__name__contains='Центральная'
    )
    facial_production_list = Production.objects.filter(
        board__name__contains='Лицевая'
    )

    round_scheme_list = StageComponentBoardQuantity.objects.filter(
        board__name__contains='Круглая'
    )
    indicator_scheme_list = StageComponentBoardQuantity.objects.filter(
        board__name__contains='Индикаторная'
    )
    central_scheme_list = StageComponentBoardQuantity.objects.filter(
        board__name__contains='Центральная'
    )
    facial_scheme_list = StageComponentBoardQuantity.objects.filter(
        board__name__contains='Лицевая'
    )

    context = {
        'board_list': board_list,
        'round_production_list': round_production_list,
        'indicator_production_list': indicator_production_list,
        'central_production_list': central_production_list,
        'facial_production_list': facial_production_list,
        'round_scheme_list': round_scheme_list,
        'indicator_scheme_list': indicator_scheme_list,
        'central_scheme_list': central_scheme_list,
        'facial_scheme_list': facial_scheme_list,
    }
    return render(request, template_name, context)


def board_production(request, slug):
    template_name = 'production/board-base.html'
    board = get_object_or_404(Board, slug=slug)
    board_list = Board.objects.all()

    board_scheme_list = StageComponentBoardQuantity.objects.filter(
        board=board
    )
    board_production_list = Production.objects.filter(
        board=board
    )

    context = {
        'board_scheme_list': board_scheme_list,
        'board_production_list': board_production_list,
        'board_list': board_list,
        'slug': slug,
        'board': board,
    }
    return render(request, template_name, context)
