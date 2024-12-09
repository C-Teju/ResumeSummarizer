from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view

import re
import uuid
import spacy
from docx import Document
import PyPDF2
import indian_names

from resume_app.models import JobProfile, Resume
from .serializers import ResumeSerializer, JobProfileSerializer
from .utils import calculate_match_percentage


class ResumeUploadAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        resume_file = request.FILES.get('file')
        if not resume_file:
            return Response({"error": "No file uploaded"}, status=400)

        text_content = self.extract_text(resume_file)
        summary = self.summarize_resume(text_content)
        matched_profile, match_percentage = self.match_with_job_profiles(summary['Skills'])

        # Generate a unique ID for the resume
        resume_id = uuid.uuid4()

        # Save the resume in the database
        resume = Resume(
            candidate_name=summary['Name'],
            skills=', '.join(summary['Skills']),
            matched_profile=matched_profile,
            match_percentage=match_percentage,
            resume_id=resume_id
        )
        resume.save()

        # Link the resume to the matched job profile
        if matched_profile:
            matched_profile.resumes.add(resume)
            matched_profile.save()

        return Response({
            'summary': summary,
            'resume_id': str(resume_id),
            'match_percentage': match_percentage
        })

    def extract_text(self, resume_file):
        if resume_file.name.endswith('.docx'):
            doc = Document(resume_file)
            return '\n'.join([para.text for para in doc.paragraphs])
        elif resume_file.name.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(resume_file)
            return '\n'.join([page.extract_text() for page in pdf_reader.pages])
        else:
            raise ValueError("Unsupported file format. Please upload a .pdf or .docx file.")

    def summarize_resume(self, text_content):
        nlp = spacy.load('en_core_web_sm')
        indian_names_set = {
            indian_names.get_first_name(),
            indian_names.get_full_name(),
            indian_names.get_last_name()
        }

        doc = nlp(text_content)
        summary = {
            "Name": None,
            "Email": None,
            "Phone": None,
            "Education": [],
            "Experience": [],
            "Skills": []
        }

        def extract_name(resume_text):
            doc = nlp(resume_text)
            for ent in doc.ents:
                if ent.label_ == "PERSON" and ent.text.strip() not in indian_names_set:
                    return ent.text.strip()
            return None

        summary['Name'] = extract_name(text_content)
        email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        phone_regex = r'\+?\d[\d -]{8,12}\d'
        summary["Email"] = re.search(email_regex, text_content).group() if re.search(email_regex, text_content) else None
        summary["Phone"] = re.search(phone_regex, text_content).group() if re.search(phone_regex, text_content) else None

                # Define the regex pattern to extract experience (months or years or both)
        experience_pattern = r'(\d+\.?\d*)\s?(months?|years?)'
        # Search for experience mentions
        experience_matches = re.findall(experience_pattern, text_content.lower())
        # Extract the experience and normalize it (convert to months)
        for match in experience_matches:
            duration, unit = match
            duration = float(duration)  # Convert to float to handle cases like 1.5 or 3.5
            if 'month' in unit:
                summary["Experience"].append(f"{int(duration)} months")
            elif 'year' in unit:
                # Convert years to months
                months = int(duration * 12)
                summary["Experience"].append(f"{months} months")
        if not summary["Experience"]:
            summary["Experience"].append("Fresher")


        # Extract entities and classify them
        for ent in doc.ents:
            if ent.label_ == "ORG" and any(keyword in ent.text.lower() for keyword in ['college', 'university','school','institute']):
                summary["Education"].append(ent.text)
            

        skill_keywords = ['java', 'python', 'html', 'css', 'javascript', 'sql', 'django', 'react', 'angular', 'flask']
        tokens = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]
        summary["Skills"] = [skill.capitalize() for skill in skill_keywords if skill in tokens]
        summary["Education"] = list(set(summary["Education"]))
        summary["Experience"] = list(set(summary["Experience"]))
        
    

        return summary

    def match_with_job_profiles(self, resume_skills):
        job_profiles = JobProfile.objects.all()
        best_profile, best_match_percentage = None, 0
        for profile in job_profiles:
            match_percentage = calculate_match_percentage(resume_skills, profile.required_skills)
            if match_percentage > best_match_percentage:
                best_profile, best_match_percentage = profile, match_percentage
        return best_profile, best_match_percentage


class JobDescriptionCompareAPI(APIView):
    def post(self, request, *args, **kwargs):
        summary = request.data.get('summary')
        job_description = request.data.get('jobDescription')
        if not summary or not job_description:
            return Response({"error": "Both summary and job description are required"}, status=400)

        resume_skills = [skill.lower() for skill in summary.get("Skills", [])]
        job_description_skills = [skill.lower().strip() for skill in job_description.split()]
        matching_skills = set(resume_skills).intersection(job_description_skills)

        match_percentage = (
            (len(matching_skills) / len(job_description_skills)) * 100
            if job_description_skills else 0
        )

        return Response({
            'matchPercentage': round(match_percentage, 2),
            'matchedSkills': list(matching_skills),
            'totalSkillsInJobDescription': len(job_description_skills),
            'matchedSkillsCount': len(matching_skills)
        })


@api_view(['GET'])
def list_resumes(request):
    resumes = Resume.objects.all()
    serializer = ResumeSerializer(resumes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def list_job_profiles(request):
    job_profiles = JobProfile.objects.all()
    data = [{
        "job_profile": profile.job_title,
        "required_skills": profile.required_skills,
        "matched_resumes": ResumeSerializer(profile.resumes.all(), many=True).data
    } for profile in job_profiles]
    return Response(data)
