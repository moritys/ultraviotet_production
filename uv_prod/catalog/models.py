from django.db import models


class Component(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Board(models.Model):
    name = models.CharField(max_length=30)
    components = models.ManyToManyField(Component, through='ComponentQuantity')

    def __str__(self):
        return self.name


class ComponentQuantity(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    quantity_used = models.IntegerField()

    class Meta:
        unique_together = ('component', 'board')
