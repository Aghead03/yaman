from django.contrib import admin
from django.urls import path
from . import views

app_name = "employ"


urlpatterns = [
    path('teachers/',views.teachers.as_view() , name="teachers"),
    path('hr/',views.hr.as_view() , name="hr"),
    path('create/', views.CreateTeacherView.as_view(), name="create"),
    path('register/', views.EmployeeCreateView.as_view(), name='employee_register'),

]