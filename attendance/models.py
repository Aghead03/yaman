from django.db import models
from django.utils import timezone
from classroom.models import Classroom
from students.models import Student

class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'present', 'حاضر'
        ABSENT = 'absent', 'غائب'
        LATE = 'late', 'متأخر'
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='الطالب')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name='الشعبة')
    date = models.DateField(default=timezone.now, verbose_name='التاريخ')
    status = models.CharField(max_length=10, choices=Status.choices, default='absent', verbose_name='الحالة')
    notes = models.TextField(blank=True, null=True, verbose_name='ملاحظات')
    
    class Meta:
        verbose_name = 'حضور'
        verbose_name_plural = 'سجل الحضور'
        unique_together = ('student', 'date')  # منع تكرار تسجيل نفس الطالب في نفس اليوم
    
    def __str__(self):
        return f"{self.student.full_name} - {self.date} - {self.get_status_display()}"