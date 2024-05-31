from production.models import Board, Stage, Production, StageComponentBoardQuantity
from catalog.models import Component


def decrease_previous_stage_quantity(current_production, current_quantity):
    previous_stage = Stage.objects.filter(
        order=current_production.stage.order - 1
    ).first()
    if previous_stage:
        previous_production = Production.objects.filter(
            board=current_production.board, stage=previous_stage
        ).first()
        if previous_production:
            previous_production.quantity -= current_quantity
            previous_production.save()



# находим схему для плата + этап
# достаем оттуда компоненты (все которые есть)
# списываем из каталога кол-во комп-в * кол-во плат