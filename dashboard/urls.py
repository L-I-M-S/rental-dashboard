from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('auth/', views.quickbooks_auth, name='quickbooks_auth'),
    path('callback/', views.quickbooks_callback, name='quickbooks_callback'),
    path('upload/', views.upload_excel, name='upload_excel'),
    path('rent-chart/', views.RentChartView.as_view(), name='rent_chart'),
]
