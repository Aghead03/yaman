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
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-control'}),
            'how_knew_us': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'full_name': 'الاسم الكامل للطالب',
            'gender': 'الجنس',
            'branch': 'الصف الدراسي',
            'birth_date': 'تاريخ الميلاد',
            'tase3': 'مجموع الصف التاسع',
            'disease': 'الأمراض أو الحالات الصحية',
            'student_number': 'رقم الطالب',
            'nationality': 'الجنسية',
            'registration_date': 'تاريخ التسجيل',
            'father_name': 'اسم الأب',
            'father_job': 'مهنة الأب',
            'father_phone': 'هاتف الأب',
            'mother_name': 'اسم الأم',
            'mother_job': 'مهنة الأم',
            'mother_phone': 'هاتف الأم',
            'address': 'العنوان',
            'home_phone': 'هاتف المنزل',
            'previous_school': 'المدرسة السابقة',
            'elementary_school': 'المدرسة الابتدائية',
            'how_knew_us': 'كيفية معرفة المعهد',
            'notes': 'ملاحظات'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # جعل الحقول مطلوبة
        for field_name, field in self.fields.items():
            if field_name not in ['how_knew_us', 'notes', 'mother_name', 'mother_job', 
                                'mother_phone', 'previous_school', 'elementary_school', 
                                'father_job', 'added_by']:
                field.required = True
            field.widget.attrs.update({'class': 'form-control'})
        
        # إزالة حقل added_by من النموذج لأنه سيتم تعبئته تلقائيًا
        self.fields.pop('added_by', None)
            
        # تخصيص خيارات القوائم المنسدلة
        self.fields['gender'].choices = [
            ('', 'اختر الجنس'),
            ('male', 'ذكر'),
            ('female', 'أنثى')
        ]
        
        self.fields['branch'].choices = [
            ('', 'اختر الصف الدراسي'),
            ('أدبي', 'الأدبي'),
            ('علمي', 'العلمي'),
            ('تاسع', 'الصف التاسع')
        ]
        
        self.fields['how_knew_us'].choices = [
            ('', 'اختر طريقة المعرفة'),
            ('friend', 'صديق'),
            ('social', 'وسائل التواصل الاجتماعي'),
            ('ad', 'إعلان'),
            ('ads', 'إعلانات طرقية'),
            ('other', 'أخرى')
        ]