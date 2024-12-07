from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

import re

from resume_app.models import JobProfile, Resume

from .models import JobProfile, Resume
from .utils import calculate_match_percentage  # Import the helper function for comparing skills
import uuid

from docx import Document
import PyPDF2

import spacy
import indian_names



class ResumeUploadAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        resume_file = request.FILES['file']
        text_content = self.extract_text(resume_file)
        if resume_file:
            summary = self.summarize_resume(text_content)

            # After summarizing, match the skills with predefined job profiles
            matched_profile, match_percentage = self.match_with_job_profiles(summary['Skills'])

            # Generate a unique ID for the resume
            resume_id = uuid.uuid4()

            # Save the resume and the matched job profile in the database
            resume = Resume(
                candidate_name=summary['Name'],
                skills=', '.join(summary['Skills']),
                matched_profile=matched_profile, # Store the closest matching job profile
                match_percentage=match_percentage,
                resume_id=resume_id  # Store the generated unique ID
            )
            print(f"Saved resume with ID: {resume.resume_id}")
            resume.save()
            
             # Link this resume to the matched job profile
            if matched_profile:  # Only add if a profile is matched 
                matched_profile.resumes.add(resume)  # This adds the resume to the 'resumes' ManyToManyField
                matched_profile.save()  # Save the updated JobProfile with the new resume association


     


            # return Response({'summary': summary})
            print(f"Generated resume ID: {resume_id}")

            return Response({'summary': summary, 'resume_id': str(resume_id), 'match_percentage': match_percentage})
        else:
            return Response({"error": "No file uploaded"}, status=400)
       

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
         # Load the spaCy model for English language processing
        nlp = spacy.load('en_core_web_sm')
        # Initialize the Indian names dataset
        # indian_names_set = set(get_first_name, get_full_name, get_last_name)
        indian_names_set = {
        indian_names.get_first_name(),
        indian_names.get_full_name(),
        indian_names.get_last_name()
        }
        # Process the text content using the NLP pipeline
        doc = nlp(text_content)
    
        # Initialize the summary dictionary
        summary = {
                "Name": None,
                "Email": None,
                "Phone": None,
                "Education": [],
                "Experience": [],
                "Skills": []
            }

        # Extract name from the first few lines
        # lines = text_content.split('\n')
        # for line in lines[:5]:  # Check only the first few lines for a name
        #         if len(line.split()) > 1 and not line.startswith('http'):
        #             summary['Name'] = line
        #             break
       # Define common headings that are not likely to be a name

        def extract_name(resume_text):
            # Process the resume text with SpaCy's NER
            doc = nlp(resume_text)
            
            # Look for PERSON entities (name entities)
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    name = ent.text.strip()

                    COMMON_HEADINGS = [
                                "OBJECTIVE", "EXPERIENCE", "EDUCATION", "TECHNICAL SKILLS", "SKILLS", "CERTIFICATIONS", 
                                "PROJECTS", "INTERNSHIP", "WORK EXPERIENCE", "SUMMARY"
                            ]

                    if any(heading in name.upper() for heading in COMMON_HEADINGS):
                        continue
                    # # Optionally, check if the name exists in the Indian names dataset
                    if name in indian_names_set or re.match(r"^[A-Za-z]+ [A-Za-z]+$", name):
                        # If the name is Indian, you can still use it
                    # If SpaCy finds a name, return it
                        return name
                # If no person entity is found, try to extract the name from the first line or first paragraph
                lines = resume_text.split("\n")
                first_line = lines[0].strip()
                # Check if the first line does not contain common patterns like URLs or technical terms
                if not re.search(r"(http[s]?|www\.)", first_line) and len(first_line.split()) > 1:
                    return first_line

            return None  # Return None if no name is found
        # Extract the name
        summary['Name'] = extract_name(text_content) or summary['Name']


        # Use regex to extract email and phone number
        email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        phone_regex = r'\+?\d[\d -]{8,12}\d'
    
        email_match = re.search(email_regex, text_content)
        phone_match = re.search(phone_regex, text_content)
    
        summary["Email"] = email_match.group() if email_match else None
        summary["Phone"] = phone_match.group() if phone_match else None
    

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
            if ent.label_ == "ORG" and any(keyword in ent.text.lower() for keyword in ['college', 'university']):
                summary["Education"].append(ent.text)
            

        # A keyword-based approach to skill extraction
        skill_keywords = ['java', 'python', 'html', 'css', 'javascript', 'sql', 'springboot', 'angular','React','PostgreSQL','MySQL','SQL','Jenkins','Docker','Kubernetes','Pandas','NumPy','Matplotlib','Django','Flask','Node.js','Design','Thinking','Figma','Sketch']
    
        # Token-based analysis for skill extraction
        # 
        # Token-based analysis for skill extraction
        tokens = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]
        for skill in skill_keywords:
            if skill in tokens:
                summary["Skills"].append(skill.capitalize())
        # skill_keywords = [skill.lower() for skill in skill_keywords]

    
        # Remove duplicates and clean up
        summary["Education"] = list(set(summary["Education"]))
        summary["Experience"] = list(set(summary["Experience"]))
        summary["Skills"] = list(set(summary["Skills"]))
    
        # Return the refined summary
        return summary



    def match_with_job_profiles(self, resume_skills):
            # Get all job profiles from the database
            job_profiles = JobProfile.objects.all()  # pylint: disable=no-member
            
            best_profile = None
            best_match_percentage = 0
 
            for profile in job_profiles:
                match_percentage = calculate_match_percentage(resume_skills, profile.required_skills)

                if match_percentage > best_match_percentage:
                    best_match_percentage = match_percentage
                    best_profile = profile
            
            return best_profile, best_match_percentage
    



