from django.contrib import admin
from django.urls import path
from . import views

app_name = "students"


urlpatterns = [
    path('student/',views.student.as_view() , name="student"),
    path('student_groups/',views.student_groups.as_view() , name="student_groups"),
    path('student_profile/<int:pk>/',views.student_profile.as_view() , name="student_profile"),
    path('attendance/',views.attendance.as_view() , name="attendance"),
    path('grades/',views.grades.as_view() , name="grades"),
    path('courses/',views.courses.as_view() , name="courses"),
    path('create/', views.CreateStudentView.as_view(), name="create_student"),
    ]