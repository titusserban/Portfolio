from doctest import DONT_ACCEPT_TRUE_FOR_1
from django import forms
from datascience.models import Report

chart_choices = (
    ("#1", "Bar chart"),
    ("#2", "Pie chart"),
    ("#3", "Line chart"),
)

result_choices = (
    ("#1", "Transaction"),
    ("#2", "Sale date"),
)


class SalesSearchForm(forms.Form):
    from_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    chart_type = forms.ChoiceField(choices = chart_choices)
    result_by = forms.ChoiceField(choices = result_choices)
    
    
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ("name", "remarks", "author")

