from django.urls import path
from datascience import views

app_name = "datascience"

urlpatterns = [
    path("overview/", views.OverviewView.as_view(), name="overview"),
    path("home/", views.home_view, name="datascience_home"),
    path("<int:pk>/pdf/", views.render_pdf_view, name="pdf"),
    path("upload_csv/", views.UploadCsvView.as_view(), name="upload_csv"),
    path("upload_file/", views.csv_upload_view, name="upload_file"),
    
    # Sales CRUD
    path("sales_list/", views.SaleListView.as_view(), name="sales_list"),
    path("sales_create/", views.CreateSaleView.as_view(), name="sales_create"),
    path("sales_update/<int:pk>/", views.UpdateSaleView.as_view(), name="sales_update"),
    path("sales_delete/<int:pk>/", views.delete_sale, name="sales_delete"),
    path("sale_details/<int:pk>", views.SaleDetailView.as_view(), name="sale_details"),
    
    # Reports CRD
    path("reports_list/", views.ReportListView.as_view(), name="reports_list"),
    path("create_report_view/", views.create_report_view, name="create_report_view"),
    path("delete_report/<int:pk>/", views.delete_report, name="delete_report"),
    
    # Customer CRUD
    path("customer_list/", views.CustomerListView.as_view(), name="customer_list"),
    path("customer_create/", views.CreateCustomerView.as_view(), name="customer_create"),
    path("customer_update/<int:pk>/", views.UpdateCustomerView.as_view(), name="customer_update"),
    path("customer_delete/<int:pk>/", views.delete_customer, name="customer_delete"),
    
    # Product CRUD
    path("product_list/", views.ProductListView.as_view(), name="product_list"),
    path("product_create/", views.CreateProductView.as_view(), name="product_create"),
    path("product_update/<int:pk>/", views.UpdateProductView.as_view(), name="product_update"),
    path("product_delete/<int:pk>/", views.delete_product, name="product_delete"),
    
    # Position CRUD
    path("position_list/", views.PositionListView.as_view(), name="position_list"),
    path("position_create/", views.CreatePositionView.as_view(), name="position_create"),
    path("position_update/<int:pk>/", views.UpdatePositionView.as_view(), name="position_update"),
    path("position_delete/<int:pk>/", views.delete_position, name="position_delete"),
    
]