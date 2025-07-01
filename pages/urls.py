from django.contrib import admin
from django.urls import path
from . import views

app_name = "pages"


urlpatterns = [
    path('',views.index.as_view() , name="index"),
]