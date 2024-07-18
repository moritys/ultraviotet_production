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
    hidden_document = forms.CharField(widget=forms.HiddenInput)

    def clean_hidden_document(self):
        data = self.cleaned_data['hidden_document']
        try:
            return int(data)
        except ValueError:
            raise forms.ValidationError('Номер документа не число.')
