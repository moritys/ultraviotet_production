from production.models import Production, StageComponentBoardQuantity, Stage


def document_is_new(document):
    initial_stage = Stage.objects.all().order_by('order').first()

    if not document.is_done:
        new_doc = Production.objects.filter(
            document=document, stage=initial_stage
        )
        if new_doc.exists():
            return True

    return False


def calculate_components_for_document(document):
    '''
    нужно умножать не на production.quantity
    а на количество плат в статусе новый заказ
    '''
    productions = Production.objects.filter(document=document)
    initial_stage = Stage.objects.all().order_by('order').first()
    components_quantity = {}

    for production in productions:
        schemes = StageComponentBoardQuantity.objects.filter(
            board=production.board, stage=production.stage, component__isnull=False
        )
        
        initial_quantity = 

        for scheme in schemes:
            if scheme.component not in components_quantity:
                components_quantity[scheme.component] = 0
            components_quantity[scheme.component] += (
                scheme.quantity * production.quantity
            )
            print(f"Document: {document}, Component: {scheme.component}, Quantity: {components_quantity[scheme.component]}")

    return components_quantity
