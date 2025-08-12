from django.db import models
from django.contrib.auth.models import User
from students.models import Student
from datetime import date

class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'نقدي'
        BANK_TRANSFER = 'bank_transfer', 'تحويل بنكي'
        CHECK = 'check', 'شيك'

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=date.today)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    is_full = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"دفعة #{self.id} - {self.student.full_name}"

class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        INCOME = 'income', 'وارد'
        EXPENSE = 'expense', 'منصرف'

    type = models.CharField(max_length=10, choices=TransactionType.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=date.today)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.amount} ل.س"