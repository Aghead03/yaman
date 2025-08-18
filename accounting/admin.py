from django.contrib import admin
from .models import Payment, Transaction
from django.db.models import Sum, Count ,Q , F


class IsFullFilter(admin.SimpleListFilter):
    title = 'حالة الدفع'
    parameter_name = 'is_full'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'مسدد بالكامل'),
            ('no', 'جزئي'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(amount__gte=F('required_amount'))
        if self.value() == 'no':
            return queryset.filter(amount__lt=F('required_amount'))

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'payment_type', 'required_amount', 'amount', 'date', 'payment_method', 'payment_status')
    list_filter = ('date', 'payment_method', 'payment_type', IsFullFilter)
    search_fields = ('student__full_name', 'id')
    
    def payment_status(self, obj):
        return "مسدد" if obj.is_full else "جزئي"
    payment_status.short_description = 'حالة الدفع'

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('type', 'amount', 'date', 'description', 'user')
    list_filter = ('type', 'date', 'user')
    search_fields = ('description',)