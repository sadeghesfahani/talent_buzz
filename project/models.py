from django.db import models

DOCUMENT_MODEL = 'common.Document'
USER_MODEL = 'user.User'


# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    text_requirements = models.TextField()
    json_requirements = models.JSONField()
    hourly_rate = models.IntegerField()
    photo = models.ImageField(upload_to='project')
    category = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    associated_user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    documents = models.ManyToManyField(DOCUMENT_MODEL, related_name='project_documents', blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    freelancers = models.ManyToManyField('user.Freelancer', related_name='freelancers', blank=True)
    reports = models.ManyToManyField(DOCUMENT_MODEL, related_name='project_reports', blank=True)

    def __str__(self):
        return self.title


class Gig(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, related_name='project')
    title = models.CharField(max_length=100)
    description = models.TextField()
    text_requirements = models.TextField()
    json_requirements = models.JSONField()
    hours = models.IntegerField()
    status = models.CharField(max_length=100)
    user = models.ForeignKey('user.Company', on_delete=models.CASCADE)
    documents = models.ManyToManyField(DOCUMENT_MODEL, related_name='gig_documents', blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reports = models.ManyToManyField(DOCUMENT_MODEL, related_name='gig_reports', blank=True)

    def __str__(self):
        return self.title


class GigReport(models.Model):
    freelancer = models.ForeignKey('user.Freelancer', on_delete=models.CASCADE)
    gig = models.ForeignKey('project.Gig', on_delete=models.CASCADE, blank=True, null=True, related_name='gig')
    document = models.ManyToManyField(DOCUMENT_MODEL)
    text = models.TextField()
    hours_spent = models.DecimalField(max_digits=5, decimal_places=2)
    submitted_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=100,
                              choices=[('submitted', 'Submitted'), ('approved', 'Approved'), ('rejected', 'Rejected')])
    reviewed_by = models.ForeignKey(USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='reviewed_reports')
    review = models.JSONField(blank=True)


class ProjectReport(models.Model):
    user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, blank=True, null=True,
                                related_name='project_reports')
    document = models.ForeignKey(DOCUMENT_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='project_report_document')
    text = models.TextField()