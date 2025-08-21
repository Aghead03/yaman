from django import forms 
from django.views.generic import ListView, CreateView ,DeleteView , UpdateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth import get_user_model
from attendance.models import Attendance
from classroom.models import Classroomenrollment
from django.http import JsonResponse
from django.shortcuts import render , get_object_or_404
from django.views.generic import View , TemplateView ,ListView ,DetailView
from .models import Student
from django.contrib import messages
from django.utils.dateparse import parse_date
from . forms import StudentForm

User = get_user_model()

class student(ListView):
    template_name = 'students/student.html'
    model = Student
    context_object_name = 'student'
    
    def get_queryset(self):
        # ترتيب الطلاب أبجديًا حسب الاسم
        queryset = Student.objects.all().order_by('full_name')
        
        # إضافة وظيفة البحث
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(full_name__icontains=search_query) |
                Q(student_number__icontains=search_query) |
                Q(branch__icontains=search_query) |
                Q(father_phone__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # إضافة قيمة البحث للقالب للحفاظ عليها في واجهة المستخدم
        context['search_query'] = self.request.GET.get('search', '')
        return context
    
    
class student_groups(TemplateView):
    template_name = 'students/student_groups.html'
    
    
def student_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    enrollments = Classroomenrollment.objects.filter(student=student).select_related('classroom')
    
    # حساب بيانات الحضور لكل شعبة
    for enrollment in enrollments:
        total_attendance = Attendance.objects.filter(classroom=enrollment.classroom).count()
        present_attendance = Attendance.objects.filter(
            classroom=enrollment.classroom, 
            student=student, 
            status='present'
        ).count()
        
        enrollment.total_attendance = total_attendance
        enrollment.present_attendance = present_attendance
        enrollment.attendance_percentage = (present_attendance / total_attendance * 100) if total_attendance > 0 else 0
    
    context = {
        'student': student,
        'enrollments': enrollments,
    }
    return render(request, 'students/student_profile.html', context)
    
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
        # إضافة المستخدم الحالي كالمستخدم الذي أضاف الطالب
        form.instance.added_by = self.request.user
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
    
    
    
    
from django.contrib.auth.mixins import UserPassesTestMixin

class UpdateStudentView(UserPassesTestMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/update_student.html'
    success_url = reverse_lazy('students:student')
    
    def test_func(self):
        # يسمح فقط للمستخدم الذي أضاف الطالب أو للمشرفين
        student = self.get_object()
        return self.request.user == student.added_by or self.request.user.is_superuser
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'تم تعديل بيانات الطالب بنجاح')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'حدث خطأ في تعديل البيانات')
        return super().form_invalid(form)    