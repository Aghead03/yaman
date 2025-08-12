from django.db import models
from students.models import Student
from courses.models import Subject

# Create your models here.
class Classroom(models.Model):
    class BranchChoices(models.TextChoices):
        LITERARY = 'أدبي', 'الأدبي'
        SCIENTIFIC = 'علمي', 'العلمي'
        NINTH_GRADE = 'تاسع', 'الصف التاسع'
        
    name = models.CharField(max_length=50, verbose_name='اسم الشعبة',default="الشعبة 1")
    branches = models.CharField(
    max_length=100,
    choices=BranchChoices.choices,
    verbose_name='الفرع',
    default=BranchChoices.SCIENTIFIC  # أو أي قيمة مناسبة
    )
    
    
    @property
    def students(self):
        """إرجاع الطلاب المنتمين لهذه الشعبة حسب الفرع"""
        return Student.objects.filter(
            classroom_enrollments__classroom=self,
            branch=self.branches
        )
    
    def __str__(self):
        return f"{self.name} - {self.get_branches_display()}"
    
    class Meta:
        verbose_name = 'شعبة'
        verbose_name_plural = 'شعب'
        
class Classroomenrollment(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='classroom_enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('classroom', 'student')
    
    def __str__(self):
        return f"{self.student} في {self.classroom}"     
    
class ClassroomSubject(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name='الشعبة')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='المادة')
    
    class Meta:
        unique_together = ('classroom', 'subject')
        verbose_name = 'مادة الشعبة'
        verbose_name_plural = 'مواد الشعب'
    
    def __str__(self):
        return f"{self.classroom.name} - {self.subject.name}"        