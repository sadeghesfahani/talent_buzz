from django.contrib import admin

from .models import Gig, Project, ProjectReport, GigReport

# Register your models here.
admin.site.register(Gig)
admin.site.register(Project)
admin.site.register(ProjectReport)


class GigReportAdmin(admin.ModelAdmin):
    list_display = (
    'freelancer', 'gig', 'submitted_at', 'start_time', 'end_time', 'status', 'reviewed_by', 'hours_spent')
    readonly_fields = ('hours_spent','submitted_at')
    fields = (
    'freelancer', 'gig', 'document', 'text', 'start_time', 'end_time', 'status', 'reviewed_by',
    'review', 'hours_spent')
    def hours_spent(self, obj):
        delta = obj.hours_spent
        return f"{delta.total_seconds() / 3600:.2f} hours"

    hours_spent.short_description = 'Hours Spent'


admin.site.register(GigReport, GigReportAdmin)
