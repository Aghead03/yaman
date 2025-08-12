from django.contrib import admin
from django.urls import path
from . import views

app_name = "grade"

urlpatterns = [
    
    path('grades/', views.GradeDashboardView.as_view(), name='grades'),
    path('grades/classrooms/', views.GradeClassroomListView.as_view(), name='grade_classrooms'),
    path('classroom/<int:classroom_id>/grades/', views.GradeListView.as_view(), name='grade_list')    ,
    path('classroom/<int:classroom_id>/grades/add/', views.GradeCreateView.as_view(), name='grade_create'),
    
]
