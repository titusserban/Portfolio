from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from datascience.models import Customer, Sale, Report, Product, Position, CSV
from datascience.forms import SalesSearchForm, ReportForm, SaleForm, CustomerForm, ProductForm, PositionForm
from datascience.utils import get_chart, get_report_image
import pandas as pd
from django.template.loader import get_template
from xhtml2pdf import pisa
import csv
from django.utils.dateparse import parse_date


 # Dashboard
class OverviewView(TemplateView):
    template_name = "datascience/datascience_overview.html"


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
    
        sale_qs = Sale.objects.filter(created__date__lte=to_date, created__date__gte=from_date, is_active=True) # lte = less than or equal, gte = greater than or equal
        
        no_data = "No data available in this range."
        
        if len(sale_qs) > 0: 
            # create the sales DataFrame      
            sales_df = pd.DataFrame(sale_qs.values())

            positions_data = []

            def get_customer_from_id(value):
                customer = Customer.objects.get(id=value)
                return customer
            
            sales_df["customer_id"] = sales_df["customer_id"].apply(get_customer_from_id) # replace the ForeignKey with the customer name
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
            # create the file object
            obj.csv_file = csv_file 
            # save the file object in the database
            obj.save() 
            # open the csv file
            with open(obj.csv_file.path, 'r') as f:
                reader = csv.reader(f)
                # skip the first row ( the thead )
                reader.__next__()
                for row in reader:
                    if len(row) == 6:
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
                            sale_obj, _ = Sale.objects.get_or_create(transaction_id=transaction_id,
                                                                    customer=customer_obj,
                                                                    salesman=salesman_obj,
                                                                    created=date,
                                                                    is_active=True)
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


# Sales CRUD
class SaleListView(ListView):
    model = Sale
    template_name = "datascience/sales/sales_list.html"
    
    def get_queryset(self):
        return self.model.objects.filter(is_active=True)


class CreateSaleView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'datascience/sales/sales_form.html'

    def get_form_kwargs(self):
        kwargs = super(CreateSaleView, self).get_form_kwargs()
        kwargs.update({"pk": None})
        return kwargs

    def get_success_url(self):
        return reverse('datascience:sales_list')


class UpdateSaleView(UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'datascience/sales/sales_form.html'

    def get_form_kwargs(self):
        kwargs = super(UpdateSaleView, self).get_form_kwargs()
        kwargs.update({"pk": self.kwargs["pk"]})
        return kwargs

    def form_valid(self, form):
        return super(UpdateSaleView, self).form_valid(form)

    def form_invalid(self, form):
        return super(UpdateSaleView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('datascience:sales_list')

def delete_sale(request, pk):
    Sale.objects.filter(id=pk).update(is_active=False)
    return redirect('datascience:sales_list')

    
class SaleDetailView(DetailView):
    model = Sale
    template_name = "datascience/sales/sales_details.html"


# Reports CRD
class ReportListView(ListView):
    model = Report
    template_name = "datascience/reports/reports_list.html"
    
    def get_queryset(self):
        return self.model.objects.filter(is_active=True)
    
def create_report_view(request):
    if is_ajax(request=request):
        name = request.POST.get('name')
        remarks = request.POST.get('remarks')
        author = request.POST.get('author')
        image = request.POST.get('image')
        
        img = get_report_image(image)
        
        # create the Report object
        Report.objects.create(name=name, remarks=remarks, author=author, image=img, is_active=True)   
        return JsonResponse({"msg": "send"})
    return JsonResponse({})

def delete_report(request, pk):
    Report.objects.filter(id=pk).update(is_active=False)
    return redirect('datascience:reports_list')
  
  
 # Upload CSV
class UploadCsvView(TemplateView):
    template_name = "datascience/reports/from_file.html"


# Customer CRUD
class CustomerListView(ListView):
    model = Customer
    template_name = "datascience/customer/customer_list.html"
    
    def get_queryset(self):
        return self.model.objects.filter(is_active=True)


class CreateCustomerView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'datascience/customer/customer_form.html'

    def get_form_kwargs(self):
        kwargs = super(CreateCustomerView, self).get_form_kwargs()
        kwargs.update({"pk": None})
        return kwargs

    def get_success_url(self):
        return reverse('datascience:customer_list')


class UpdateCustomerView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'datascience/customer/customer_form.html'

    def get_form_kwargs(self):
        kwargs = super(UpdateCustomerView, self).get_form_kwargs()
        kwargs.update({"pk": self.kwargs["pk"]})
        return kwargs

    def form_valid(self, form):
        return super(UpdateCustomerView, self).form_valid(form)

    def form_invalid(self, form):
        return super(UpdateCustomerView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('datascience:customer_list')

def delete_customer(request, pk):
    Customer.objects.filter(id=pk).update(is_active=False)
    return redirect('datascience:customer_list')


# Product CRUD
class ProductListView(ListView):
    model = Product
    template_name = "datascience/product/product_list.html"
    
    def get_queryset(self):
        return self.model.objects.filter(is_active=True)


class CreateProductView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'datascience/product/product_form.html'

    def get_form_kwargs(self):
        kwargs = super(CreateProductView, self).get_form_kwargs()
        kwargs.update({"pk": None})
        return kwargs

    def get_success_url(self):
        return reverse('datascience:product_list')


class UpdateProductView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'datascience/product/product_form.html'

    def get_form_kwargs(self):
        kwargs = super(UpdateProductView, self).get_form_kwargs()
        kwargs.update({"pk": self.kwargs["pk"]})
        return kwargs

    def form_valid(self, form):
        return super(UpdateProductView, self).form_valid(form)

    def form_invalid(self, form):
        return super(UpdateProductView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('datascience:product_list')

def delete_product(request, pk):
    Product.objects.filter(id=pk).update(is_active=False)
    return redirect('datascience:product_list')


# Position CRUD
class PositionListView(ListView):
    model = Position
    template_name = "datascience/position/position_list.html"
    
    def get_queryset(self):
        return self.model.objects.filter(is_active=True)


class CreatePositionView(CreateView):
    model = Position
    form_class = PositionForm
    template_name = 'datascience/position/position_form.html'

    def get_form_kwargs(self):
        kwargs = super(CreatePositionView, self).get_form_kwargs()
        kwargs.update({"pk": None})
        return kwargs

    def get_success_url(self):
        return reverse('datascience:position_list')


class UpdatePositionView(UpdateView):
    model = Position
    form_class = PositionForm
    template_name = 'datascience/position/position_form.html'

    def get_form_kwargs(self):
        kwargs = super(UpdatePositionView, self).get_form_kwargs()
        kwargs.update({"pk": self.kwargs["pk"]})
        return kwargs

    def form_valid(self, form):
        return super(UpdatePositionView, self).form_valid(form)

    def form_invalid(self, form):
        return super(UpdateProductView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('datascience:position_list')

def delete_position(request, pk):
    Position.objects.filter(id=pk).update(is_active=False)
    return redirect('datascience:position_list')

