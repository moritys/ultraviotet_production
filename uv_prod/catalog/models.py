from django.db import models


class Component(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название',
        help_text='Уникальное название компонента, не более 50 символов'
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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Компонент'
        verbose_name_plural = 'Компоненты'
