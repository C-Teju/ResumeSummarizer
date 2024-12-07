from django.contrib import admin
from .models import JobProfile, Resume

from django.utils.html import format_html


from django.urls import path
from django.template.response import TemplateResponse

# Register your models here.

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['candidate_name', 'match_percentage', 'matched_profile', 'resume_id']

@admin.register(JobProfile)
class JobProfileAdmin(admin.ModelAdmin):
    list_display = ['job_title','get_matching_resumes']

    def get_matching_resumes(self, obj):
        # Filter resumes where the matched_profile matches this job profile
        matching_resumes = Resume.objects.filter(matched_profile=obj)
        if matching_resumes.exists():
            # Return resume IDs as a comma-separated string
            return format_html( "<br>".join(str(resume.resume_id) for resume in matching_resumes))
        return "No matching resumes"

    get_matching_resumes.short_description = "Matching Resume IDs"
    get_matching_resumes.allow_tags = True



    # change_list_template = "admin/job_profiles_pivot.html"

    # def changelist_view(self, request, extra_context=None):
    #     job_profiles = JobProfile.objects.all()
    #     resumes = Resume.objects.all()
        
    #     # Create a pivot-like structure
    #     pivot_data = {}
    #     for job_profile in job_profiles:
    #         pivot_data[job_profile.job_title] = [
    #             resume.resume_id for resume in resumes if resume.matched_profile == job_profile
    #         ]
        
    #     extra_context = {"pivot_data": pivot_data, "job_profiles": job_profiles}
    #     return super().changelist_view(request, extra_context=extra_context)

# admin.site.register(JobProfile, JobProfileAdmin)
