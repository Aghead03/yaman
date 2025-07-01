from django.db import models
from django.core.validators import MinLengthValidator
from datetime import date

class Teacher(models.Model):
    # خيارات المواد الدراسية
    class SubjectChoices(models.TextChoices):
        MATH = 'math', 'الرياضيات'
        PHYSICS = 'physics', 'الفيزياء'
        CHEMISTRY = 'chemistry', 'الكيمياء'
        BIOLOGY = 'biology', 'علوم'
        ARABIC = 'arabic', 'اللغة العربية'
        ENGLISH = 'english', 'اللغة الإنجليزية'
        FRENCH = 'french', 'اللغة الفرنسية'
        HISTORY = 'history', 'التاريخ'
        GEOGRAPHY = 'geography', 'الجغرافيا'
        PHILOSOPHY = 'philosophy', 'الفلسفة'
        RELIGION = 'religion', 'التربية الإسلامية'

    # خيارات نوع العقد
    class ContractTypeChoices(models.TextChoices):
        FULL_TIME = 'full-time', 'بكلوريا'
        PART_TIME = 'part-time', 'تاسع'
        HOURLY = 'hourly', 'مشترك'

    # خيارات الفروع الدراسية
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
    id_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='رقم الهوية',
        validators=[MinLengthValidator(5)]
    )

    # المعلومات المهنية
    subject = models.CharField(
        max_length=20,
        choices=SubjectChoices.choices,
        verbose_name='المادة'
    )
    branches = models.CharField(
        max_length=100,
        verbose_name='الفروع',
        help_text='الفروع التي يدرسها المدرس (يمكن اختيار أكثر من فرع)'
    )
    contract_type = models.CharField(
        max_length=20,
        choices=ContractTypeChoices.choices,
        verbose_name='نوع العقد'
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
