import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class ResumeUploadService {
  private apiUrl = 'http://127.0.0.1:8000/upload/'; // Django backend URL

  constructor(private http: HttpClient) {}

  uploadResume(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);

    return this.http.post(this.apiUrl, formData);
  }
}