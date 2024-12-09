// import { bootstrapApplication } from '@angular/platform-browser';
// import { appConfig } from './app/app.config';
// import { AppComponent } from './app/app.component';

// bootstrapApplication(AppComponent, appConfig)
//   .catch((err) => console.error(err));
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { provideHttpClient } from '@angular/common/http';
import { importProvidersFrom } from '@angular/core';
import { CommonModule } from '@angular/common';
import { provideRouter, Route, RouterModule } from '@angular/router';
import { ResumeListComponent } from './app/resume-list.component';
import { JobProfileListComponent } from './app/job-profile-list.component';
import { AppRoutingModule } from './app/app-routing.module'; // Import AppRoutingModule


// Defining the routes 
// const routes: Route[] = [
//   { path: 'resumes', component: ResumeListComponent },
//   { path: 'job-profiles', component: JobProfileListComponent },
//   { path: '', redirectTo: '/resumes', pathMatch: 'full' }
// ];
bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(),
    importProvidersFrom(CommonModule, AppRoutingModule),
    // provideRouter(routes)
  ]
}).catch(err => console.error(err));
