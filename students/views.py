from django import forms 
from django.views.generic import ListView, CreateView ,DeleteView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View , TemplateView ,ListView ,DetailView
from .models import Student
from django.contrib import messages
from django.utils.dateparse import parse_date
from . forms import StudentForm


class student(ListView):
    template_name = 'students/student.html'
    model = Student
    context_object_name = 'student'
    
    
class student_groups(TemplateView):
    template_name = 'students/student_groups.html'
    
class student_profile(DetailView):
    template_name = 'students/student_profile.html'
    model = Student
    context_object_name = 'student'

    

    
class grades(TemplateView):
    template_name = 'students/grades.html'
    
class courses(TemplateView):
    template_name = 'students/courses.html'
    
class CreateStudentView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/create_student.html'
    success_url = reverse_lazy('students:student')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'تم إضافة الطالب بنجاح')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'حدث خطأ في إدخال البيانات')
        return super().form_invalid(form)
    
    
    
class StudentDeleteView(DeleteView):
    model = Student
    success_url = reverse_lazy('students:student')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})