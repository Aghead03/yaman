from django.contrib import admin
from django.urls import path
from . import views

app_name = "attendance"


urlpatterns = [
        
        path('attendance/',views.attendance.as_view() , name="attendance"),
        path('attendance/detail/<int:classroom_id>/<str:date>/', views.AttendanceDetailView.as_view(), name='attendance_detail'),
        path('api/students/', views.get_students, name='get_students'),
        path('attendance/take/', views.TakeAttendanceView.as_view(), name='take_attendance'),
        path('attendance/update/<int:classroom_id>/<str:date>/', views.UpdateAttendanceView.as_view(), name='update_attendance'),

]