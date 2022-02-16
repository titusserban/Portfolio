from django.urls import path
from datascience import views

app_name = "datascience"

urlpatterns = [
    path("", views.home_view, name="datascience_home"),
    path("sales_list/", views.SaleListView.as_view(), name="sales_list"),
    path("sale_details/<pk>/", views.SaleDetailView.as_view(), name="sale_details"),
    path("create_report_view/", views.create_report_view, name="create_report_view"),
]