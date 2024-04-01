from django.db import models

from catalog.models import Component


class Stage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    components = models.ManyToManyField(
        Component, through='StageComponentQuantity'
    )

    def __str__(self):
        return self.name


class StageComponentQuantity(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    quantity_used = models.IntegerField()

    class Meta:
        unique_together = ('component', 'stage')
