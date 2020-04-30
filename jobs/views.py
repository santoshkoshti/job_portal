from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import (Job, JobCategory, JOB_TYPE, Location, Company, Applicant)
from django.views.generic import ListView, DetailView, CreateView
# Create your views here.
from django.db.models import Q


def HomeView(request):
    try:
        context = {

            "category": JobCategory.objects.all()[:8],
            "jobss": Job.objects.order_by("-id").filter()[:6],
            "location": Location.objects.all()[:6],
            "company": Company.objects.all()[:6],
        }
    except Exception as e:
        return HttpResponse(e)
    return render(request, "index.html", context)


def JobListView1(request):
    try:
        jobs_list= Job.objects.order_by("-id")   #recently updated
        count = jobs_list.count()
        paginator = Paginator (jobs_list, 4)
        page = request.GET.get('page')
        jobs_list = paginator.get_page(page)

        context = {
            "jobs_list": jobs_list,
            "pagination":jobs_list,
            "count" :count
        }
    except Exception as e:
        return HttpResponse(e)
    return render(request, "jobs_list.html", context)


def categorylist(request):
    try:
        categorylists =JobCategory.objects.all()
        paginator = Paginator(categorylists, 4)
        page = request.GET.get('page')
        categorylists = paginator.get_page(page)
        context = {
            "category_list":categorylists,
            "pagination":categorylists
        }
    except Exception as e:
        return HttpResponse(e)
    return render(request, "categorylist.html", context)


def categoryjobs(request, slug_text):
    try:
        category = JobCategory.objects.filter(slug=slug_text)
        object = Job.objects.filter(category_type=category[0])
        paginator = Paginator(object, 4)
        page = request.GET.get('page')
        object = paginator.get_page(page)
        context = {
            'categorys': category[0],
            "category": object,
            "pagination":object,
        }
    except Exception as e:
        return HttpResponse(e)
    return render(request, "categoryjobs.html", context)


def locationlist(request):
    try:
        locationlists = Location.objects.all()
        paginator = Paginator(locationlists, 4)
        page = request.GET.get('page')
        locationlists = paginator.get_page(page)
        context = {
            "location_list":locationlists,
            "pagination":locationlists
        }
    except Exception as e:
        return HttpResponse(e)
    return render(request, "locationlist.html", context)


def locationjobs(request, slug_text):
    try:
        location = Location.objects.filter(slug=slug_text)
        object = Job.objects.filter(job_location=location[0])
        paginator = Paginator(object, 4)
        page = request.GET.get('page')
        object = paginator.get_page(page)

        context = {
            "location": object,
            'locations': location[0],
            "pagination":object

        }
    except Exception as e:
        return HttpResponse(e)
    return render(request, "locationjobs.html", context)



def job_details(request, slug_text):
    try:
        job = Job.objects.filter(slug=slug_text)[0]
        if request.user.is_authenticated:
            jobappiled= Applicant.objects.filter(
                job_id=job.pk, user_id=request.user
            )
            context = {
                "job": job,
                "jobappiled":jobappiled
            }

        else:
            context = {
                    "job": job,
                }
    except Exception as e:
        return HttpResponse(e)
    return render(request, "job_details.html", context)



def companylist(request):
    try:
        company_lists=Company.objects.all()
        paginator = Paginator(company_lists, 4)
        page = request.GET.get('page')
        company_lists = paginator.get_page(page)
        context = {
            "company_list": company_lists,
            "pagination": company_lists
        }
    except Exception as e:
        return HttpResponse(e)
    return render(request, "companylist.html", context)



def companyjobs(request, slug_text):
    try:
        company = Company.objects.filter(slug=slug_text)
        object = Job.objects.filter(company_name=company[0])
        paginator = Paginator(object, 4)
        page = request.GET.get('page')
        object = paginator.get_page(page)
        context = {
            'company' :company[0],
            "companyjobs": object,
            "pagination": object
        }
    except Exception as e:
        return HttpResponse(e)
    return render(request, "companyjobs.html", context)


def applyjob(request):
    try:
        jobid = request.POST.get("id")
        job = Job.objects.get(pk=jobid)
        jobapplication = Applicant(job=job, user=request.user)
        jobapplication.save()
    except Exception as e:
        return HttpResponse(e)
    return HttpResponse('SUCCESSFULLY APPLIED FOR JOB')



class SearchView(ListView):
    model = Job
    template_name = 'searchresult.html'

    def get_queryset(self):
        if self.request.GET.get('location') == "" and self.request.GET.get('job') == "": #both empty input
            object_list = Job.objects.all()
            return object_list
        else:
            if self.request.GET.get('location') != "" and self.request.GET.get('job') != "": #both filled input
                object_list = Job.objects.filter(title__icontains=self.request.GET.get('job')).filter(job_location__title__icontains=self.request.GET.get('location'))
                return object_list
            elif self.request.GET.get('location') != "": #location only filled
                object_list = Job.objects.filter(job_location__title__icontains=self.request.GET.get('location'))
                return object_list
            elif self.request.GET.get('job') != "": #job search filled
                object_list = Job.objects.filter(title__icontains=self.request.GET.get('job'))
                return object_list


#job saved into database
def postjob(request):
    obj = Job()
    if request.user.is_authenticated:

        if request.method == "POST":
            obj.user_id = request.POST['username']
            obj.title = request.POST['title']
            obj.description = request.POST['description']
            obj.salary = request.POST['salary']
            obj.job_location_id = request.POST['location']
            obj.type = request.POST['type']
            obj.category_type_id = request.POST['category']
            obj.last_date = request.POST['last_date']
            obj.company_name_id = request.POST['company_name']
            # print(title)
            # print(salary)
            # print(location)
            # print(type)
            # print(category)
            # print(last_date)
            obj.save()
            return HttpResponse('SUCCESSFULLY POST YOU JOB')
        else:
            category = JobCategory.objects.all()
            locations = Location.objects.all()
            companys = Company.objects.all()
            context = {
                "category": category,
                "locations":locations,
                "companys":companys
            }
            return render(request,'postjob.html',context)

    else:
        return redirect('login')



def applications(request):
    if request.user.is_authenticated:
        context = {
            "application": Applicant.objects.filter(user=request.user)
        }
        return render(request,"applications.html",context)
    else:
        return redirect('login')




def myjobs(request):
    if request.user.is_authenticated:
        context = {
            "myjobs": Job.objects.filter(user_id=request.user)
        }
        return render(request,"jobapplications.html",context)
    else:
        return redirect('login')


def comingsoon(request):
    return HttpResponse('This page coming soon go to home page <a href="/"> click here</a>')