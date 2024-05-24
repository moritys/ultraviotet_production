from django.db import models

from catalog.models import Component


class Board(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name='Название',
        help_text='Уникальное название платы, не более 30 символов'
    )
    slug = models.SlugField(
        max_length=30,
        verbose_name='Слаг',
        help_text='Уникальный слаг платы, не более 30 символов'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Плата'
        verbose_name_plural = 'Платы'


class Stage(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Уникальное название этапа, не более 256 символов'
    )
    order = models.PositiveSmallIntegerField(
        verbose_name='Порядок этапа',
        help_text='Порядок выполнения этапов, от 1 до бесконечности'
    )
    cable_stage = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('order',)
        verbose_name = 'Этап производства'
        verbose_name_plural = 'Этапы производства'


class Production(models.Model):
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        verbose_name='Плата'
    )
    stage = models.ForeignKey(
        Stage,
        on_delete=models.CASCADE,
        verbose_name='Этап производства'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество на этапе',
        help_text='Количество заданных плат на этом этапе'
    )

    def __str__(self):
        return f'{self.board.name} - {self.stage.name} - {self.quantity}'

    class Meta:
        verbose_name = 'Текущее производство: статус и количество'
        verbose_name_plural = 'Текущее производство: статус и количество'


class StageComponentBoardQuantity(models.Model):
    stage = models.ForeignKey(
        Stage,
        on_delete=models.CASCADE,
        verbose_name='Этап'
    )
    component = models.ForeignKey(
        Component,
        blank=True, null=True,
        on_delete=models.CASCADE,
        verbose_name='Компонент'
    )
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        verbose_name='Плата'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество компонента на этап'
    )

    class Meta:
        unique_together = ('stage', 'board')
        verbose_name = 'Схема: Связь этапа и количества компонентов'
        verbose_name_plural = 'Схема: Связь этапа и количества компонентов'

    def __str__(self):
        if self.component:
            return (
                f'{self.board.name} | {self.stage.name}: '
                f'{self.component.name}, {self.quantity} шт.'
            )
        return (
                f'{self.board.name} | {self.stage.name}: '
                f'без компонентов'
            )
