from datetime import timedelta, date

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from finance.models import Invoice

DOCUMENT_MODEL = 'common.Document'
USER_MODEL = 'user.User'
FREELANCER_MODEL = 'user.Freelancer'
COMPANY_MODEL = 'user.Company'


# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    text_requirements = models.TextField()
    json_requirements = models.JSONField(blank=True, null=True)
    hourly_rate = models.IntegerField()
    photo = models.ImageField(upload_to='project', blank=True, null=True)
    category = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    associated_user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    documents = models.ManyToManyField(DOCUMENT_MODEL, related_name='project_documents', blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    freelancers = models.ManyToManyField(FREELANCER_MODEL, related_name='freelancers', blank=True)
    reports = models.ManyToManyField(DOCUMENT_MODEL, related_name='project_reports', blank=True)

    def __str__(self):
        return self.title


class Gig(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_projects')
    title = models.CharField(max_length=100)
    description = models.TextField()
    text_requirements = models.TextField(blank=True)
    json_requirements = models.JSONField(blank=True, null=True)
    hours = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(COMPANY_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='project_users')
    documents = models.ManyToManyField(DOCUMENT_MODEL, related_name='gig_documents', blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reports = models.ManyToManyField(DOCUMENT_MODEL, related_name='gig_reports', blank=True)
    freelancers = models.ManyToManyField(FREELANCER_MODEL, related_name='gig_freelancers', blank=True)
    number_of_freelancers = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title


class GigReport(models.Model):
    freelancer = models.ForeignKey(FREELANCER_MODEL, on_delete=models.CASCADE)
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE, blank=True, null=True, related_name='gig')
    document = models.ManyToManyField(DOCUMENT_MODEL, related_name='gig_report_document', blank=True)
    text = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=100,
                              choices=[('submitted', 'Submitted'), ('approved', 'Approved'), ('rejected', 'Rejected')])
    reviewed_by = models.ForeignKey(USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='reviewed_reports')
    review = models.JSONField(blank=True, null=True)

    @property
    def hours_spent(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return timedelta(0)  # Return zero if either start_time or end_time is None


class ProjectReport(models.Model):
    user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True,
                                related_name='project_reports')
    document = models.ForeignKey(DOCUMENT_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='project_report_document')
    text = models.TextField()


class GigApplication(models.Model):
    freelancer = models.ForeignKey(FREELANCER_MODEL, on_delete=models.CASCADE, related_name='freelancer_application')
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE, related_name='gig_application')
    status = models.IntegerField(choices=[(0, 'Pending'), (1, 'Accepted'), (2, 'Rejected')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.freelancer.user.first_name} applied for {self.gig}'


class ProjectApplication(models.Model):
    freelancer = models.ForeignKey(FREELANCER_MODEL, on_delete=models.CASCADE,
                                   related_name='freelancer_project_application')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_application')
    status = models.IntegerField(choices=[(0, 'Pending'), (1, 'Accepted'), (2, 'Rejected')])


@receiver(post_save, sender=GigReport)
def create_invoice_on_gigreport_approved(sender, instance, **kwargs):
    if instance.status == 'approved':
        # Calculate amount based on hours spent and hourly rate of the gig
        hours_spent = instance.hours_spent.total_seconds() / 3600  # Convert timedelta to hours
        hourly_rate = instance.gig.project.hourly_rate
        amount = hours_spent * hourly_rate

        # Create the invoice
        Invoice.objects.create(
            company=instance.gig.user,
            freelancer=instance.freelancer,
            project=instance.gig.project,
            gig=instance.gig,
            amount=amount,
            status='pending',
            due_date=date.today() + timedelta(days=30)  # Example due date 30 days from now
        )