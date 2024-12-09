import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { ResumeListComponent } from './resume-list.component';
import { JobProfileListComponent } from './job-profile-list.component';

const routes: Routes = [
  { path: '', component: AppComponent }, // Home page
  { path: 'resumes', component: ResumeListComponent }, // Resume list page
  { path: 'job-profiles', component: JobProfileListComponent }, // Job profile list page
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
