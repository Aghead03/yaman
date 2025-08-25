from django.urls import path
from . import views

app_name = 'accounting'

urlpatterns = [
    path('', views.AccountingHomeView.as_view(), name='accounting'),
    
    # الدفعات
    path('payments/add/', views.PaymentCreateView.as_view(), name='add_payment'),
    path('payments/settle/', views.SettlementCreateView.as_view(), name='settle_payment'),
    path('payments/<int:pk>/edit/', views.PaymentUpdateView.as_view(), name='edit_payment'),
    path('payments/<int:pk>/delete/', views.PaymentDeleteView.as_view(), name='delete_payment'),
    path('payments/<int:pk>/receipt/', views.ReceiptDetailView.as_view(), name='receipt'),
    
    # الحركات المالية
    path('income/add/', views.IncomeCreateView.as_view(), name='add_income'),
    path('expense/add/', views.ExpenseCreateView.as_view(), name='add_expense'),
    path('transactions/<int:pk>/edit/', views.TransactionUpdateView.as_view(), name='edit_transaction'),
    path('transactions/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='delete_transaction'),
    
    path('students/<int:pk>/account/', views.StudentAccountView.as_view(), name='student_account'),
    
    path('reports/', views.reports.as_view(), name="reports"),
    path('export/', views.ExportView.as_view(), name='export'),
]