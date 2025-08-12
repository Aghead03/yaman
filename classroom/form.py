from django import forms
from .models import Classroom ,ClassroomSubject

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = '__all__'
        
        
class ClassroomSubjectForm(forms.ModelForm):
    class Meta:
        model = ClassroomSubject
        fields = ['classroom', 'subject']           