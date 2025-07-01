from django.shortcuts import render
from django.views.generic import View , TemplateView ,ListView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Teacher
from .forms import TeacherForm
from django.contrib import messages

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
    
class hr(TemplateView):
    template_name = 'employ/hr.html'
