# Resume Enhancer

Resume Enhancer is a web application that allows users to upload their resumes in PDF format and generate enhanced resumes and cover letters tailored to specific job descriptions using OpenAI's GPT-3.5 model. The application leverages FastAPI for the backend and React for the frontend.
![Screenshot 2025-01-24 at 11 35 35 AM](https://github.com/user-attachments/assets/3833f52b-090b-4d05-8e9a-d0f91a9b6d0c)

## Features

- Upload PDF resumes
- Convert PDF resumes to text
- Generate enhanced resumes and cover letters based on job descriptions
- Download the generated resumes in PDF format

## Prerequisites

- Docker
- Docker Compose

## Getting Started

### Clone the Repository

To clone the repository, run the following command:

```sh
git clone https://github.com/your-username/resume-enhancer.git
cd resume-enhancer
```

## Setup Environment Variables
Create a .env file in the backend directory with the following content:
```sh
OPENAI_API_KEY=your_openai_api_key
```
## Build and Run the Application
To build and run the application using Docker Compose, run the following command:
```sh
docker-compose up --build
```
This command will build the Docker images for the backend and frontend services and start the application.

## Access the Application
Once the application is running, you can access the frontend at http://localhost:3000 and the backend API at http://localhost:8000.

## Usage
Open the application in your browser.
Upload your PDF resume.
Paste the job description in the provided text area.
Click the "Generate Resume" button.
Download the generated resume and cover letter.


### Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

### License
This project is licensed under the MIT License. See the LICENSE file for details.
