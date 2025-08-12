from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView ,TemplateView
from django.urls import reverse
from django.db.models import Avg
from .models import Grade
from .form import GradeForm

from classroom.models import Classroom,ClassroomSubject
from students.models import Student

class grades(TemplateView):
    template_name = 'grade/grades.html'
    
class GradeDashboardView(TemplateView):
    template_name = 'grade/grades.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classrooms'] = Classroom.objects.all()
        return context

class GradeClassroomListView(ListView):
    model = Classroom
    template_name = 'grade/classroom_list.html'
    context_object_name = 'classrooms'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_grades'] = True  # للتمييز إذا كنت في قسم العلامات
        return context    

class GradeListView(ListView):
    model = Grade
    template_name = 'grades/grade_list.html'
    context_object_name = 'grades'
    
    def get_queryset(self):
        classroom_id = self.kwargs['classroom_id']
        # استخدم العلاقة الصحيحة عبر Classroomenrollment
        return Grade.objects.filter(
            student__classroom_enrollments__classroom_id=classroom_id
        ).select_related('student', 'subject')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classroom_id = self.kwargs['classroom_id']
        classroom = get_object_or_404(Classroom, id=classroom_id)
        
        # جلب الطلاب المسجلين في هذه الشعبة
        students = Student.objects.filter(
            classroom_enrollments__classroom=classroom
        ).distinct()
        
        # جلب مواد الشعبة
        subjects = ClassroomSubject.objects.filter(
            classroom=classroom
        ).select_related('subject')
        
        context.update({
            'classroom': classroom,
            'students': students,
            'subjects': subjects
        })
        return context

class GradeCreateView(CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'grade/grade_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        classroom_id = self.kwargs['classroom_id']
        classroom_subjects = ClassroomSubject.objects.filter(
            classroom_id=classroom_id
        ).select_related('subject')
        kwargs['subject_choices'] = classroom_subjects
        kwargs['classroom_id'] = classroom_id
        return kwargs
    
    def form_valid(self, form):
        form.instance.student = form.cleaned_data['student']
        return super().form_valid(form)
    
    def get_success_url(self):
        enrollment = self.object.student.classroom_enrollments.first()
        if enrollment:
            return reverse('grade:grade_list', kwargs={
                'classroom_id': enrollment.classroom.id
            })
        return reverse('grade:grade_dashboard')  # صفحة بديلة إذا لم يكن الطالب مسجلاً في أي فصل
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classroom'] = get_object_or_404(Classroom, id=self.kwargs['classroom_id'])
        return context