from django import forms


class ProductionForm(forms.Form):
    board = forms.CharField(label='Плата', max_length=50)
    stage = forms.CharField(label='Этап', max_length=256)
    quantity = forms.IntegerField(
        label='Количество плат',
        min_value=0,
        max_value=500_000,
    )
