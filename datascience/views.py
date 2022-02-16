from django.http import JsonResponse
from itertools import groupby
from venv import create
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from datascience.models import Sale, Report
from datascience.forms import SalesSearchForm, ReportForm

from registration.models import UserProfile
from datascience.models import Customer

from .utils import get_chart, get_report_image

import pandas as pd

def home_view(request):
    
    search_form = SalesSearchForm(request.POST or None) # or None in order to allow the form to load without errors -> all fields are required
    report_form = ReportForm
    
    # declare the DataFrame variables
    sales_df = None
    positions_df = None
    merged_df = None
    groupby_df = None
    chart = None
    no_data = None
    
    if request.method == "POST":
        # Get the user inputs
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        chart_type = request.POST.get("chart_type")
        result_by = request.POST.get("result_by")
    
        sale_qs = Sale.objects.filter(created__date__lte=to_date, created__date__gte=from_date) # lte = less than or equal, gte = greater than or equal
        
        if len(sale_qs) > 0: 
            # create the sales DataFrame      
            sales_df = pd.DataFrame(sale_qs.values())

            positions_data = []
            
            def get_salesman_from_id(value):
                salesman = UserProfile.objects.get(id=value)
                return salesman.user.username

            def get_customer_from_id(value):
                customer = Customer.objects.get(id=value)
                return customer
            
            sales_df["customer_id"] = sales_df["customer_id"].apply(get_customer_from_id) # replace the ForeignKey with the customer name
            sales_df["salesman_id"] = sales_df["salesman_id"].apply(get_salesman_from_id) # replace the ForeignKey with the salesman name
            sales_df["created"] = sales_df["created"].apply(lambda x: x.strftime("%m-%d-%Y"))
            sales_df["updated"] = sales_df["updated"].apply(lambda x: x.strftime("%m-%d-%Y"))
            sales_df.rename({'customer_id': 'customer',
                             'salesman_id': 'salesman',
                             'id': 'sales_id'},
                            axis=1,
                            inplace=True) # inplace=True in order to avoid storing the value in a variable
            
            # we cannot access the get_positions() on a query set, therefore we have to loop through the query set
            for sale_item in sale_qs:
                for position in sale_item.get_positions():
                    obj = {
                        "position_id": position.id,
                        "product": position.product.name,
                        "quantity": position.quantity,
                        "price": position.price,
                        "sales_id": position.get_sales_id(),
                    }
                    positions_data.append(obj)
            
            positions_df = pd.DataFrame(positions_data)
            merged_df = pd.merge(sales_df, positions_df, on='sales_id')
            groupby_df = merged_df.groupby('transaction_id', as_index=False)['price'].agg('sum')
            
            chart = get_chart(chart_type, sales_df, result_by)
            
            sales_df = sales_df.to_html()
            positions_df = positions_df.to_html()
            merged_df = merged_df.to_html()
            groupby_df = groupby_df.to_html()
           
        else:
            no_data = "No data available in this range."
        
    context = { 
        "search_form": search_form,
        "sales_df": sales_df,
        "positions_df": positions_df,
        "merged_df": merged_df,
        "groupby_df": groupby_df,
        "chart": chart,
        "report_form": report_form,
        "no_data": no_data,
    }
    
    return render(request, "datascience/datascience_home.html", context)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def create_report_view(request):
    if is_ajax(request=request):
        name = request.POST.get('name')
        remarks = request.POST.get('remarks')
        author = request.POST.get('author')
        image = request.POST.get('image')
        
        img = get_report_image(image)
        
        # create the Report object
        Report.objects.create(name=name, remarks=remarks, author=author, image=img)
        
        return JsonResponse({"msg": "send"})
    
    return JsonResponse({})


class SaleListView(ListView):
    model = Sale
    template_name = "datascience/sales_list.html"
    
    
class SaleDetailView(DetailView):
    model = Sale
    template_name = "datascience/sales_details.html"

