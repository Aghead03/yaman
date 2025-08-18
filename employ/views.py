from django.shortcuts import render , redirect
from django.views.generic import View , TemplateView ,ListView ,DeleteView , UpdateView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Teacher , Employee
from .forms import TeacherForm ,EmployeeRegistrationForm
from django.contrib import messages
from django.contrib.auth.models import Group

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.forms import AdminPasswordChangeForm




class CreateTeacherView(CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'employ/teacher_form.html'  # تأكد من مسار القالب
    success_url = success_url = '/employ/teachers/'  # أو أي مسار تريد التوجيه إليه  # عدل لمسار قائمة المدرسين
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'تم إضافة المدرس بنجاح')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'حدث خطأ في إدخال البيانات')
        return super().form_invalid(form)
# Create your views here.

class TeacherDeleteView(DeleteView):
    model = Teacher
    success_url = reverse_lazy('employ:teachers')  # استخدام reverse_lazy أفضل من المسار الثابت
    template_name = 'employ/teacher_confirm_delete.html'  # ستحتاج لإنشاء هذا القالب
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'تم حذف المدرس بنجاح')
        return super().delete(request, *args, **kwargs)




class teachers(ListView):
    template_name = 'employ/teachers.html'
    model = Teacher
    context_object_name = 'teacher'
    
class hr(ListView):
    model = Employee
    template_name = 'employ/hr.html'
    context_object_name = 'employees'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        position = self.request.GET.get('position')
        search = self.request.GET.get('search')
        
        if position:
            queryset = queryset.filter(position=position)
        if search:
            queryset = queryset.filter(user__username__icontains=search) | \
            queryset.filter(user__first_name__icontains=search) | \
            queryset.filter(user__last_name__icontains=search)
        return queryset.select_related('user')



def create_groups():
    groups = ['Admins', 'Accountants','Mentor', 'Managers','Marketing','Reception', 'Employees']
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)

class EmployeeCreateView(CreateView):
    form_class = EmployeeRegistrationForm
    template_name = 'employ/employee_form.html'
    success_url = '/employ/hr/'
    
    def get(self, request, *args, **kwargs):
        create_groups() 
        return super().get(request, *args, **kwargs)
    
    
@user_passes_test(lambda u: u.is_superuser)
def select_employee(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        return redirect('employ:employee_update', pk=employee_id)
    
    employees = Employee.objects.all()
    return render(request, 'employ/select_employee.html', {'employees': employees})

class EmployeeUpdateView(UserPassesTestMixin, UpdateView):
    model = Employee  # تغيير من User إلى Employee
    form_class = EmployeeRegistrationForm
    template_name = 'employ/employee_update.html'
    success_url = reverse_lazy('employ:select_employee')

    def test_func(self):
        return self.request.user.is_superuser

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object.user  # تمرير مستخدم الموظف كنموذج
        return kwargs

    def form_valid(self, form):
        # حفظ بيانات المستخدم أولاً
        user = form.save()
        
        # ثم حفظ بيانات الموظف
        employee = self.object
        employee.position = form.cleaned_data['position']
        employee.phone_number = form.cleaned_data['phone_number']
        employee.salary = form.cleaned_data['salary']
        employee.save()
        
        messages.success(self.request, 'تم تحديث بيانات الموظف بنجاح')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # استخدم AdminPasswordChangeForm بدلاً من PasswordChangeForm
        context['password_form'] = AdminPasswordChangeForm(user=self.object.user)
        return context