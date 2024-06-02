from django.contrib import admin
from .models import User,Gig,Company,Document,Freelancer
# Register your models here.


admin.site.register(User)
admin.site.register(Gig)
admin.site.register(Company)
admin.site.register(Document)
admin.site.register(Freelancer)
