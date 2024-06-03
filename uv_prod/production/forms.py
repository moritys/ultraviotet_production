from typing import Any
from django import forms

from production.models import Production, Stage


class ProductionFormtest(forms.ModelForm):

    class Meta:
        model = Production
        fields = ('quantity',)
        widgets = {
            'quantity': forms.NumberInput(
                attrs={
                    'class': 'input',
                    'placeholder': '100',
                }
            )
        }


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

    def clean(self):
        '''
        Проверка максимального количества.
        Работает только если в бд заведены записи производства.
        '''
        cleaned_data = super().clean()
        hidden_stage = cleaned_data.get('hidden_stage')
        current_stage = Stage.objects.get(name=hidden_stage).order
        print(current_stage)

        if hidden_stage:
            previous_stage = Stage.objects.filter(
                order__lt=current_stage
            ).first()

            if previous_stage:
                max_quantity = previous_stage.production_set.first().quantity
                self.fields['quantity'].widget.attrs['max'] = max_quantity

        return cleaned_data
