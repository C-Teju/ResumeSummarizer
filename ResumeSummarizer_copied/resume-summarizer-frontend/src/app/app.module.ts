// import { NgModule } from '@angular/core';
// import { BrowserModule } from '@angular/platform-browser';
// import { AppComponent } from './app.component';
// import { HttpClientModule } from '@angular/common/http';
// import { CommonModule } from '@angular/common'; 

// @NgModule({
//   declarations: [
//     // AppComponent // Declare your main component
//   ],
//   imports: [
//     BrowserModule,
//     HttpClientModule,
//     CommonModule // Add this if you're using CommonModule
//   ],
//   providers: [], // Add any services here
//   bootstrap: [] // Bootstrapping the main component
// })
// export class AppModule {}
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app.component';

bootstrapApplication(AppComponent);
