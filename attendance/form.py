from django import forms
from .models import Attendance



class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'classroom', 'date', 'status', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }
        labels = {
            'student': 'الطالب',
            'classroom': 'الشعبة',
            'date': 'التاريخ',
            'status': 'حالة الحضور',
            'notes': 'ملاحظات',
        }