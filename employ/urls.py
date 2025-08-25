from django.contrib import admin
from django.urls import path
from . import views

app_name = "employ"


urlpatterns = [
    path('teachers/',views.teachers.as_view() , name="teachers"),
    path('delete/<int:pk>/', views.TeacherDeleteView.as_view(), name="delete_teacher"),
    path('teacher/<int:pk>/', views.TeacherProfileView.as_view(), name='teacher_profile'),
    path('hr/',views.hr.as_view() , name="hr"),
    path('create/', views.CreateTeacherView.as_view(), name="create"),
    path('delete-employee/<int:pk>/', views.EmployeeDeleteView.as_view(), name='employee_delete'),
    path('register/', views.EmployeeCreateView.as_view(), name='employee_register'),
    path('update/', views.select_employee, name='select_employee'),
    path('update/<int:pk>/', views.EmployeeUpdateView.as_view(), name='employee_update'),
    path('vacations/', views.VacationListView.as_view(), name='vacation_list'),
    path('vacations/create/', views.VacationCreateView.as_view(), name='vacation_create'),
    path('vacations/update/<int:pk>/', views.VacationUpdateView.as_view(), name='vacation_update'),

]