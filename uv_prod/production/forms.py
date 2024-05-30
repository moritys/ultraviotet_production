from django import forms


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
