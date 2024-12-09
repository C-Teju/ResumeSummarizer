from rest_framework import serializers
from .models import Resume, JobProfile

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['resume_id', 'candidate_name', 'skills', 'summary', 'file']  # Include relevant fields


class JobProfileSerializer(serializers.ModelSerializer):
    matched_resume_ids = serializers.SerializerMethodField()

    class Meta:
        model = JobProfile
        fields = ['job_title', 'matched_resume_ids']

    def get_matched_resume_ids(self, obj):
        return obj.resumes.values_list('resume_id', flat=True)  # Extract IDs
