from django.contrib import admin
from django.urls import path
from . import views

app_name = "employ"


urlpatterns = [
    path('teachers/',views.teachers.as_view() , name="teachers"),
    path('delete/<int:pk>/', views.TeacherDeleteView.as_view(), name="delete_teacher"),  # جديد
    path('hr/',views.hr.as_view() , name="hr"),
    path('create/', views.CreateTeacherView.as_view(), name="create"),
    path('delete-employee/<int:pk>/', views.EmployeeDeleteView.as_view(), name='employee_delete'),
    path('register/', views.EmployeeCreateView.as_view(), name='employee_register'),
    path('update/', views.select_employee, name='select_employee'),
    path('update/<int:pk>/', views.EmployeeUpdateView.as_view(), name='employee_update'),

]