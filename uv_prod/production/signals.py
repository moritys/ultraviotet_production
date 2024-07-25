from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Document, Production, Board, Stage
from .utils import calculate_components_for_document


@receiver(post_save, sender=Document)
def create_production_for_document(sender, instance, created, **kwargs):
    if created:
        board_quantities = {
            'central': instance.central_q,
            'facial': instance.facial_q,
            'round': instance.round_q,
            'indicator': instance.indicator_q,
        }

        initial_stage = Stage.objects.order_by('order').first()
        for board_slug, quantity in board_quantities.items():
            try:
                board = Board.objects.get(slug=board_slug)
                Production.objects.create(
                    board=board,
                    stage=initial_stage,
                    quantity=quantity,
                    document=instance
                )
            except Board.DoesNotExist:
                pass


@receiver(post_save, sender=Document)
def handle_new_document(sender, instance, created, **kwargs):
    if created:
        create_production_for_document(instance)

        components_quantity = calculate_components_for_document(instance)

        for component, quantity in components_quantity.items():
            pass
