import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ResumeUploadService {
  private baseUrl = 'http://127.0.0.1:8000/api/'; // Updated base URL

  constructor(private http: HttpClient) {}

  uploadResume(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);

    return this.http.post(`${this.baseUrl}upload/`, formData);
  }

  compareJobDescription(resumeId: string, jobDescription: string): Observable<any> {
    return this.http.post(`${this.baseUrl}compare/`, {
      resume_id: resumeId,
      job_description: jobDescription,
    });
  }

  fetchResumes(): Observable<any> {
    return this.http.get(`${this.baseUrl}resumes/`);
  }

  fetchJobProfiles(): Observable<any> {
    return this.http.get(`${this.baseUrl}job-profiles/`);
  }
}
