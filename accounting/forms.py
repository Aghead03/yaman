from django import forms
from .models import Payment, Transaction
from django.db.models import Sum, Count ,Q , F


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student', 'payment_type', 'required_amount', 'amount', 'date', 'payment_method', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        # استخراج معلمة student من kwargs إذا وجدت
        self.student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        
        # إذا كان هناك طالب محدد، نعطيه قيمة ابتدائية
        if self.student:
            self.fields['student'].initial = self.student
            # يمكنك أيضاً جعل حقل الطالب مخفياً أو غير قابل للتعديل
            self.fields['student'].widget = forms.HiddenInput()

class SettlementForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        if self.student:
            payments = self.student.payments.all()
            total_required = payments.aggregate(Sum('required_amount'))['required_amount__sum'] or 0
            total_paid = payments.aggregate(Sum('amount'))['amount__sum'] or 0
            self.fields['amount'].initial = total_required - total_paid
            self.fields['amount'].label = f"المبلغ المتبقي للتسديد ({total_required - total_paid} ل.س)"

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }