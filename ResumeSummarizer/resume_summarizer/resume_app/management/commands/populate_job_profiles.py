from django.core.management.base import BaseCommand
from resume_app.models import JobProfile



class Command(BaseCommand):
    help = 'Populate the JobProfile table with predefined profiles'

    def handle(self, *args, **kwargs):
        profiles = [
            {"title": "UI Developer (Angular)", "skills": "HTML, CSS, JavaScript, Angular"},
        {"title": "UI Developer (React)", "skills": "HTML, CSS, JavaScript, React"},
        {"title": "UX Designer", "skills": "Design Thinking, Figma, Sketch"},
        {"title": "DBA (Database Administrator)", "skills": "SQL, MySQL, PostgreSQL"},
        {"title": "DevOps (CI/CD)", "skills": "Jenkins, Docker, Kubernetes"},
        {"title": "Python Data Analyst", "skills": "Python, Pandas, NumPy, Matplotlib"},
        {"title": "Backend Developer (Python)", "skills": "Python, Django, Flask"},
        {"title": "Backend Developer (Non-Python)", "skills": "Java, Node.js, SpringBoot"}

            # Add other job profiles as needed
        ]

        for profile in profiles:
            job_profile, created = JobProfile.objects.get_or_create(  # pylint: disable=no-member
                job_title=profile["title"],
                required_skills=profile["skills"]
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created job profile: {profile['title']}"))  # pylint: disable=no-member
            else:
                self.stdout.write(f"Job profile already exists: {profile['title']}")