"""
URL configuration for resume_summarizer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from resume_app import views
from resume_app.views import ResumeUploadAPI, JobDescriptionCompareAPI, list_resumes, list_job_profiles

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # API endpoint to upload a resume
    path('api/upload/', ResumeUploadAPI.as_view(), name='resume-upload'),

    # API endpoint to compare a resume summary with a job description
    path('api/compare/', JobDescriptionCompareAPI.as_view(), name='compare'),

    # API endpoint to retrieve the list of resumes
    path('api/resumes/', list_resumes, name='resume-list'),

    # API endpoint to retrieve the list of job profiles
    path('api/job-profiles/', list_job_profiles, name='job-profile-list'),
    
    ]
