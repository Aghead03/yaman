from django import forms
from django.forms import modelformset_factory 
from .models import Grade

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'exam_type', 'grade', 'notes', 'classroom']
        widgets = {
            'student': forms.HiddenInput(),
            'subject': forms.HiddenInput(),
            'exam_type': forms.HiddenInput(),
            'classroom': forms.HiddenInput(),
            'grade': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'step': 0.1
            }),
            'notes': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل الملاحظات هنا'
            })
        }

GradeFormSet = modelformset_factory(  
    Grade,
    form=GradeForm,
    extra=0
)