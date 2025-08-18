from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from .models import Grade
from classroom.models import Classroom
from courses.models import Subject
from students.models import Student
from .form import GradeForm

def grades_dashboard(request):
    classrooms = Classroom.objects.all()
    return render(request, 'grade/dashboard.html', {'classrooms': classrooms})

def view_grades(request, classroom_id, subject_id):
    # صفحة عرض العلامات (للقراءة فقط)
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    subject = get_object_or_404(Subject, pk=subject_id)
    
    grades = Grade.objects.filter(
        classroom=classroom,
        subject=subject
    ).select_related('student')
    
    return render(request, 'grade/view_grades.html', {
        'classroom': classroom,
        'subject': subject,
        'grades': grades
    })

def edit_grades(request, classroom_id, subject_id):
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    subject = get_object_or_404(Subject, pk=subject_id)
    
    GradeFormSet = modelformset_factory(Grade, form=GradeForm, extra=0)
    students = classroom.students.all().order_by('full_name')
    
    if request.method == 'POST':
        formset = GradeFormSet(request.POST, request.FILES)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.classroom = classroom
                instance.subject = subject
                instance.save()
            return redirect('grade:view_grades', classroom.id, subject.id)
    else:
        # جلب العلامات الموجودة للمادة الحالية فقط
        grades = Grade.objects.filter(
            classroom=classroom,
            subject=subject
        )
        
        # إنشاء علامات للطلاب المفقودين فقط
        existing_student_ids = grades.values_list('student_id', flat=True)
        missing_students = students.exclude(id__in=existing_student_ids)
        
        new_grades = []
        for student in missing_students:
            for exam_type in ['activity', 'monthly', 'midterm', 'final']:
                new_grades.append(Grade(
                    student=student,
                    classroom=classroom,
                    subject=subject,
                    exam_type=exam_type,
                    grade=0,
                    notes=''
                ))
        
        if new_grades:
            Grade.objects.bulk_create(new_grades)
            grades = Grade.objects.filter(classroom=classroom, subject=subject)
        
        formset = GradeFormSet(queryset=grades)
    
    return render(request, 'grade/edit_grades.html', {
        'classroom': classroom,
        'subject': subject,
        'formset': formset,
        'students': students
    })
    
def select_subject(request, classroom_id):
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    subjects = classroom.classroomsubject_set.all()  
    
    return render(request, 'grade/select_subject.html', {
        'classroom': classroom,
        'subjects': subjects
    })  