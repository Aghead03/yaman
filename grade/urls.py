from django.urls import path
from . import views

app_name = 'grade'

urlpatterns = [
    path('', views.grades_dashboard, name='dashboard'),
    path('<int:classroom_id>/subjects/', views.select_subject, name='select_subject'),  
    path('<int:classroom_id>/subjects/<int:subject_id>/', views.view_grades, name='view_grades'),
    path('<int:classroom_id>/subjects/<int:subject_id>/edit/', views.edit_grades, name='edit_grades'),
]