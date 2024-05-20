from django.db import models


class Component(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(
        blank=True, null=True, verbose_name='Описание'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество на складе'
    )
    critical_quantity = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Критическое количество, когда пора заказывать'
    )

    def __str__(self):
        return f'{self.name}, {self.quantity} шт. на складе'

    class Meta:
        verbose_name = 'Компонент'
        verbose_name_plural = 'Компоненты'
