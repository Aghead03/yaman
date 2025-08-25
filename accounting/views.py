from django.views import generic
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count ,Q , F
from datetime import datetime, timedelta
from .models import Payment, Transaction
from django.http import JsonResponse
from .forms import PaymentForm, IncomeForm, ExpenseForm ,SettlementForm
from django.utils import timezone
from students.models import Student
from django.db.models import Case, When, Value, BooleanField


class AccountingHomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'accounting/accounting.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # تحديد التبويب النشط
        active_tab = self.request.GET.get('tab', 'students')
        
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
        
        # التصحيح: حساب أرصدة الطلاب بشكل صحيح
        students = Student.objects.prefetch_related('payments').all().order_by('full_name')
        
        for student in students:
            student.total_required = sum(p.required_amount for p in student.payments.all())
            student.total_paid = sum(p.amount for p in student.payments.all())
            student.balance = student.total_required - student.total_paid
            student.is_paid_in_full = student.balance <= 0
        
        # تصفية الطلاب حسب حالة الدفع
        payment_status = self.request.GET.get('payment_status')
        if payment_status == 'paid':
            students = [s for s in students if s.is_paid_in_full]
        elif payment_status == 'unpaid':
            students = [s for s in students if not s.is_paid_in_full]
        
        context.update({
            'active_tab': active_tab,
            'payments': payments,
            'transactions': transactions,
            'students': students,
            'payment_status_filter': payment_status,
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

    def get_initial(self):
        initial = super().get_initial()
        student_id = self.request.GET.get('student')
        if student_id:
            try:
                student = Student.objects.get(id=student_id)
                initial['student'] = student
            except Student.DoesNotExist:
                pass
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        student_id = self.request.GET.get('student')
        if student_id:
            try:
                kwargs['student'] = Student.objects.get(id=student_id)
            except Student.DoesNotExist:
                pass
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        
        return response


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
        return reverse('accounting:accounting') + '?tab=cash'

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


class StudentAccountView(LoginRequiredMixin, generic.DetailView):
    model = Student
    template_name = 'accounting/student_account.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.object
        payments = student.payments.all().order_by('-date')
        
        # التصحيح: حساب إجمالي المطلوب من جميع الدفعات
        total_required = sum(payment.required_amount for payment in payments)
        
        # التصحيح: حساب إجمالي المدفوع من جميع الدفعات
        total_paid = sum(payment.amount for payment in payments)
        
        balance = total_required - total_paid
        
        context.update({
            'payments': payments,
            'total_required': total_required,
            'total_paid': total_paid,
            'balance': balance,
            'is_paid_in_full': balance <= 0
        })
        return context
    
    
    
    

from django.http import JsonResponse, HttpResponseRedirect



class SettlementCreateView(LoginRequiredMixin, generic.CreateView):
    model = Payment
    form_class = SettlementForm
    template_name = 'accounting/settlement_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        student_id = self.request.GET.get('student')
        if student_id:
            kwargs['student'] = Student.objects.get(id=student_id)
        return kwargs

    def form_valid(self, form):
        student_id = self.request.GET.get('student')
        if student_id:
            student = Student.objects.get(id=student_id)
            payments = student.payments.all()
            total_required = payments.aggregate(Sum('required_amount'))['required_amount__sum'] or 0
            total_paid = payments.aggregate(Sum('amount'))['amount__sum'] or 0
            balance = total_required - total_paid

            if form.instance.amount == balance:
                form.instance.student = student
                form.instance.payment_type = 'installment'
                form.instance.required_amount = form.instance.amount
                form.instance.date = timezone.now().date()
                form.instance.payment_method = 'cash'
                form.instance.created_by = self.request.user
                
                # حفظ النموذج بدون استخدام super().form_valid
                self.object = form.save()
                
                # إنشاء حركة مالية
                Transaction.objects.create(
                    type='income',
                    amount=form.instance.amount,
                    date=form.instance.date,
                    description=f"تسديد حساب الطالب {student.full_name}",
                    user=self.request.user
                )

                return HttpResponseRedirect(reverse('accounting:student_account', kwargs={'pk': student.id}))
            else:
                form.add_error('amount', 'المبلغ المدخل يجب أن يساوي الرصيد المتبقي')
                return self.form_invalid(form)
        return super().form_invalid(form)
import xlwt
from django.http import HttpResponse


class ExportView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        export_type = request.GET.get('export_type', 'excel')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        tab = request.GET.get('tab', 'students')
        
        # تصفية البيانات حسب الفترة
        date_filter = Q()
        if from_date and to_date:
            try:
                date_filter = Q(date__range=[from_date, to_date])
            except (ValueError, TypeError):
                # معالجة خطأ تنسيق التاريخ
                pass
        
        if tab == 'students':
            data = self.export_students(date_filter)
            filename = 'students_report'
        elif tab == 'payments':
            data = self.export_payments(date_filter)
            filename = 'payments_report'
        elif tab == 'cash':
            data = self.export_transactions(date_filter)
            filename = 'cash_flow_report'
        else:
            data = self.export_reports(date_filter)
            filename = 'financial_reports'
        
        if export_type == 'excel':
            return self.export_to_excel(data, filename)
        elif export_type == 'csv':
            return self.export_to_csv(data, filename)
        elif export_type == 'pdf':
            return self.export_to_pdf(data, filename, request)
        
        return HttpResponseRedirect(reverse('accounting:accounting'))
    
    def export_students(self, date_filter):
        students = Student.objects.prefetch_related('payments').all()
        
        data = []
        headers = ['اسم الطالب', 'إجمالي المطلوب', 'إجمالي المدفوع', 'الرصيد', 'الحالة']
        
        for student in students:
            # استخدام aggregate للحصول على المجاميع بشكل أكثر كفاءة
            payments = student.payments.filter(date_filter)
            total_required = payments.aggregate(total=Sum('required_amount'))['total'] or 0
            total_paid = payments.aggregate(total=Sum('amount'))['total'] or 0
            balance = total_required - total_paid
            status = 'مسدد' if balance <= 0 else 'غير مسدد'
            
            data.append([
                student.full_name,
                total_required,
                total_paid,
                balance,
                status
            ])
        
        return {'headers': headers, 'data': data, 'title': 'تقرير حسابات الطلاب'}
    
    def export_payments(self, date_filter):
        payments = Payment.objects.filter(date_filter).select_related('student')
        
        data = []
        headers = ['رقم الإيصال', 'الطالب', 'نوع الدفعة', 'المبلغ المطلوب', 
                'المبلغ المدفوع', 'تاريخ الدفع', 'طريقة الدفع', 'الحالة']
        
        for payment in payments:
            data.append([
                payment.id,
                payment.student.full_name,
                payment.get_payment_type_display(),
                payment.required_amount,
                payment.amount,
                payment.date.strftime('%Y-%m-%d'),
                payment.get_payment_method_display(),
                'مسدد' if payment.is_full else 'جزئي'
            ])
        
        return {'headers': headers, 'data': data, 'title': 'تقرير الدفعات'}
    
    def export_transactions(self, date_filter):
        transactions = Transaction.objects.filter(date_filter).select_related('user')
        
        data = []
        headers = ['التاريخ', 'النوع', 'المبلغ', 'الوصف', 'المستخدم']
        
        for transaction in transactions:
            data.append([
                transaction.date.strftime('%Y-%m-%d'),
                transaction.get_type_display(),
                transaction.amount,
                transaction.description,
                transaction.user.username if transaction.user else ''
            ])
        
        return {'headers': headers, 'data': data, 'title': 'تقرير حركة الصندوق'}
    
    def export_to_excel(self, data, filename):
        try:
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = f'attachment; filename="{filename}.xls"'
            
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Report')
            
            # إضافة العنوان
            title_style = xlwt.XFStyle()
            title_font = xlwt.Font()
            title_font.bold = True
            title_font.height = 16 * 20  # حجم الخط
            title_style.font = title_font
            title_style.alignment = xlwt.Alignment()
            title_style.alignment.horz = xlwt.Alignment.HORZ_CENTER
            
            ws.write_merge(0, 0, 0, len(data['headers'])-1, data['title'], title_style)
            
            # إضافة الرؤوس
            header_style = xlwt.XFStyle()
            header_font = xlwt.Font()
            header_font.bold = True
            header_style.font = header_font
            header_style.alignment = xlwt.Alignment()
            header_style.alignment.horz = xlwt.Alignment.HORZ_CENTER
            
            for col, header in enumerate(data['headers']):
                ws.write(2, col, header, header_style)
                # ضبط عرض الأعمدة تلقائياً
                ws.col(col).width = 256 * (len(str(header)) + 5)
            
            # إضافة البيانات
            for row, row_data in enumerate(data['data'], 3):
                for col, value in enumerate(row_data):
                    # تحديد نمط البيانات الرقمية
                    cell_style = xlwt.XFStyle()
                    if isinstance(value, (int, float)):
                        cell_style.num_format_str = '#,##0.00'
                    ws.write(row, col, value, cell_style)
            
            wb.save(response)
            return response
            
        except Exception as e:
            # معالجة الأخطاء
            return HttpResponse(f"خطأ في التصدير إلى Excel: {str(e)}")