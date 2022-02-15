from doctest import DONT_ACCEPT_TRUE_FOR_1
from django import forms

chart_choices = (
    ("#1", "Bar chart"),
    ("#2", "Pie chart"),
    ("#3", "Line chart"),
)

class SalesSearchForm(forms.Form):
    from_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    chart_type = forms.ChoiceField(choices = chart_choices)

