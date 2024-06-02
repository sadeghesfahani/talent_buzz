from django.contrib import admin

from .models import User, Company, Freelancer


# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
    'company_name', 'owner', 'company_website', 'company_size', 'company_industry', 'company_type', 'company_founded',
    'company_location')
    search_fields = ('company_name', 'company_industry', 'company_type', 'company_location')
    list_filter = ('company_size', 'company_industry', 'company_type', 'company_founded')
    readonly_fields = ('owner',)
    fieldsets = (
        (None, {
            'fields': ('owner', 'company_name', 'company_logo', 'company_description', 'company_website')
        }),
        ('Company Details', {
            'fields': ('company_size', 'company_industry', 'company_type', 'company_founded', 'company_location')
        }),
        ('Specialities & Social Media', {
            'fields': ('company_specialities', 'company_social_media')
        }),
    )


admin.site.register(Company, CompanyAdmin)

admin.site.register(User)
admin.site.register(Freelancer)
