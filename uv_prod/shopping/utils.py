from production.models import Production, StageComponentBoardQuantity, Stage


def document_is_new(document):
    if document.is_done:
        return False

    initial_stage = Stage.objects.all().order_by('order').first()
    work_stages = Stage.objects.all().order_by('order')[1:]

    initial_production = Production.objects.filter(
        document=document, stage=initial_stage
    ).first()

    if not initial_production or initial_production.quantity == 0:
        return False

    for stage in work_stages:
        work_production = Production.objects.filter(
            document=document, stage=stage
        ).first()
        if work_production and work_production.quantity != 0:
            return False

    return True


def calculate_components_for_document(document):
    """
    Функция для подсчета количества компонентов
    для каждого нового документа по схеме.
    """
    board_quantities = {
        'central': document.central_q or 0,
        'facial': document.facial_q or 0,
        'round': document.round_q or 0,
        'indicator': document.indicator_q or 0,
    }
    components_quantity = {}

    ordered_boards = {
        board: quantity for board, quantity in board_quantities.items() if quantity > 0  # noqa
    }

    for board, quantity in ordered_boards.items():
        schemes = StageComponentBoardQuantity.objects.filter(
            board__slug=board,
            component__isnull=False
        )

        for scheme in schemes:
            component = scheme.component

            if component not in components_quantity:
                components_quantity[component] = {
                    'calculated': 0,
                    'stock': component.quantity
                }

            components_quantity[component]['calculated'] += (
                scheme.quantity * quantity
            )

    return components_quantity
