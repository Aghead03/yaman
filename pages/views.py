from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from students.models import Student
from employ.models import Employee
from accounting.models import Transaction
from django.contrib.admin.models import LogEntry
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from django.db.models import Q
from employ.models import Teacher

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # إحصائيات الطلاب والمدرسين
        context['students_count'] = Student.objects.count()
        context['teachers_count'] = Teacher.objects.count()
        # حساب الدخل والمصروفات الشهرية
        start_date = timezone.now().replace(day=1)
        end_date = start_date + timedelta(days=31)
        
        context['monthly_income'] = Transaction.objects.filter(
            type='income',
            date__gte=start_date,
            date__lte=end_date
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        context['monthly_expenses'] = Transaction.objects.filter(
            type='expense',
            date__gte=start_date,
            date__lte=end_date
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # سجل النشاطات الأخيرة
        context['recent_activities'] = LogEntry.objects.select_related('user').order_by('-action_time')[:10]
        
        return context