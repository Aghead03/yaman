# views.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from students.models import Student
from employ.models import Employee, Teacher
from accounting.models import Transaction
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum ,Q
from .models import ActivityLog  # استيراد النموذج الجديد

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
        
        # سجل النشاطات الأخيرة من النموذج الجديد
        context['recent_activities'] = ActivityLog.objects.filter(
            Q(user__is_superuser=False) | Q(user__isnull=True)
        ).select_related('user').order_by('-timestamp')[:10]
        return context
    
    
class welcome(TemplateView):
    template_name =   'pages/welcome.html'      