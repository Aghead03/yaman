from django.contrib import admin
from django.urls import path
from . import views

app_name = "accounting"


urlpatterns = [
    path('',views.accounting.as_view() , name="accounting"),
    path('reports/',views.reports.as_view() , name="reports"),
    
]