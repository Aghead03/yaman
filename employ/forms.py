from django import forms
from .models import Teacher , Employee
from django.forms import DateInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group ,User



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
        
        


class EmployeeRegistrationForm(UserCreationForm):
    position = forms.ChoiceField(choices=Employee.POSITION_CHOICES, label='الوظيفة')
    phone_number = forms.CharField(max_length=20, label='رقم الهاتف')
    salary = forms.DecimalField(label='الراتب')
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'اسم المستخدم',
            'first_name': 'الاسم الأول',
            'last_name': 'الاسم الأخير',
            'email': 'البريد الإلكتروني',
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            
            # إنشاء الموظف
            employee = Employee.objects.create(
                user=user,
                position=self.cleaned_data['position'],
                phone_number=self.cleaned_data['phone_number'],
                salary=self.cleaned_data['salary']
            )
            
            # تعيين الصلاحيات حسب الوظيفة
            group_name = self.get_group_name()
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            
        return user
    
    def get_group_name(self):
        position = self.cleaned_data['position']
        return {
            'admin': 'Admins',
            'accountant': 'Accountants',
            'mentor': 'Mentor',
            'manager': 'Managers',
            'marketing': 'Marketing',
            'reception':'Reception',
        }.get(position, 'Employees')        