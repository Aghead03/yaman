from django.shortcuts import render
from django.views.generic import View , TemplateView ,ListView ,DetailView ,CreateView, UpdateView ,DeleteView
from django.urls import reverse_lazy
from .models import Subject

# إدارة المواد
class SubjectListView(ListView):
    model = Subject
    template_name = 'curses/subject_list.html'
# Create your views here.

class SubjectCreateView(CreateView):
    model = Subject
    fields = ['name', 'subject_type', 'teachers']
    template_name = 'courses/subject_form.html'
    success_url = reverse_lazy('courses:subject_list')
    
class SubjectUpdateView(UpdateView):
    model = Subject
    fields = ['name', 'subject_type', 'teachers']
    template_name = 'courses/subject_form.html'
    success_url = reverse_lazy('courses:subject_list')

class SubjectDeleteView(DeleteView):
    model = Subject
    template_name = 'courses/subject_confirm_delete.html'
    success_url = reverse_lazy('courses:subject_list')    

class courses(TemplateView):
    template_name = 'courses/courses.html'