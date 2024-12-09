import { Component } from '@angular/core';
import { ResumeUploadService } from './resume-upload.service';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-resume-list',
  templateUrl: './resume-list.component.html',
  standalone: true,
  providers: [ResumeUploadService],
  imports: [CommonModule], // Import CommonModule for *ngFor and *ngIf
})
export class ResumeListComponent {
  resumeList: any[] = [];

  constructor(private resumeUploadService: ResumeUploadService) {
    this.fetchResumes();
  }
  ngOnInit(): void {
    this.fetchResumes();
  }
//   fetchResumes(): void {
//     this.resumeUploadService.fetchResumes().subscribe(
//       (response: any) => {
//         this.resumeList = response.results || response;
//       },
//       (error: any) => {
//         console.error('Error fetching resume list:', error);
//       }
//     );
//   }
// }

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
}
