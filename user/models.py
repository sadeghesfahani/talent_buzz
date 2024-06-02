from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


# Create your models here.
class User(AbstractUser):
    password = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=120, blank=True)
    address_1 = models.CharField(max_length=120, blank=True)
    address_2 = models.CharField(max_length=120, blank=True)
    city = models.CharField(max_length=120, blank=True)
    province = models.CharField(max_length=120, blank=True)
    post_code = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.first_name + " " + self.last_name + self.username


class Freelancer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    availability = models.JSONField(blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True)
    total_earning = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    total_job = models.IntegerField(blank=True)
    skill = models.JSONField(blank=True)
    language = models.JSONField(blank=True)
    experience = models.JSONField(blank=True)
    education = models.JSONField(blank=True)
    certification = models.JSONField(blank=True)
    portfolio = models.JSONField(blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Company(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    employees = models.ManyToManyField(User, related_name='employees')
    company_name = models.CharField(max_length=120, blank=True)
    company_logo = models.ImageField(upload_to='company_logo', blank=True)
    company_description = models.TextField(blank=True)
    company_website = models.URLField(max_length=200, blank=True)
    company_size = models.CharField(max_length=120, blank=True)
    company_industry = models.CharField(max_length=120, blank=True)
    company_type = models.CharField(max_length=120, blank=True)
    company_founded = models.DateField(blank=True)
    company_location = models.CharField(max_length=120, blank=True)
    company_specialities = models.JSONField(blank=True)
    company_social_media = models.JSONField(blank=True)

    def __str__(self):
        return self.company_name


class Gig(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField()
    category = models.CharField(max_length=120)
    sub_category = models.CharField(max_length=120)
    requirements = models.JSONField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    documents = models.ManyToManyField('Document', related_name='documents', blank=True)

    def __str__(self):
        return self.title


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " - " + self.document.name
