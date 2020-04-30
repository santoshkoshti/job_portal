from django.urls import path
from jobs import views
from .views import *



urlpatterns = [
    path('', views.HomeView, name='home'),
    # path('jobs/', JobListView.as_view(), name='jobs'),
    path('jobss/', views.JobListView1, name='jobss'),
    path('categorylist/', views.categorylist, name='categorylist'),
    path('categoryjobs/<slug:slug_text>', views.categoryjobs, name='category-jobs'),
    path('locationlist/', views.locationlist, name='locationlist'),
    path('locationjobs/<slug:slug_text>', views.locationjobs, name='location-jobs'),
    path('job_details/<slug:slug_text>', views.job_details, name='job-details'),
    path('companylist/', views.companylist, name='companylist'),
    path('companyjobs/<slug:slug_text>', views.companyjobs, name='company-jobs'),
    path("applyjob/", views.applyjob, name="applyjob"),
    path('comingsoon/', views.comingsoon, name='commingsoon'),
    path('search', SearchView.as_view(), name='search'),
    path('postjob', views.postjob, name='postjob'),
    path('applications/', views.applications, name='applications'),
    path('myjobs/', views.myjobs, name='myjobs'),

]