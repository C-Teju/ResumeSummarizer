import { Component } from '@angular/core';
import { ResumeUploadService } from './resume-upload.service';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-job-profile-list',
  templateUrl: './job-profile-list.component.html',
  standalone: true,
  providers: [ResumeUploadService],
  imports: [CommonModule], // Import CommonModule for *ngFor and *ngIf
})
export class JobProfileListComponent {
  jobProfiles: any[] = [];

  constructor(private resumeUploadService: ResumeUploadService) {
    this.fetchJobProfiles();
  }
  ngOnInit(): void {
    this.fetchJobProfiles();
  }

//   fetchJobProfiles(): void {
//     this.resumeUploadService.fetchJobProfiles().subscribe(
//       (response: any) => {
//         this.jobProfiles = response.results || response;
//       },
//       (error: any) => {
//         console.error('Error fetching job profile list:', error);
//       }
//     );
//   }
fetchJobProfiles(): void {
    this.resumeUploadService.fetchJobProfiles().subscribe(
      (response: any) => {
        console.log('Job profiles fetched:', response);
        this.jobProfiles = response.results || response;
      },
      (error: any) => {
        console.error('Error fetching job profile list:', error);
      }
    );
  }
}


// }
