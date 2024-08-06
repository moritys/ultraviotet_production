from django.db import models


class Component(models.Model):
    name = models.CharField(
        unique=True,
        max_length=50,
        verbose_name='Название',
        help_text='Схема названия: "Part | Footprint"'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
        help_text='Не обязательное поле, описание'
    )
    quantity = models.IntegerField(
        verbose_name='Количество на складе'
    )
    critical_quantity = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Критическое количество',
        help_text='Когда уже пора заказывать'
    )
    part_number = models.CharField(
        max_length=50,
        verbose_name='Номер партии',
        help_text='Пример: "CL10B104KB8NNNC"'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Компонент'
        verbose_name_plural = 'Компоненты'
