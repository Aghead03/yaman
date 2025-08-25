from django.shortcuts import render , redirect
from django.views.generic import View , TemplateView ,ListView ,DeleteView , UpdateView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Teacher , Employee
from .forms import TeacherForm ,EmployeeRegistrationForm
from django.contrib import messages
from django.contrib.auth.models import Group
from attendance.models import TeacherAttendance
from django.utils import timezone


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
    
    
    
class TeacherProfileView(View):
    template_name = 'employ/teacher_profile.html'
    
    def get(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
            
            # الحصول على إحصائيات الحضور
            from django.db.models import Count, Q
            from datetime import datetime, timedelta
            
            today = datetime.now().date()
            month_start = today.replace(day=1)
            year_start = today.replace(month=1, day=1)
            
            
            # إحصائيات اليوم
            daily_attendance = TeacherAttendance.objects.filter(
                teacher=teacher,
                date=today
            ).first()
            
            # إحصائيات الشهر
            monthly_stats = TeacherAttendance.objects.filter(
                teacher=teacher,
                date__gte=month_start,
                date__lte=today
            ).aggregate(
                total_days=Count('id'),
                present_days=Count('id', filter=Q(status='present')),
                absent_days=Count('id', filter=Q(status='absent')),
                total_sessions=Count('session_count')
            )
            
            # إحصائيات السنة
            yearly_stats = TeacherAttendance.objects.filter(
                teacher=teacher,
                date__gte=year_start,
                date__lte=today
            ).aggregate(
                total_days=Count('id'),
                present_days=Count('id', filter=Q(status='present')),
                absent_days=Count('id', filter=Q(status='absent')),
                total_sessions=Count('session_count')
            )
            
            context = {
                'teacher': teacher,
                'branches': teacher.branches.split(',') if teacher.branches else [],
                'daily_attendance': daily_attendance,
                'monthly_stats': monthly_stats,
                'yearly_stats': yearly_stats,
                'today': today,
            }
            return render(request, self.template_name, context)
        except Teacher.DoesNotExist:
            messages.error(request, 'المدرس غير موجود')
            return redirect('employ:teachers')   



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
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'تم إضافة الموظف بنجاح مع تعيين كلمة السر')
        return response
    
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
    
# views.py
class EmployeeDeleteView(UserPassesTestMixin, DeleteView):
    model = Employee
    success_url = reverse_lazy('employ:hr')
    template_name = 'employ/employee_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'تم حذف الموظف بنجاح')
        return super().delete(request, *args, **kwargs)    

# views.py - إضافة هذه الواجهات
from .models import Vacation
from .forms import VacationForm
from django.db.models import Q

class VacationListView(UserPassesTestMixin, ListView):
    model = Vacation
    template_name = 'employ/vacation_list.html'
    context_object_name = 'vacations'
    
    def test_func(self):
        return self.request.user.is_authenticated
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # التصفية حسب اسم الموظف
        employee_name = self.request.GET.get('employee_name')
        if employee_name:
            queryset = queryset.filter(
                Q(employee__user__first_name__icontains=employee_name) |
                Q(employee__user__last_name__icontains=employee_name)
            )
        
        # التصفية حسب التاريخ
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)
        
        return queryset.select_related('employee__user')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employees'] = Employee.objects.all()
        return context

class VacationCreateView(UserPassesTestMixin, CreateView):
    model = Vacation
    template_name = 'employ/vacation_form.html'
    success_url = reverse_lazy('employ:vacation_list')
    
    def test_func(self):
        return self.request.user.is_authenticated
    
    def get_form_class(self):
        # استخدام AdminVacationForm للجميع ليظهر حقل اختيار الموظف
        from .forms import AdminVacationForm
        return AdminVacationForm
    
    def form_valid(self, form):
        form.instance.submission_date = timezone.now().date()
        messages.success(self.request, 'تم تقديم طلب الإجازة بنجاح')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # إضافة قائمة الموظفين للقالب
        context['employees'] = Employee.objects.all()
        return context

class VacationUpdateView(UserPassesTestMixin, UpdateView):
    model = Vacation
    form_class = VacationForm
    template_name = 'employ/vacation_form.html'
    success_url = reverse_lazy('employ:vacation_list')
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user == self.get_object().employee.user
    
    def form_valid(self, form):
        messages.success(self.request, 'تم تحديث طلب الإجازة بنجاح')
        return super().form_valid(form)