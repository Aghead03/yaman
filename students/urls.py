from django.contrib import admin
from django.urls import path
from . import views

app_name = "students"


urlpatterns = [
    path('student/',views.student.as_view() , name="student"),
    path('student_groups/',views.student_groups.as_view() , name="student_groups"),
    path('student_profile/<int:student_id>/',views.student_profile , name="student_profile"),
    path('create/', views.CreateStudentView.as_view(), name="create_student"),
    path('update/<int:pk>/', views.UpdateStudentView.as_view(), name="update_student"),  # جديد
    path('delete/<int:pk>/', views.StudentDeleteView.as_view(), name="delete_student"),
]