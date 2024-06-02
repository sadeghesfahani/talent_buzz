from django.contrib import admin
from .models import Invoice
# Register your models here.

class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_number', 'company', 'freelancer', 'project', 'gig',
        'amount', 'paid_amount', 'status', 'due_date', 'created_at', 'paid_at'
    )
    search_fields = (
        'invoice_number', 'company__company_name', 'freelancer__user__first_name',
        'freelancer__user__last_name', 'project__title', 'gig__title'
    )
    list_filter = (
        'status', 'due_date', 'created_at', 'paid_at',
        'paid_currency', 'received_currency', 'transaction_fee_currency'
    )
    readonly_fields = ('created_at', 'updated_at', 'paid_at')
    fieldsets = (
        (None, {
            'fields': ('invoice_number', 'status', 'notes')
        }),
        ('Related Entities', {
            'fields': ('company', 'freelancer', 'project', 'gig')
        }),
        ('Financial Details', {
            'fields': (
                'amount', 'paid_amount', 'received_amount', 'transaction_fee',
                'tax', 'paid_currency', 'received_currency', 'transaction_fee_currency'
            )
        }),
        ('Dates', {
            'fields': ('due_date', 'created_at', 'updated_at', 'paid_at')
        }),
        ('Documents', {
            'fields': ('document',)
        }),
    )

admin.site.register(Invoice, InvoiceAdmin)