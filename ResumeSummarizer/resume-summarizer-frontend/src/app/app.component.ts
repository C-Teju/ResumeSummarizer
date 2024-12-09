import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ResumeUploadService } from './resume-upload.service';
import { Router } from '@angular/router';
import { ResumeListComponent } from './resume-list.component';
import { JobProfileListComponent } from './job-profile-list.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  standalone: true,
  providers: [ResumeUploadService],
  imports: [CommonModule, FormsModule, ResumeListComponent, JobProfileListComponent],
})
export class AppComponent {
  title = 'resume-summarizer-frontend';
  selectedFile: File | null = null;
  summary: any = null;
  jobDescription: string = '';
  matchPercentage: number | null = null;
  resumeId: string | null = null;
  resumeList: any[] = [];
  jobProfileList: any[] = [];
  resumeUploaded = false;
  selectedResume: any = null;

  constructor(private http: HttpClient, private resumeUploadService: ResumeUploadService, private router: Router) {}

  // File selection
  onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0];
  }

  // Resume Upload
  onSubmit(event: Event): void {
    event.preventDefault();
    if (this.selectedFile) {
      this.resumeUploadService.uploadResume(this.selectedFile).subscribe(
        (response: any) => {
          alert('Resume uploaded successfully!');
          this.summary = response.summary;
          this.resumeId = response.resume_id;
        },
        (error) => {
          console.error('Error uploading resume:', error);
          alert('Error uploading resume. Please try again.');
        }
      );
    }
  }

    // View Resume List
    navigateToResumeList(): void {
      console.log('Navigating to Resume List...');
      // this.router.navigate(['/resumes']);
        // this.fetchResumes();  // Fetch the resume list when navigating
        this.router.navigateByUrl('/resumes').then(() => {
          this.fetchResumes();  // Fetch resumes after navigating
        });
    }
  
    // View Job Profile List
    navigateToJobProfileList(): void {
      console.log('Navigating to Job Profile List...');
      // this.router.navigate(['/job-profiles']);
      //   this.fetchJobProfiles();  // Fetch the job profiles when navigating
      this.router.navigateByUrl('/job-profiles').then(() => {
        this.fetchJobProfiles();  // Fetch job profiles after navigating
      });
    }

  // Fetch Resumes
  fetchResumes(): void {
    this.resumeUploadService.fetchResumes().subscribe(
      (response: any) => {
        console.log('Resumes fetched:', response);
        this.resumeList = response.results || response;
      },
      (error) => {
        console.error('Error fetching resume list:', error);
      }
    );
  }

  // View Resume
  viewResume(resumeId: string): void {
    this.http.get(`http://127.0.0.1:8000/api/resumes/${resumeId}`).subscribe(
      (response: any) => {
        this.selectedResume = response;
        this.jobDescription = '';
        this.matchPercentage = null;
      },
      (error) => {
        console.error('Error fetching resume details:', error);
      }
    );
  }
  compareJobDescription() {
    if (this.summary) {
      const payload = {
        summary: this.summary,
        jobDescription: this.jobDescription,
      };

      this.http.post('http://127.0.0.1:8000/api/compare/', payload).subscribe(
        (response: any) => {
          this.resumeId = response.resume_id;
          this.matchPercentage = response.matchPercentage;
        },
        (error: any) => {
          console.error('Error comparing job description', error);
          this.matchPercentage = null; 
        }
      );
    }
  }

  // Compare Job Description
  // compareJobDescription(): void {
  //   if (this.resumeId && this.jobDescription) {
  //     const payload = {
  //       resume_id: this.resumeId,
  //       job_description: this.jobDescription,
  //     };

  //     this.resumeUploadService.compareJobDescription(payload.resume_id, payload.job_description).subscribe(
  //       (response: any) => {
  //         this.matchPercentage = response.match_percentage;
  //       },
  //       (error) => {
  //         console.error('Error comparing job description:', error);
  //         this.matchPercentage = null;
  //       }
  //     );
  //   }
  // }

  // View Job Profiles
  fetchJobProfiles(): void {
    this.resumeUploadService.fetchJobProfiles().subscribe(
      (response: any) => {
        console.log('Job profiles fetched:', response);
        this.jobProfileList = response.results || response;
      },
      (error: any) => {
        console.error('Error fetching job profile list:', error);
      }
    );
  }
}

