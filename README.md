# Resume Summarizer

## Overview
**Resume Summarizer** is a web application that allows users to upload their resumes in various formats (PDF, DOC, DOCX) and receive a concise summary of their qualifications, education, and experience. Additionally, users can compare their resumes against a job description to see how well they match.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation Instructions](#installation-instructions)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)

## Features
- Upload resumes in PDF, DOC, or DOCX formats.
- Get a detailed summary of the uploaded resume.
- Compare the summarized resume with a job description to obtain a match percentage.
- User-friendly interface built with Angular for the frontend and Django for the backend.

## Technologies Used
- Backend: Django, Django REST Framework
- Frontend: Angular
- Database: SQLite (or your preferred database)
- Languages: Python, JavaScript, HTML, CSS
- Additional Libraries: 
  - `docx2txt` for parsing DOCX files
  - `pdfminer` for parsing PDF files
  - `pandas` for data handling

## Installation Instructions

### Prerequisites
- Python 3.x installed
- Node.js and npm installed
- Angular CLI installed (for frontend)

### Clone the repository

git clone https://github.com/C-Teju/Resume_Summarizer.git
cd Resume_Summarizer

###Backend Setup
Navigate to the backend directory:

cd resume_summarizer
Create a virtual environment (optional but recommended):
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

Install the required packages:
pip install -r requirements.txt

Apply migrations:
python manage.py migrate

Start the Django server:
python manage.py runserver

###Frontend Setup
Open a new terminal window and navigate to the frontend directory:
cd resume_summarizer_frontend

Install the necessary npm packages:
npm install

Start the Angular development server:
ng serve
Open your browser and navigate to http://localhost:4200.

##Usage
Open the application in your web browser.
Upload your resume using the provided upload button.
Wait for the summary to be generated, which will display the key details of your resume.
Enter the job description in the provided textarea and click on the "Compare" button to see the match percentage.

##API Endpoints
  POST /api/summarize/
    Description: Uploads the resume file and returns a summary.
    Request Body: Form-data containing the file.
    Response: JSON object with summarized details (Name, Email, Phone, Education, Experience, Skills).
  POST /api/compare/
    Description: Compares the job description with the summarized resume.
    Request Body: JSON object containing the job description and resume summary.
    Response: JSON object with the match percentage

##Contributing
Contributions are welcome! If you have suggestions for improvements or want to report a bug, feel free to create an issue or submit a pull request.
Fork the repository.
Create a new branch (git checkout -b feature/YourFeature).
Make your changes and commit them (git commit -m 'Add new feature').
Push to the branch (git push origin feature/YourFeature).
Open a pull request.

