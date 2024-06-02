from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string


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
    profile_picture = models.ForeignKey('common.Photo', on_delete=models.CASCADE, related_name="profile", null=True, blank=True)

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

    def send_activation_email(self, uidb64, token):
        # Construct the activation link
        activation_link = f"http://simplereminder.ai/activate/{uidb64}/{token}/"

        # Send the email
        subject = "Activate your account"
        # message = f"Click the following link to activate your account: {activation_link}"
        # from_email = "noreply@yourdomain.com"
        #
        # send_mail(subject, message, from_email, [self.email], fail_silently=False)
        # subject = 'Activate Your Account'
        template_name = 'email.html'
        context = {
            'activation_link': activation_link
        }
        message = render_to_string(template_name, context)

        email = EmailMultiAlternatives(
            subject,
            "activation",
            'sadeghesfahani.sina@gmail.com',
            [self.email]
        )

        # Attach HTML content
        email.attach_alternative(message, "text/html")

        # Send the email
        email.send()
        # send_mail(subject, message, 'sadeghesfahani.sina@gmail.com', [self.email])

    def __str__(self):
        return self.first_name + " " + self.last_name + self.username


class Freelancer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    availability = models.JSONField(blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    total_earning = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_job = models.IntegerField(blank=True,null=True)
    skill = models.JSONField(blank=True,null=True)
    language = models.JSONField(blank=True,null=True)
    experience = models.JSONField(blank=True,null=True)
    education = models.JSONField(blank=True,null=True)
    certification = models.JSONField(blank=True,null=True)
    portfolio = models.JSONField(blank=True,null=True)

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
