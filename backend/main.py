from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from openai import OpenAI
from dotenv import load_dotenv
import subprocess
import markdown
from weasyprint import HTML
from pdfminer.high_level import extract_text

# Load environment variables from .env file
load_dotenv()

# Database setup
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@db:5432/resume_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define the database model
class Resume(Base):
    __tablename__ = 'resumes'

    id = Column(Integer, primary_key=True, index=True)
    job_description = Column(String)

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# FastAPI instance
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to store resumes
RESUME_DIR = "resumes"
os.makedirs(RESUME_DIR, exist_ok=True)

# OpenAI API key
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

# Function to convert PDF to text using pdfminer
def convert_pdf_to_md(pdf_path):
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to convert PDF to text: {str(e)}")

# Function to generate PDF from Markdown content
def generate_pdf_from_md(md_content, pdf_path):
    # Convert Markdown to HTML with a consistent style
    html_content = markdown.markdown(md_content, extensions=['extra', 'smarty'])

    # Generate PDF from HTML
    HTML(string=html_content).write_pdf(pdf_path)

# Function to generate updated resume and cover letter using OpenAI
def generate_resume_and_cover_letter(md_resume, job_description, resume_id):
    print("Original Resume:", md_resume)
    # Define the prompt for the AI model to adapt the resume
    resume_prompt = f"""
    I have a resume formatted in Markdown and a job description. \
    Please adapt my resume to better align with the job requirements while \
    maintaining a professional tone. Ensure the resulting resume is Applicant Tracking Systems (ATS) friendly. \
    Ensure ATS best-practices and naming conventions are used. \
    Tailor my skills, experiences, and achievements to highlight the most relevant points for the position. \
    Ensure that my resume still reflects my unique qualifications and strengths \
    but emphasizes the skills and experiences that match the job description. \
    Do not imagine, generate or create false information about my skills or experience. 

    ### Here is my resume in Markdown:
    {md_resume}

    ### Here is the job description:
    {job_description}

    Please modify the resume to:
    - Use keywords and phrases from the job description. Use ATS best-practices where applicable.
    - Adjust (or add) the bullet points under each role to emphasize relevant skills and achievements.
    - Make sure my experiences are presented in a way that matches the required qualifications.
    - Maintain clarity, conciseness, and professionalism throughout.
    """

    # Generate updated resume
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Ensure the model parameter is provided
        messages=[
            {"role": "system", "content": "You are a master 'Applicant Tracking Systems' style resume writer."},
            {"role": "user", "content": resume_prompt}
        ],
        temperature=0.3,
        max_tokens=1500  # Increase the max tokens to ensure the full response is received
    )
    print("Response:", response)
    updated_resume = response.choices[0].message.content

    # # Ensure the response is correctly parsed and formatted
    # if "---" in updated_resume:
    #     updated_resume = updated_resume.split("---")[0].strip()
    print("Updated Resume:", updated_resume)

    # Define the prompt for the AI model to generate a cover letter
    cover_letter_prompt = f"""
    I have a job description and some information about the company. \
    Please write a professional cover letter that is tailored to the job and company. \
    Highlight my relevant skills and experiences, and explain why I am a good fit for the position. \
    Ensure the cover letter is engaging, and persuasive without being overly verbose or promotional. \

    Here is the job description:
    {job_description}

    Return the cover letter in Markdown format.
    """

    # Generate cover letter
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Ensure the model parameter is provided
        messages=[
            {"role": "system", "content": "You are a master 'Applicant Tracking Systems' style resume cover-letter writer."},
            {"role": "user", "content": cover_letter_prompt}
        ],
        temperature=0.25,
        max_tokens=1000  # Increase the max tokens to ensure the full response is received
    )
    cover_letter = response.choices[0].message.content

    # Create directory for the organization
    #os.makedirs(f"Hiring_Organization_{resume_id}", exist_ok=True)

    # Write updated resume and cover letter to files
    # with open(f"Hiring_Organization_{resume_id}/updated_resume.md", "w") as file:
    #     file.write(updated_resume)
    # with open(f"Hiring_Organization_{resume_id}/cover_letter.md", "w") as file:
    #     file.write(cover_letter)

    # Generate PDF from Markdown content
    pdf_path = os.path.join(RESUME_DIR, f"resume_{resume_id}.pdf")
    generate_pdf_from_md(updated_resume, pdf_path)

    return updated_resume, cover_letter

# API to generate resume and cover letter
@app.post("/generate_resume", response_model=dict)
async def generate_resume(file: UploadFile = File(...), job_description: str = Form(...)):
    db = SessionLocal()
    db_resume = Resume(
        job_description=job_description
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)

    # Save the uploaded PDF file
    pdf_path = os.path.join(RESUME_DIR, file.filename)
    with open(pdf_path, "wb") as pdf_file:
        pdf_file.write(file.file.read())

    # Convert PDF to text
    md_resume = convert_pdf_to_md(pdf_path)

    # Generate updated resume and cover letter using OpenAI
    updated_resume, cover_letter = generate_resume_and_cover_letter(md_resume, job_description, db_resume.id)

    db.close()
    return {"message": "Resume and Cover Letter Generated Successfully", "resume_id": db_resume.id, "organization_name": f"Hiring_Organization_{db_resume.id}"}

# API to download resume PDF
@app.get("/download_resume/{resume_id}")
async def download_resume(resume_id: int):
    pdf_path = os.path.join(RESUME_DIR, f"resume_{resume_id}.pdf")
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="Resume not found")
    return FileResponse(pdf_path, media_type='application/pdf', filename=f"resume_{resume_id}.pdf")
