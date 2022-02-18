from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from datascience.models import Customer, Sale, Report, Product, Position, CSV
from datascience.forms import SalesSearchForm, ReportForm
from datascience.utils import get_chart, get_report_image
import pandas as pd
from django.template.loader import get_template
from xhtml2pdf import pisa
import csv
from django.utils.dateparse import parse_date

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
        
        no_data = "No data available in this range."
        
        if len(sale_qs) > 0: 
            # create the sales DataFrame      
            sales_df = pd.DataFrame(sale_qs.values())

            positions_data = []

            def get_customer_from_id(value):
                customer = Customer.objects.get(id=value)
                return customer
            
            sales_df["customer_id"] = sales_df["customer_id"].apply(get_customer_from_id) # replace the ForeignKey with the customer name
            sales_df["salesman_id"] = sales_df["salesman"]
            sales_df["created"] = sales_df["created"].apply(lambda x: x.strftime("%m-%d-%Y"))
            sales_df["updated"] = sales_df["updated"].apply(lambda x: x.strftime("%m-%d-%Y"))
            sales_df.rename({'customer_id': 'customer',
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
            
            sales_df = sales_df.to_html(index=False)
            positions_df = positions_df.to_html(index=False)
            merged_df = merged_df.to_html(index=False)
            groupby_df = groupby_df.to_html(index=False)
            no_data = None
        
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
    
def csv_upload_view(request):
    if request.method == 'POST':
        # get the file name
        csv_file_name = request.FILES.get('file').name
        # get the file
        csv_file = request.FILES.get('file')
        obj, created = CSV.objects.get_or_create(file_name=csv_file_name)
        
        csv_exists = {'csv_exists': True}

        # check if the object is created 
        if created:
            obj.csv_file = csv_file # create the file object
            obj.save() # save the file object in the database
            # open the csv file
            with open(obj.csv_file.path, 'r') as f:
                reader = csv.reader(f)
                reader.__next__() # skip the first row ( the thead )
                for row in reader:
                    # store the values from the CSV file in variables
                    transaction_id = row[1]
                    product = row[2]
                    quantity = int(row[3])
                    customer = row[4]
                    date = parse_date(row[5])

                    # check if the product exists
                    try:
                        product_obj = Product.objects.get(name__iexact=product)
                    except Product.DoesNotExist:
                        product_obj = None

                    if product_obj is not None:
                        customer_obj, _ = Customer.objects.get_or_create(name=customer) 
                        salesman_obj = "CSV Upload"
                        position_obj = Position.objects.create(product=product_obj, quantity=quantity, created=date)

                        sale_obj, _ = Sale.objects.get_or_create(transaction_id=transaction_id, customer=customer_obj, salesman=salesman_obj, created=date)
                        sale_obj.positions.add(position_obj)
                        sale_obj.save()        
                    csv_exists = {'csv_exists': False}       
                return JsonResponse(csv_exists)
        return JsonResponse(csv_exists)
    return HttpResponse()

def render_pdf_view(request, pk):
    template_path = 'datascience/reports/pdf.html'
    obj = get_object_or_404(Report, pk=pk)
    context = {'obj': obj}

    # Create the Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    # display the pdf
    response['Content-Disposition'] = 'filename="report.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
       html, dest=response)

    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


class SaleListView(ListView):
    model = Sale
    template_name = "datascience/sales/sales_list.html"
    
    
class SaleDetailView(DetailView):
    model = Sale
    template_name = "datascience/sales/sales_details.html"


class ReportListView(ListView):
    model = Report
    template_name = "datascience/reports/reports_list.html"
    
    
class UploadCsvView(TemplateView):
    template_name = "datascience/reports/from_file.html"
