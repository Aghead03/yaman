from django.contrib import admin
from django.urls import path,include

from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    
    path('login/',LoginView.as_view(template_name='registration/login.html',redirect_authenticated_user=True),name='login',),
    path('logout/',LogoutView.as_view(),name='logout'),
    
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('students/', include('students.urls')),
    path('employ/', include('employ.urls')),
    path('accounting/', include('accounting.urls')),    
    path('attendance/', include('attendance.urls')),
    path('grade/', include('grade.urls')),
    path('courses/', include('courses.urls')),
    path('classroom/', include('classroom.urls')),
    path('registration/', include('registration.urls')),
]