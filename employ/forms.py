from django import forms
from .models import Teacher
from django.forms import DateInput

class TeacherForm(forms.ModelForm):
    branches = forms.MultipleChoiceField(
        choices=Teacher.BranchChoices.choices,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=True,
        label='الفروع'
    )

    class Meta:
        model = Teacher
        fields = '__all__'
        widgets = {
            'hire_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        labels = {
            'full_name': 'الاسم الكامل',
            'phone_number': 'رقم الهاتف',
            'id_number': 'رقم الهوية',
            'subject': 'المادة',
            'contract_type': 'نوع العقد',
            'hire_date': 'تاريخ التعيين',
            'notes': 'ملاحظات',
        }