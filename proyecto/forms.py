from django import forms

class NumberInput(forms.NumberInput):
    input_type = 'number'

class PaypalAmountForm(forms.Form):
    cantidad = forms.IntegerField(widget=NumberInput, label="Cantidad")
