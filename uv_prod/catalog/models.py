from django.db import models


class Component(models.Model):
    name = models.CharField(max_length=50, verbose_name='')
    description = models.TextField(blank=True, null=True, verbose_name='')
    quantity = models.PositiveIntegerField(verbose_name='')
    critical_quantity = models.PositiveIntegerField(blank=True, null=True, verbose_name='')

    def __str__(self):
        return f'{self.name}, {self.quantity} шт. на складе'

    class Meta:
        verbose_name = 'Компонент'
        verbose_name_plural = 'Компоненты'
