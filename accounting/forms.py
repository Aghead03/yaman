from django import forms
from .models import Payment, Transaction

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student', 'amount', 'date', 'payment_method', 'is_full', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

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