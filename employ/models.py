from django.db import models
from django.core.validators import MinLengthValidator
from datetime import date

class Teacher(models.Model):

    class BranchChoices(models.TextChoices):
        LITERARY =  'أدبي'
        SCIENTIFIC =  'علمي'
        NINTH_GRADE =  'تاسع'

    # المعلومات الشخصية
    full_name = models.CharField(
        max_length=100,
        verbose_name='الاسم الكامل',
        validators=[MinLengthValidator(3)]
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name='رقم الهاتف',
        validators=[MinLengthValidator(8)]
    )



    branches = models.CharField(
        max_length=100,
        verbose_name='الفروع',
        help_text='الفروع التي يدرسها المدرس (يمكن اختيار أكثر من فرع)'
    )

    hire_date = models.DateField(
        default=date.today,
        verbose_name='تاريخ التعيين'
    )

    # معلومات إضافية
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='ملاحظات'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'مدرس'
        verbose_name_plural = 'المدرسون'
        ordering = ['-created_at']
# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Employee(models.Model):
    POSITION_CHOICES = [
        ('admin', 'إداري'),
        ('accountant', 'محاسب'),
        ('mentor', 'موجه'),
        ('manager', 'مدير'),
        ('marketing', 'تسويق'),
        ('reception', 'استقبال'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    phone_number = models.CharField(max_length=20)
    hire_date = models.DateField(auto_now_add=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    # باقي الحقول حسب احتياجك
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_position_display()}"