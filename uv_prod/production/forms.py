from django import forms

from django.core.exceptions import ValidationError

from production.models import Stage


class ProductionForm(forms.Form):
    quantity = forms.IntegerField(
        label='Количество плат',
        min_value=0,
        max_value=500_000,
        widget=forms.NumberInput(
            attrs={
                'class': 'input',
                'placeholder': '100',
            }
        )
    )
    hidden_board = forms.CharField(widget=forms.HiddenInput)
    hidden_stage = forms.CharField(widget=forms.HiddenInput)
    hidden_document = forms.CharField(widget=forms.HiddenInput)

    def clean_hidden_document(self):
        data = self.cleaned_data['hidden_document']
        try:
            return int(data)
        except ValueError:
            raise forms.ValidationError('Номер документа не число.')

    def clean(self):
        '''
        Проверка максимального количества.
        Работает только если в бд заведены записи производства.
        '''
        super().clean()
        hidden_stage = self.cleaned_data['hidden_stage']
        hidden_document = self.cleaned_data['hidden_document']
        hidden_stage_order = Stage.objects.get(name=hidden_stage).order

        quantity = self.cleaned_data['quantity']

        if hidden_stage:
            previous_stage = Stage.objects.filter(
                order__lt=hidden_stage_order
            ).first()

            if previous_stage:
                max_quantity = previous_stage.production_set.filter(
                    document__number=hidden_document
                ).first().quantity
                if quantity > max_quantity:
                    raise ValidationError(
                        'Значение не должно быть больше, '
                        f'чем в предыдущем статусе ({max_quantity})'
                    )
