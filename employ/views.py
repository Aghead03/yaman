from django.shortcuts import render
from django.views.generic import View , TemplateView ,ListView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Teacher , Employee
from .forms import TeacherForm ,EmployeeRegistrationForm
from django.contrib import messages
from django.contrib.auth.models import Group


class CreateTeacherView(CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'employ/teacher_form.html'  # تأكد من مسار القالب
    success_url = success_url = '/employ/teachers/'  # أو أي مسار تريد التوجيه إليه  # عدل لمسار قائمة المدرسين
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'تم إضافة المدرس بنجاح')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'حدث خطأ في إدخال البيانات')
        return super().form_invalid(form)
# Create your views here.

class teachers(ListView):
    template_name = 'employ/teachers.html'
    model = Teacher
    context_object_name = 'teacher'
    
class hr(ListView):
    model = Employee
    template_name = 'employ/hr.html'
    context_object_name = 'employees'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        position = self.request.GET.get('position')
        search = self.request.GET.get('search')
        
        if position:
            queryset = queryset.filter(position=position)
        if search:
            queryset = queryset.filter(user__username__icontains=search) | \
            queryset.filter(user__first_name__icontains=search) | \
            queryset.filter(user__last_name__icontains=search)
        return queryset.select_related('user')



def create_groups():
    groups = ['Admins', 'Accountants','Mentor', 'Managers','Marketing','Reception', 'Employees']
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)

class EmployeeCreateView(CreateView):
    form_class = EmployeeRegistrationForm
    template_name = 'employ/employee_form.html'
    success_url = '/employ/hr/'
    
    def get(self, request, *args, **kwargs):
        create_groups() 
        return super().get(request, *args, **kwargs)