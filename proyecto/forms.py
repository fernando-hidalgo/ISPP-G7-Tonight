from django import forms


class DatePickerInput(forms.DateInput):
        input_type = 'date'

class TimePickerInput(forms.TimeInput):
    input_type = 'time'

class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'

class TransactionForm(forms.Form):
    dia = forms.DateField(widget=DatePickerInput, label="Día")
    hora = forms.TimeField(widget=TimePickerInput, label="Hora")


