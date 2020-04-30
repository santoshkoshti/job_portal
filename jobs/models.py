from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import pre_save

# from accounts.models import User
from portal.suglify import unique_slug_generator

JOB_TYPE = (
    ('Full Time', "Full time"),
    ('Part time', "Part time"),
    ('Intership', "Internship"),
)

class Company(models.Model):
    title = models.CharField(max_length=500,default="paralleldesk")
    slug = models.SlugField(max_length=500,null=True,blank=True)
    company_address = models.TextField(null=True, blank=True)
    company_description = models.CharField(max_length=300)
    website = models.CharField(max_length=100, default="")
    email = models.EmailField(max_length=200, null=True, blank=True)
    phone = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title


class JobCategory(models.Model):
    title = models.CharField(max_length=500,default="System Admin")
    slug = models.SlugField(max_length=500,null=True,blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title



class Location(models.Model):
    title = models.CharField(max_length=500,default="Bangalore")
    slug = models.SlugField(max_length=500,null=True,blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500,null=True,blank=True)
    description = models.TextField()
    type = models.CharField(choices=JOB_TYPE, max_length=10)
    last_date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)
    salary = models.IntegerField(default=0, blank=True)
    category_type = models.ForeignKey(
        JobCategory, on_delete=models.CASCADE,
    )
    company_name = models.ForeignKey(
        Company, on_delete=models.CASCADE,
    )
    job_location = models.ForeignKey(
        Location, on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('job-details', args=[str(self.slug)])

class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.job



def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Job)
pre_save.connect(slug_generator, sender=JobCategory)
pre_save.connect(slug_generator, sender=Company)
pre_save.connect(slug_generator, sender=Location)
# class Applicant(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants')
#     created_at = models.DateTimeField(default=timezone.now)
#
#     def __str__(self):
#         return self.user.get_full_name()
