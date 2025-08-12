from django.views import generic
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count ,Q
from datetime import datetime, timedelta
from .models import Payment, Transaction
from django.http import JsonResponse
from .forms import PaymentForm, IncomeForm, ExpenseForm
from django.utils import timezone

class AccountingHomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'accounting/accounting.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # تحديد التبويب النشط
        active_tab = self.request.GET.get('tab', 'payments')
        
        # بيانات تبويب الدفعات
        payments = Payment.objects.all().order_by('-date')
        
        # تصفية الدفعات
        from_date = self.request.GET.get('from_date')
        to_date = self.request.GET.get('to_date')
        status = self.request.GET.get('status')
        
        if from_date:
            payments = payments.filter(date__gte=from_date)
        if to_date:
            payments = payments.filter(date__lte=to_date)
        if status:
            payments = payments.filter(is_full=(status == 'paid'))
        
        # بيانات تبويب حركة الصندوق
        transactions = Transaction.objects.all().order_by('-date')
        
        # تصفية الحركات المالية
        type_filter = self.request.GET.get('type')
        cash_from_date = self.request.GET.get('cash_from_date', from_date)
        cash_to_date = self.request.GET.get('cash_to_date', to_date)
        
        if cash_from_date:
            transactions = transactions.filter(date__gte=cash_from_date)
        if cash_to_date:
            transactions = transactions.filter(date__lte=cash_to_date)
        if type_filter:
            transactions = transactions.filter(type=type_filter)
        
        # إحصائيات الصندوق (مع التصفية إن وجدت)
        filtered_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        filtered_expenses = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        filtered_balance = filtered_income - filtered_expenses
        
        # إحصائيات عامة (بدون تصفية)
        total_income = Transaction.objects.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = Transaction.objects.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        cash_balance = total_income - total_expenses
        
        # بيانات تبويب التقارير
        # الدفعات الشهرية
        start_date = timezone.now() - timedelta(days=30)
        monthly_payments = Payment.objects.filter(date__gte=start_date).aggregate(
            total=Sum('amount'),
            count=Count('id')
        )
        
        # حركات الصندوق الشهرية
        monthly_transactions = Transaction.objects.filter(date__gte=start_date).aggregate(
            income=Sum('amount', filter=Q(type='income')),
            expense=Sum('amount', filter=Q(type='expense'))
        )
        
        # أعلى طالب مدفوعات
        top_student_payment = Payment.objects.values('student__full_name').annotate(
            total=Sum('amount')
        ).order_by('-total').first()
        
        # أعلى مصروف
        top_expense = Transaction.objects.filter(type='expense').order_by('-amount').first()
        
        # حركات الصندوق للأشهر الستة الماضية للرسم البياني
        months = []
        income_data = []
        expense_data = []
        
        for i in range(6, -1, -1):
            month_start = timezone.now() - timedelta(days=30*i)
            month_name = month_start.strftime('%B')
            months.append(month_name)
            
            income = Transaction.objects.filter(
                type='income',
                date__month=month_start.month,
                date__year=month_start.year
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            expense = Transaction.objects.filter(
                type='expense',
                date__month=month_start.month,
                date__year=month_start.year
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            income_data.append(income)
            expense_data.append(expense)
        
        context.update({
            'active_tab': active_tab,
            'payments': payments,
            'transactions': transactions,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'cash_balance': cash_balance,
            'filtered_income': filtered_income,
            'filtered_expenses': filtered_expenses,
            'filtered_balance': filtered_balance,
            'monthly_payments': {
                'total': monthly_payments['total'] or 0,
                'count': monthly_payments['count'] or 0
            },
            'monthly_transactions': {
                'income': monthly_transactions['income'] or 0,
                'expense': monthly_transactions['expense'] or 0,
                'balance': (monthly_transactions['income'] or 0) - (monthly_transactions['expense'] or 0)
            },
            'top_student': {
                'name': top_student_payment['student__full_name'] if top_student_payment else 'لا يوجد',
                'amount': top_student_payment['total'] if top_student_payment else 0
            },
            'top_expense': top_expense,
            'chart_data': {
                'months': months,
                'income': income_data,
                'expense': expense_data
            }
        })
        
        return context

class PaymentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'accounting/payment_form.html'
    success_url = reverse_lazy('accounting:accounting')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class PaymentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'accounting/payment_form.html'
    success_url = reverse_lazy('accounting:accounting')

class PaymentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Payment
    template_name = 'accounting/payment_confirm_delete.html'
    success_url = reverse_lazy('accounting:accounting')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return JsonResponse({'success': True, 'redirect_url': success_url})

class IncomeCreateView(LoginRequiredMixin, generic.CreateView):
    model = Transaction
    form_class = IncomeForm
    template_name = 'accounting/transaction_form.html'
    def get_success_url(self):
        return reverse('accounting:accounting')

    def form_valid(self, form):
        form.instance.type = 'income'
        form.instance.user = self.request.user
        return super().form_valid(form)

class ExpenseCreateView(LoginRequiredMixin, generic.CreateView):
    model = Transaction
    form_class = ExpenseForm
    template_name = 'accounting/transaction_form.html'
    success_url = reverse_lazy('accounting:accounting')

    def form_valid(self, form):
        form.instance.type = 'expense'
        form.instance.user = self.request.user
        return super().form_valid(form)

class TransactionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Transaction
    template_name = 'accounting/transaction_form.html'
    success_url = reverse_lazy('accounting:accounting') 

    def get_form_class(self):
        if self.object.type == 'income':
            return IncomeForm
        return ExpenseForm

class TransactionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Transaction
    template_name = 'accounting/transaction_confirm_delete.html'
    success_url = reverse_lazy('accounting:accounting')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return JsonResponse({'success': True, 'redirect_url': success_url})

class ReceiptDetailView(LoginRequiredMixin, generic.DetailView):
    model = Payment
    template_name = 'accounting/receipt.html'
    
class reports(generic.TemplateView):
    template_name = 'accounting/reports.html'
