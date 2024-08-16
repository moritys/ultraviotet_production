from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    Document, Production, Board, StageComponentBoardQuantity
)


def create_production_for_document(document):
    board_quantities = {
        'central': document.central_q,
        'facial': document.facial_q,
        'round': document.round_q,
        'indicator': document.indicator_q,
    }
    print(board_quantities)

    for board_slug, quantity in board_quantities.items():
        if quantity:
            try:
                board = Board.objects.get(slug=board_slug)
                stages = StageComponentBoardQuantity.objects.filter(
                    board=board
                ).order_by('stage__order')
                initial_stage = stages.first().stage

                Production.objects.create(
                    board=board,
                    stage=initial_stage,
                    quantity=quantity,
                    document=document
                )

                for stage in stages.exclude(id=initial_stage.id):
                    Production.objects.get_or_create(
                        board=board,
                        stage=stage.stage,
                        defaults={'quantity': 0},
                        document=document
                    )
            except Board.DoesNotExist:
                pass
            except Exception:
                pass


@receiver(post_save, sender=Document)
def handle_new_document(sender, instance, created, **kwargs):
    if created:
        create_production_for_document(instance)
