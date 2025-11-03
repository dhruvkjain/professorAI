from concurrent.futures import ThreadPoolExecutor
from fastapi import APIRouter, HTTPException
from app.pipelines.manim_pipeline import process_manim_script_pipeline
from app.utils.job_status import create_job, update_job, get_job, JobStatus

router = APIRouter()
executor = ThreadPoolExecutor(max_workers=4)

@router.post("/generate/")
async def generate_manim_code(subject: str, syllabus_job_id: str):
    """
    Generates Manim videos based on the syllabus JSON produced by the syllabus pipeline.
    
    Args:
        subject: The subject name (e.g., "Mathematics")
        syllabus_job_id: The job ID of the completed syllabus extraction
    """
    # retrieve syllabus job data
    syllabus_job = get_job(syllabus_job_id)
    if not syllabus_job:
        raise HTTPException(status_code=404, detail="Syllabus job not found")

    if syllabus_job["status"] != JobStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Syllabus job not completed yet")

    syllabus_data = syllabus_job["result"]["data"]
    if not syllabus_data:
        raise HTTPException(status_code=400, detail="No syllabus data found in job result")

    job_id = create_job()

    def run_manim():
        try:
            update_job(job_id, JobStatus.RUNNING)
            result = process_manim_script_pipeline(subject, syllabus_data)
            update_job(job_id, JobStatus.COMPLETED, result=result)
        except Exception as e:
            update_job(job_id, JobStatus.FAILED, error=str(e))

    executor.submit(run_manim)
    return {"job_id": job_id, "status": "queued"}


@router.get("/status/{job_id}")
async def get_manim_status(job_id: str):
    """
    Check the current status of a Manim generation job.
    """
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
