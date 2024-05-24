from django.shortcuts import get_object_or_404, render

from production.models import Board, Production, StageComponentBoardQuantity


def production(request):
    template_name = 'production/production.html'
    board_list = Board.objects.all()
    for board in board_list:
        production_quantity = 0
        production_data = Production.objects.filter(board=board)

        for production_instance in production_data:
            production_quantity += production_instance.quantity

        board.total_production_quantity = production_quantity
    context = {
        'board_list': board_list,
    }
    return render(request, template_name, context)


def board_production(request, slug):
    template_name = 'production/board-base.html'
    board = get_object_or_404(Board, slug=slug)
    board_list = Board.objects.all()
    production_quantity = 0
    production_data = Production.objects.filter(board=board)

    for production_instance in production_data:
        production_quantity += production_instance.quantity

    board.total_production_quantity = production_quantity

    combined_data = []

    for stage in StageComponentBoardQuantity.objects.filter(board=board):
        production = Production.objects.filter(
            board=board, stage=stage.stage
        ).first()
        if production:
            quantity = production.quantity
        else:
            quantity = 0
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
    return render(request, template_name, context)
