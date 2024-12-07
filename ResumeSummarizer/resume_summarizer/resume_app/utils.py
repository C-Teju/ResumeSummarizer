# utils.py
    # Function to compare resume skills with job profile skills and return a percentage match.

def calculate_match_percentage(resume_skills, profile_skills):
    resume_skill_set = set([skill.strip().lower() for skill in resume_skills])

    profile_skill_set = set([skill.strip().lower() for skill in profile_skills.split(",")])

    total_skills = len(profile_skill_set)
    matching_skills = len(resume_skill_set.intersection(profile_skill_set))

    if total_skills == 0:
        return 0
    return (matching_skills / total_skills) * 100

# #santhu added the below code and commented the above
# def calculate_match_percentage(resume_skills, job_skills):
#     resume_skills_set = set(resume_skills.lower().split(', '))
#     job_skills_set = set(job_skills.lower().split(', '))
#     matched_skills = resume_skills_set.intersection(job_skills_set)
    
#     if not job_skills_set:
#         return 0.0
    
#     return round((len(matched_skills) / len(job_skills_set)) * 100, 2)
