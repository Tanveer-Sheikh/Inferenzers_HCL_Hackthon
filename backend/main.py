from fastapi import FastAPI

app = FastAPI()
jobs = {}


@app.get("/")
def root():
    return {"message": "Backend is working"}

@app.get("/ping")
def ping():
    return {"message": "pong"}

from fastapi import UploadFile, File
import uuid

from fastapi import Form

@app.post("/upload")
def upload(user_id: str = Form(...), file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"filename": file.filename, "status": "completed", "user_id": user_id}
    return {"message": "File received", "filename": file.filename, "job_id": job_id, "user_id": user_id}



@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    if job_id not in jobs:
        return {"error": "Job not found"}

    return {
        "job_id": job_id,
        "user_id": jobs[job_id]["user_id"],  
        "filename": jobs[job_id]["filename"],
        "status": jobs[job_id]["status"],
        "extracted_data": {
            "name": "John Doe",
            "dob": "1992-07-14",
            "phone": "+91-9876543210",
            "email": "john@example.com",
            "address": "Warangal, Telangana"
        },
        "confidence": 0.91
    }

@app.get("/users/{user_id}/jobs")
def get_jobs_for_user(user_id: str):
    user_jobs = []

    for job_id, job_data in jobs.items():
        if job_data["user_id"] == user_id:
            user_jobs.append({
                "job_id": job_id,
                "filename": job_data["filename"],
                "status": job_data["status"]
            })

    return {
        "user_id": user_id,
        "total_jobs": len(user_jobs),
        "jobs": user_jobs
    }