class JobDescriptionCompareAPI(APIView):
    def post(self, request, *args, **kwargs):
        summary = request.data.get('summary')
        job_description = request.data.get('jobDescription')

        if not summary or not job_description:
            return Response({"error": "Both summary and job description are required"}, status=400)

        # Extract skills from the summary for comparison
        resume_skills = [skill.lower() for skill in summary.get("Skills", [])]
        job_description_skills = [skill.lower().strip() for skill in job_description.split()]

        # Calculate number of matching skills
        matching_skills = set(resume_skills).intersection(job_description_skills)
        matched_count = len(matching_skills)
        total_job_description_skills = len(job_description_skills)

        if total_job_description_skills == 0:
            match_percentage = 0
        else:
            match_percentage = (matched_count / total_job_description_skills) * 100

        match_percentage = round(match_percentage, 2)
        return Response({
            'matchPercentage': match_percentage,
            'matchedSkills': list(matching_skills),
            'totalSkillsInJobDescription': total_job_description_skills,
            'matchedSkillsCount': matched_count
        })




        # def prepare_pivot_data():
#     job_profiles = JobProfile.objects.all()  # Get all job profiles
#     pivot_data_list = []

#     # Prepare data for each job profile
#     for job_profile in job_profiles:
#         resumes_for_profile = Resume.objects.filter(matched_profile=job_profile)
#         # resume_ids = [resume.resume_id for resume in resumes_for_profile]  # Get the resume IDs for the job profile

#         pivot_data_list.append({
#             'job_title': job_profile.job_title,
#             'resumes': [resume.resume_id for resume in resumes_for_profile]  # Store the resume IDs associated with this job profile
#         })

#     return pivot_data_list

# class JobProfilesView(APIView):
#     def get(self, request, *args, **kwargs):
#         # Prepare the pivot data
#         pivot_data_list = prepare_pivot_data()

#         # Get all job profiles for the template
#         # job_profiles = JobProfile.objects.all()

#         context = {
#             'pivot_data': pivot_data_list,
#             'job_profiles': JobProfile.objects.all(),
#         }

#         return render(request, 'admin/job_profiles_pivot.html', context)

# def job_profiles_pivot_view(request):
#     job_profiles = JobProfile.objects.all()
#     pivot_data = {}

#     # Initialize the dictionary with job profiles
#     for profile in job_profiles:
#         pivot_data[profile.job_title] = []

#     # Populate the dictionary with resumes for each job profile
#     for resume in Resume.objects.all():
#         if resume.matched_profile:
#             pivot_data[resume.matched_profile.job_title].append(resume.resume_id)

#     context = {
#         'job_profiles': job_profiles,
#         'pivot_data': pivot_data,
#     }
#     return render(request, 'admin/job_profiles_pivot.html', context)
        