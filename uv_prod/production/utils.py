from django.shortcuts import get_object_or_404

from production.models import (
    Stage, Production, StageComponentBoardQuantity
)
from catalog.models import Component


def decrease_component_quantity(current_production, current_quantity):
    schemes = StageComponentBoardQuantity.objects.filter(
        board=current_production.board,
        stage=current_production.stage
    )

    for scheme in schemes:
        if scheme.component:
            component = get_object_or_404(Component, name=scheme.component)
            component.quantity -= scheme.quantity * current_quantity
            component.save()
            if component.quantity < 0:
                print('Количество компонента меньше 0, кто то накосячил')


def decrease_previous_stage_quantity(current_production, current_quantity):
    decrease_component_quantity(current_production, current_quantity)
    previous_stage = Stage.objects.filter(
        order=current_production.stage.order - 1
    ).first()
    if previous_stage:
        previous_production = Production.objects.filter(
            board=current_production.board, stage=previous_stage
        ).first()
        if previous_production:
            try:
                previous_production.quantity -= current_quantity
                previous_production.save()
                return True
            except Exception as ex:
                print(
                    'В предыдущем статусе нет плат: '
                    f'{ex}'
                )
                return False
