from django.shortcuts import get_object_or_404

from production.models import (
    Stage, Production, StageComponentBoardQuantity
)
from catalog.models import Component


def decrease_component_quantity(
        current_production: Production,
        current_quantity: int
):
    '''
    Списывает компоненты со склада.
    - current_production: объект модели Production (текущее производство),
    для которого нужно списать компоненты;
    - current_quantity: количество плат в данном этапе;

    1. Сначала находит схему/схемы списания по текущему этапу
    2. Далее для каждой схемы (если в ней используется компонент)
    находит компонент в базе
    3. Уменьшает количество компонента в базе по формуле:
    новое_кол-во = старое_кол-во - (кол-во_в_схеме * кол-во_плат)
    4. Сохраняет новое количество.
    '''
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


def decrease_previous_stage_quantity(
        current_production: Production,
        current_quantity: int
):
    '''
    Переводит платы из предыдущего этапа.
    - current_production: объект модели Production (текущее производство);
    - current_quantity: количество плат в данном этапе;

    1. Списывает компоненты со склада по схеме
    2. Находит объект модели предыдущего этапа
    (используется поле order в модели этапа)
    3. Если предыдущий этап есть в БД,
    то ищет объект производства для этого этапа
    4. Если такой этап найден, то
    4.1. Пытается у предыдущего этапа производства уменьшить количество плат
    на количество плат в текущем этапе. Сохраняет изменения
    4.2. Если не удается уменьшить количество плат в предыдущем этапе
    (например, юзер ввел число больше и получается отрицательное значение),
    то изменения не сохраняются и в лог выводится ошибка. Возвращается False
    5. Если исключений не возникло, то возвращается True.
    '''
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
            except Exception as ex:
                print(
                    'В предыдущем статусе нет плат: '
                    f'{ex}'
                )
                return False
    return True
