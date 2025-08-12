
from django.db import models
from employ.models import Teacher
# Create your models here.

class Subject(models.Model):
    class SubjectType(models.TextChoices):
        SCIENTIFIC = 'scientific', 'علمي'
        LITERARY = 'literary', 'أدبي'
        NINTH = 'ninth', 'تاسع'
        COMMON = 'common', 'مشترك'
    
    name = models.CharField(max_length=100, verbose_name='اسم المادة')
    subject_type = models.CharField(
        max_length=10, 
        choices=SubjectType.choices,
        verbose_name='نوع المادة'
    )
    teachers = models.ManyToManyField(
        'employ.Teacher', 
        verbose_name='المدرسون',
        related_name='subjects_taught' 
    )
    class Meta:
        verbose_name = 'مادة'
        verbose_name_plural = 'المواد'
    
    def __str__(self):
        return self.name
    