from django.db import models
import uuid

class JobProfile(models.Model):
    job_title = models.CharField(max_length=225)
    required_skills = models.TextField()  # Comma-separated list of skills
    # resumes = models.ManyToManyField('Resume', related_name='job_profiles', blank=True)  

    def __str__(self):
        return str(self.job_title)
    # def get_matching_resumes(self):
    #     # Filter resumes where the matched_profile equals this job profile's name
    #     matching_resumes = Resume.objects.filter(matched_profile=self.job_title)
    #     # Return the resume_ids of the matched resumes
    #     return [resume.resume_id for resume in matching_resumes]
    

class Resume(models.Model):
    candidate_name = models.CharField(max_length=100)
    skills = models.TextField()  # Summarized skills from the resume
    matched_profile = models.ForeignKey(JobProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="resumes") #CharField(JobProfile,max_length=255, default='No match')  #.ForeignKey(JobProfile, on_delete=models.SET_NULL, null=True, blank=True)
    match_percentage = models.FloatField(null=True)
    resume_id = models.UUIDField(default=uuid.uuid4, unique=True)  # Unique resume ID

    # objects = models.Manager()

    def __str__(self):
        return str(self.resume_id)

   