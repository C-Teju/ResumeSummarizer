// import { Component } from '@angular/core';
// import { RouterOutlet } from '@angular/router';
// import { ResumeUploadService } from './resume-upload.service';
// import { HttpClient, HttpClientModule } from '@angular/common/http';
// import { CommonModule } from '@angular/common';


// @Component({
//   selector: 'app-root',
//   standalone: true,
//   templateUrl: './app.component.html',
//   styleUrl: './app.component.css',
//   imports: [CommonModule, HttpClientModule]
// })
// export class AppComponent {
//   title = 'resume-summarizer-frontend';
//   selectedFile: File | null = null;
//   summary: any;
//   errorMessage: string | null = null;

//   constructor(private resumeUploadService: ResumeUploadService) {}

//   onFileSelected(event: any) {
//     this.selectedFile = event.target.files[0];
//   }

//   onSubmit() {
//     if (this.selectedFile) {
//       this.resumeUploadService.uploadResume(this.selectedFile).subscribe(
//         (response) => {
//           console.log('Response from backend:', response);
//           this.summary = response.summary; // Display the summary
//           this.errorMessage = null; 
//         },
//         (error) => {
//           console.error('Error uploading file', error);
//           this.errorMessage = 'Error uploading file, please try again.';
//           this.summary = null;
//         }
//       );
//       // this.errorMessage = null;
//     }
//   }
// }


import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { provideHttpClient } from '@angular/common/http';
import { ResumeUploadService } from './resume-upload.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; 

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  standalone: true,
  providers: [
    ResumeUploadService 
  ],
  imports: [CommonModule, FormsModule]
})
export class AppComponent {
  title = 'resume-summarizer-frontend';
  selectedFile: File | null = null;
  summary: any;
  jobDescription: string = ''; 
  matchPercentage: number | null = null;

  constructor(private http: HttpClient, private resumeUploadService: ResumeUploadService) {}

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  onSubmit(event: Event) {
    event.preventDefault();
    if (this.selectedFile) {
      const formData = new FormData();
      formData.append('file', this.selectedFile);
      
      this.http.post('http://127.0.0.1:8000/upload/', formData).subscribe(
        (response:any) => {
          this.summary = response.summary;
          // this.errorMessage = null;
        },
        (error:any) => {
          console.error('Error uploading file', error);
          // this.errorMessage = 'Error uploading file, please try again.';
          this.summary = null; 
        }
      );
    }
  }

  compareJobDescription() {
    if (this.summary) {
      // Send the job description and summary to the backend for comparison
      const payload = {
        summary: this.summary,
        jobDescription: this.jobDescription,
      };

      this.http.post('http://127.0.0.1:8000/compare/', payload).subscribe(
        (response: any) => {
          this.matchPercentage = response.matchPercentage;
        },
        (error: any) => {
          console.error('Error comparing job description', error);
          this.matchPercentage = null; 
        }
      );
    }
  }
  // check if the error handling is proper
}
