from django.db import models

from catalog.models import Component


class Board(models.Model):
    '''
    Модель платы.
    - name: название платы (круглая, центральная, ...);
    - slug: уникальный слаг платы для создания url (round, central, ...);
    '''
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
    '''
    Модель этапа производства.
    - name: название этапа;
    - order: порядок этапа (чем меньше цифра, тем выше он в списке),
    !важный параметр, в зависимости от него плата переплывает
    !из предыдущего этапа;
    - cable_stage: является ли этап работой со шлейфами;
    '''
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


class Document(models.Model):
    number = models.PositiveSmallIntegerField(
        verbose_name='Номер приложения',
        help_text='Номер приложения по докам'
    )
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        verbose_name='Плата'
    )
    board_quantity = models.PositiveIntegerField(
        verbose_name='Количество заказанных плат',
        help_text='Сколько конкретно данных плат заказано'
    )

    def __str__(self) -> str:
        return f'Приложение {self.number}'

    class Meta:
        ordering = ('number',)
        verbose_name = 'Приложение'
        verbose_name_plural = 'Приложения'


class Production(models.Model):
    '''
    Модель производства.
    Учитывает количество плат в каждом этапе производства.
    Отображается на странице производства.
    Её меняет юзер и через неё списываются компоненты.
    - board: плата;
    - stage: текущий этап данной платы;
    - quantity: количество плат в данном этапе;
    '''
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
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        verbose_name='Номер прилы'
    )

    def __str__(self):
        return f'{self.board.name} - {self.stage.name} - {self.quantity}'

    class Meta:
        verbose_name = 'Текущее производство: статус и количество'
        verbose_name_plural = 'Текущее производство: статус и количество'


class StageComponentBoardQuantity(models.Model):
    '''
    Модель схемы производства.
    Содержит данные об использовании компонентов:
    отдельно для каждой платы, каждого этапа и компонента.
    На каждый этап может использоваться несколько компонентов,
    но связь плата + этап должна быть уникальной.
    - board: плата;
    - stage: этап;
    - component: компонент (может не быть);
    - quantity: количество компонента на этап (если компонента нет, то 0);
    '''
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        verbose_name='Плата'
    )
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
