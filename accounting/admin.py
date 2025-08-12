from django.contrib import admin
from .models import Payment, Transaction

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'amount', 'date', 'payment_method', 'is_full')
    list_filter = ('date', 'payment_method', 'is_full')
    search_fields = ('student__full_name', 'id')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('type', 'amount', 'date', 'description', 'user')
    list_filter = ('type', 'date', 'user')
    search_fields = ('description',)