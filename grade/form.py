from django import forms
from .models import Grade
from courses.models import Subject

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'grade', 'exam_type', 'notes']

    def __init__(self, *args, **kwargs):
        subject_choices = kwargs.pop('subject_choices', None)
        classroom_id = kwargs.pop('classroom_id', None)
        super().__init__(*args, **kwargs)
        
        if subject_choices:
            subjects = [cs.subject for cs in subject_choices]
            self.fields['subject'].queryset = Subject.objects.filter(
                id__in=[s.id for s in subjects]
            )
        
        if classroom_id:
            self.fields['student'].queryset = self.fields['student'].queryset.filter(
                classroom_enrollments__classroom_id=classroom_id
            )