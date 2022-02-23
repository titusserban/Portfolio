from django import forms
from datascience.models import Report, Sale, Customer, Product, Position

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
    from_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), initial="2022-02-02")
    to_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), initial="2022-02-10")
    chart_type = forms.ChoiceField(choices = chart_choices)
    result_by = forms.ChoiceField(choices = result_choices)
    
    
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ("name", "remarks", "author")


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['positions', 'salesman', 'customer']

    def __init__(self, pk, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)
        self.pk = pk
        

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name']

    def __init__(self, pk, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.pk = pk


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']

    def __init__(self, pk, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.pk = pk


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['product', 'quantity']

    def __init__(self, pk, *args, **kwargs):
        super(PositionForm, self).__init__(*args, **kwargs)
        self.pk = pk