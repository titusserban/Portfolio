from django.urls import path
from datascience import views

app_name = "datascience"

urlpatterns = [
    path("", views.home_view, name="datascience_home"),
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
]