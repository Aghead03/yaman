from django.shortcuts import render ,get_object_or_404 , redirect
from django.views.generic import View , TemplateView ,ListView ,DetailView
from .models import Attendance
from .form import AttendanceForm
from classroom.models import Classroom
from students.models import Student
from django.contrib import messages
from django.http import JsonResponse
from django.db import IntegrityError
# Create your views here.

class attendance(ListView):
    model = Attendance
    template_name = 'attendance/attendance.html'
    context_object_name = 'attendance_records'
    
    def get_queryset(self):
        # الحصول على سجلات الحضور مع معلومات الشعبة
        return Attendance.objects.select_related('classroom').order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # تجميع التواريخ لكل شعبة
        summary = {}
        for record in context['attendance_records']:
            key = (record.classroom.id, record.classroom.name, record.date)
            if key not in summary:
                summary[key] = {
                    'classroom_id': record.classroom.id,
                    'classroom_name': record.classroom.name,
                    'date': record.date,
                    'student_count': Attendance.objects.filter(
                        classroom=record.classroom, 
                        date=record.date
                    ).count()
                }
        context['summary'] = summary.values()
        return context

class TakeAttendanceView(View):
    template_name = 'attendance/take_attendance.html'
    
    def get(self, request):
        form = AttendanceForm()
        return render(request, self.template_name, {
            'form': form,
            'classrooms': Classroom.objects.all()
        })
    
    def post(self, request):
        date = request.POST.get('date')
        classroom_id = request.POST.get('classroom')
        
        if not date or not classroom_id:
            messages.error(request, 'يجب اختيار التاريخ والشعبة')
            return redirect('attendance:take_attendance')
        
        classroom = get_object_or_404(Classroom, id=classroom_id)
        students = Student.objects.filter(
            classroom_enrollments__classroom=classroom
        ).distinct()
        
        # التحقق من وجود سجلات قديمة لنفس التاريخ والشعبة
        existing_attendances = Attendance.objects.filter(
            classroom=classroom,
            date=date
        ).exists()
        
        if existing_attendances:
            messages.error(request, 'يوجد بالفعل سجل حضور لهذا التاريخ والشعبة. الرجاء استخدام تعديل الحضور بدلاً من ذلك.')
            return redirect('attendance:take_attendance')
        
        success_count = 0
        error_messages = []
        
        for student in students:
            # قراءة القيمة مباشرة من الـ radio button
            status = request.POST.get(f'status_{student.id}', 'present')  # الافتراضي حاضر
            notes = request.POST.get(f'notes_{student.id}', '')
            
            try:
                attendance = Attendance.objects.create(
                    student=student,
                    classroom=classroom,
                    date=date,
                    status=status,
                    notes=notes
                )
                success_count += 1
            except IntegrityError as e:
                error_messages.append(f'خطأ في تسجيل حضور الطالب {student.full_name}: {str(e)}')
        
        if success_count > 0:
            messages.success(request, f'تم تسجيل حضور {success_count} طالب بنجاح')
        if error_messages:
            messages.error(request, '<br>'.join(error_messages))
        
        return redirect('attendance:attendance')


def get_students(request):
    classroom_id = request.GET.get('classroom')
    
    if not classroom_id:
        return JsonResponse({'error': 'يجب تحديد معرف الشعبة'}, status=400)
    
    try:
        # جلب الطلاب عبر علاقة التسجيل في الشعبة
        students = Student.objects.filter(
            classroom_enrollments__classroom_id=classroom_id
        ).distinct().values('id', 'full_name')
        
        if not students.exists():
            return JsonResponse({'error': 'لا يوجد طلاب في هذه الشعبة'}, status=404)
            
        return JsonResponse(list(students), safe=False)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



class AttendanceDetailView(ListView):
    model = Attendance
    template_name = 'attendance/attendance_detail.html'
    context_object_name = 'attendances'
    
    def get_queryset(self):
        classroom_id = self.kwargs.get('classroom_id')
        date = self.kwargs.get('date')
        return Attendance.objects.filter(classroom_id=classroom_id, date=date)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classroom'] = get_object_or_404(Classroom, id=self.kwargs.get('classroom_id'))
        context['date'] = self.kwargs.get('date')
        return context
    
    
### لتعديل الحضور 
class UpdateAttendanceView(View):
    template_name = 'attendance/update_attendance.html'
    
    def get(self, request, classroom_id, date):
        classroom = get_object_or_404(Classroom, id=classroom_id)
        attendances = Attendance.objects.filter(classroom=classroom, date=date)
        
        return render(request, self.template_name, {
            'classroom': classroom,
            'date': date,
            'attendances': attendances
        })
    
    def post(self, request, classroom_id, date):
        classroom = get_object_or_404(Classroom, id=classroom_id)
        students = Student.objects.filter(classroom_enrollments__classroom=classroom)
        
        success_count = 0
        error_messages = []
        
        for student in students:
            # قراءة القيمة مباشرة من الـ radio button
            status = request.POST.get(f'status_{student.id}', 'present')  # الافتراضي حاضر
            notes = request.POST.get(f'notes_{student.id}', '')
            
            try:
                attendance, created = Attendance.objects.update_or_create(
                    student=student,
                    date=date,
                    defaults={
                        'classroom': classroom,
                        'status': status,
                        'notes': notes
                    }
                )
                success_count += 1
            except IntegrityError as e:
                error_messages.append(f'خطأ في تحديث حضور الطالب {student.full_name}: {str(e)}')
        
        if success_count > 0:
            messages.success(request, f'تم تحديث حضور {success_count} طالب بنجاح')
        if error_messages:
            messages.error(request, '<br>'.join(error_messages))
        
        return redirect('attendance:attendance')