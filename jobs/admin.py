from django.contrib import admin
from .models import Location, JobCategory,Company,Job,Applicant
# Register your models here.
admin.site.register(Location)
admin.site.register(Company)
admin.site.register(JobCategory)
admin.site.register(Job)
admin.site.register(Applicant)

