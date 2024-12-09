from rest_framework import serializers
from .models import Resume, JobProfile

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['candidate_name', 'skills', 'matched_profile', 'match_percentage', 'resume_id']

class JobProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobProfile
        fields = ['job_title', 'required_skills']
