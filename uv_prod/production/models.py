from django.db import models

from catalog.models import Component


class Board(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Плата'
        verbose_name_plural = 'Платы'


class Stage(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    component = models.ManyToManyField(
        Component,
        through='StageComponentBoardQuantity',
        verbose_name='Компоненты и платы'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Этап производства'
        verbose_name_plural = 'Этапы производства'


class Production(models.Model):
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, verbose_name='Плата'
    )
    stage = models.ForeignKey(
        Stage, on_delete=models.CASCADE, verbose_name='Этап производства'
    )
    quantity = models.PositiveIntegerField(verbose_name='Количество на этапе')

    def __str__(self):
        return f'Производство: {self.quantity} {self.board}'

    class Meta:
        verbose_name = 'Текущее производство: статус и количество'
        verbose_name_plural = 'Текущее производство: статус и количество'


class StageComponentBoardQuantity(models.Model):
    stage = models.ForeignKey(
        Stage, on_delete=models.CASCADE, verbose_name='Этап'
    )
    component = models.ForeignKey(
        Component, on_delete=models.CASCADE, verbose_name='Компонент'
    )
    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, verbose_name='Плата'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество компонента на этап'
    )

    class Meta:
        unique_together = ('component', 'stage')
        verbose_name = 'Схема: Связь этапа и количества компонентов'
        verbose_name_plural = 'Схема: Связь этапа и количества компонентов'

    def __str__(self):
        return f'{self.board} | {self.stage}: {self.component}, {self.quantity} шт.'
