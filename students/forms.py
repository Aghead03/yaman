from django import forms
from .models import Student
from django.forms import DateInput

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'birth_date': DateInput(attrs={'type': 'date'}),
            'registration_date': DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'full_name': 'الاسم الكامل',
            'gender': 'الجنس',
            'branch': 'الصف',
            'birth_date': 'تاريخ الميلاد',
            'tase3':'مجموع التاسع',
            'disease':' امراض الطالب ',
            'student_number': 'رقم الطالب',
            'nationality': 'الجنسية',
            'registration_date': 'تاريخ التسجيل',
            'father_name': 'اسم الأب',
            'father_job': 'عمل الأب',
            'father_phone': 'هاتف الأب',
            'mother_name': 'اسم الأم',
            'mother_job': 'عمل الأم',
            'mother_phone': 'هاتف الأم',
            'address': 'العنوان',
            'home_phone': 'هاتف المنزل',
            'previous_school': 'المدرسة السابقة',
            'elementary_school': 'المدرسة الابتدائية',
            'how_knew_us': 'كيف عرفت المعهد؟',
            'notes': 'ملاحظات'
        }