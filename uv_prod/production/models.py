from django.db import models

from catalog.models import Component


class Board(models.Model):
    name = models.CharField(max_length=30)


class Stage(models.Model):
    name = models.CharField(max_length=100)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    component = models.ManyToManyField(
        Component, through='StageComponentQuantity'
    )

    def __str__(self):
        return self.name


class Production(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class StageComponentQuantity(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('component', 'stage')
