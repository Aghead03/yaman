from django.db import models
from django.contrib.auth.models import User
from students.models import Student
from datetime import date

class Payment(models.Model):
    class PaymentType(models.TextChoices):
        COURSE = 'course', 'دورة'
        INSTALLMENT = 'installment', 'قسط'
        
    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'نقدي'
        BANK_TRANSFER = 'bank_transfer', 'تحويل بنكي'
        CHECK = 'check', 'شيك'

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices, default=PaymentType.COURSE)
    required_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=date.today)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    is_paid = models.BooleanField(default=False, verbose_name="مسدد بالكامل")
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_full(self):
        return self.amount >= self.required_amount

    def save(self, *args, **kwargs):
        # حساب حالة الدفع
        self.is_paid = (self.amount >= self.required_amount)
        
        # حفظ الدفع أولاً للحصول على ID
        super().save(*args, **kwargs)
        
        # إذا كانت هذه دفعة جديدة (لها ID الآن) أو تم تغيير المبلغ
        if self.pk and (not hasattr(self, '_amount_changed') or self._amount_changed):
            # إنشاء أو تحديث حركة مالية مرتبطة
            Transaction.objects.update_or_create(
                payment=self,
                defaults={
                    'type': 'income',
                    'amount': self.amount,
                    'date': self.date,
                    'description': f'دفعة من {self.student.full_name} ({self.get_payment_type_display()})',
                    'user': self.created_by
                }
            )
            self._amount_changed = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_amount = self.amount

    def __setattr__(self, name, value):
        if name == 'amount' and hasattr(self, '_original_amount'):
            self._amount_changed = value != self._original_amount
        super().__setattr__(name, value)

    def __str__(self):
        return f"دفعة #{self.id} - {self.student.full_name}"

class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        INCOME = 'income', 'وارد'
        EXPENSE = 'expense', 'منصرف'

    class ExpenseCategory(models.TextChoices):
        EMPLOYEE_SALARY = 'employee_salary', 'راتب موظف'
        TEACHER_SALARY = 'teacher_salary', 'راتب مدرس'
        FIXED_ASSETS = 'fixed_assets', 'شراء أصول ثابتة'
        MAINTENANCE = 'maintenance', 'مصاريف صيانة'
        PRINTING = 'printing', 'مصروف طباعة'
        MEDICAL = 'medical', 'مصروف طبابة'
        UTILITIES = 'utilities', 'مصروف خدمي'
        MARKETING = 'marketing', 'تسويق'
        COPYING = 'copying', 'طباعة'
        BUFFET = 'buffet', 'بوفيه'
        MISCELLANEOUS = 'miscellaneous', 'مصاريف متفرقة'
        GOVERNMENT = 'government', 'مصاريف حكومية'
        CLEANING = 'cleaning', 'تنظيف'

    type = models.CharField(max_length=10, choices=TransactionType.choices)
    expense_type = models.CharField(
        max_length=20, 
        choices=ExpenseCategory.choices, 
        null=True, 
        blank=True,
        verbose_name='نوع المصروف'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=date.today)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payment = models.OneToOneField(
        Payment, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='transaction'
    )