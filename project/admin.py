from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from .models import Gig, Project, ProjectReport, GigReport, GigApplication, ProjectApplication

# Register your models here.
admin.site.register(Gig)
admin.site.register(Project)
admin.site.register(ProjectReport)
admin.site.register(ProjectApplication)


class GigReportAdmin(admin.ModelAdmin):
    list_display = (
        'freelancer', 'gig', 'submitted_at', 'start_time', 'end_time', 'status', 'reviewed_by', 'hours_spent')
    readonly_fields = ('hours_spent', 'submitted_at')
    fields = (
        'freelancer', 'gig', 'document', 'text', 'start_time', 'end_time', 'status', 'reviewed_by',
        'review', 'hours_spent')

    def hours_spent(self, obj):
        delta = obj.hours_spent
        return f"{delta.total_seconds() / 3600:.2f} hours"

    hours_spent.short_description = 'Hours Spent'


class GigApplicationAdmin(admin.ModelAdmin):
    list_display = ('freelancer', 'gig', 'status', 'created_at')
    list_filter = ('status',('created_at', DateFieldListFilter))


admin.site.register(GigApplication, GigApplicationAdmin)
admin.site.register(GigReport, GigReportAdmin)
