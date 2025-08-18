from django import forms
from .models import Classroom ,ClassroomSubject

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = '__all__'
        widgets = {
            'branches': forms.Select(attrs={'class': 'form-control'}),
            'class_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.class_type == 'course':
            self.fields['branches'].widget = forms.HiddenInput()
        
        
class ClassroomSubjectForm(forms.ModelForm):
    class Meta:
        model = ClassroomSubject
        fields = ['classroom', 'subject']           