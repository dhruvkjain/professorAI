from fastapi import APIRouter, BackgroundTasks
from app.pipelines.syllabus_pipeline import process_syllabus_pipeline
from app.utils.job_status import create_job, update_job, get_job, JobStatus

router = APIRouter()

@router.post("/generate/")
async def generate_syllabus(subject: str, pdf_path: str, background_tasks: BackgroundTasks):
    """
    Orchestrates:
      1. Extract syllabus from PDF
      2. Identify chapter dependencies
      3. Generate QA pairs
      4. Generate video scripts
      5. Push graph to Neo4j and generate a visualization using pyvis in html
    """
    
    job_id = create_job()

    def run_pipeline():
        try:
            update_job(job_id, JobStatus.RUNNING)
            result = process_syllabus_pipeline(subject, pdf_path)
            update_job(job_id, JobStatus.COMPLETED, result=result)
        except Exception as e:
            update_job(job_id, JobStatus.FAILED, error=str(e))

    background_tasks.add_task(run_pipeline)
    return {"job_id": job_id, "status": "queued"}

@router.get("/status/{job_id}")
async def get_status(job_id: str):
    """
    Fetch current status or result of a syllabus generation job.
    """
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job