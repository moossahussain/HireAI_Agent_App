from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Query
import os
import shutil
from typing import Optional, Dict, Any
import uuid
from pydantic import BaseModel
import asyncio

from app.config import settings
from app.crew.agents import create_agents
from app.crew.tasks import create_tasks
from app.utils.file_utils import save_file, read_file

app = FastAPI(title="CrewAI Job Application Assistant")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple API key auth
def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if not settings.API_KEY or x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True

class JobPostingRequest(BaseModel):
    job_posting_url: str
    github_url: Optional[str] = None
    personal_writeup: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Welcome to CrewAI Job Application Assistant API"}

@app.post("/api/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    authenticated: bool = Depends(verify_api_key)
):
    try:
        # Generate a unique ID for the resume
        resume_id = str(uuid.uuid4())
        
        # Save the resume file
        resume_path = await save_file(file, f"resumes/{resume_id}.md")
        
        return {
            "resume_id": resume_id,
            "session_id": resume_id,
            "filename": file.filename,
            "message": "Resume uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload resume: {str(e)}")

@app.post("/api/analyze-job")
async def analyze_job(
    request: JobPostingRequest,
    session_id: str = Query(...,  description="Session ID for resume file association"),
    authenticated: bool = Depends(verify_api_key)

):
    try:
        
        # Import the crew here to avoid circular imports
        from crewai import Crew
        
        # Create agents
        researcher, profiler, resume_strategist, interview_preparer = create_agents(session_id=session_id)
        
        # Create tasks with the provided inputs
        research_task, profile_task, resume_strategy_task, interview_preparation_task = create_tasks(
            researcher, profiler, resume_strategist, interview_preparer,
            job_posting_url=request.job_posting_url,
            github_url=request.github_url,
            personal_writeup=request.personal_writeup,
            session_id=session_id
        )
        
        # Create and kickoff the crew
        job_application_crew = Crew(
            agents=[researcher, profiler, resume_strategist, interview_preparer],
            tasks=[research_task, profile_task, resume_strategy_task, interview_preparation_task],
            verbose=True
        )
        
        # Start processing in the background
        asyncio.create_task(
            process_job_analysis(
                job_application_crew, 
                request.job_posting_url, 
                request.github_url, 
                request.personal_writeup,
                session_id
            )
        )
        
        return {
            "session_id": session_id,
            "message": "Job analysis started",
            "status": "processing"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze job: {str(e)}")

async def process_job_analysis(crew, job_posting_url, github_url, personal_writeup, session_id):
    try:
        # Prepare inputs
        job_application_inputs = {
            'job_posting_url': job_posting_url,
            'github_url': github_url if github_url else "",
            'personal_writeup': personal_writeup if personal_writeup else ""
        }
        
        # Run the crew
        result = crew.kickoff(inputs=job_application_inputs)
        
        # Save results to output files with session ID
        output_dir = f"data/outputs/{session_id}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Move generated files to the output directory
        if os.path.exists("tailored_resume.md"):
            shutil.move("tailored_resume.md", f"{output_dir}/tailored_resume.md")
        
        if os.path.exists("interview_materials.md"):
            shutil.move("interview_materials.md", f"{output_dir}/interview_materials.md")
            
    except Exception as e:
        print(f"Error in background processing: {str(e)}")

@app.get("/api/results/{session_id}")
async def get_results(
    session_id: str,
    authenticated: bool = Depends(verify_api_key)
):
    output_dir = f"data/outputs/{session_id}"
    
    if not os.path.exists(output_dir):
        raise HTTPException(status_code=404, detail="Results not found or still processing")
    
    results = {}
    
    resume_path = f"{output_dir}/tailored_resume.md"
    if os.path.exists(resume_path):
        results["tailored_resume"] = read_file(resume_path)
    
    interview_path = f"{output_dir}/interview_materials.md"
    if os.path.exists(interview_path):
        results["interview_materials"] = read_file(interview_path)
    
    if not results:
        return {"status": "processing", "message": "Results are still being generated"}
    
    return {
        "status": "completed",
        "session_id": session_id,
        "results": results
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)