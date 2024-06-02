from django.db import models


# Create your models here.
class Invoice(models.Model):
    # Related models
    company = models.ForeignKey('user.Company', on_delete=models.CASCADE, related_name='finance_companies', blank=True)
    freelancer = models.ForeignKey('user.Freelancer', on_delete=models.CASCADE, related_name='freelancer', blank=True)
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, related_name='finance_projects',
                                blank=True)
    gig = models.ForeignKey('project.Gig', on_delete=models.CASCADE, related_name='finance_gigs', blank=True)

    # Financial details
    amount = models.IntegerField()
    paid_amount = models.IntegerField(blank=True, null=True)
    received_amount = models.IntegerField(blank=True, null=True)
    transaction_fee = models.IntegerField(blank=True, null=True)

    # Invoice details
    status = models.CharField(max_length=100, blank=True)
    due_date = models.DateField()
    notes = models.TextField(blank=True)
    document = models.ManyToManyField('common.Document', related_name='invoice_document', blank=True)
    invoice_number = models.CharField(max_length=100, blank=True)
    tax = models.IntegerField(blank=True, null=True)

    # Currency details
    paid_currency = models.CharField(max_length=100, blank=True)
    received_currency = models.CharField(max_length=100, blank=True)
    transaction_fee_currency = models.CharField(max_length=100)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(blank=True, null=True)
