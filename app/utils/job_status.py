from uuid import uuid4
from enum import Enum
from typing import Dict

class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

jobs: Dict[str, dict] = {}

def create_job() -> str:
    job_id = str(uuid4())
    jobs[job_id] = {"status": JobStatus.PENDING, "result": None, "error": None}
    return job_id

def update_job(job_id: str, status: JobStatus, result=None, error=None):
    if job_id in jobs:
        jobs[job_id].update({"status": status, "result": result, "error": error})

def get_job(job_id: str):
    return jobs.get(job_id, {"status": "unknown"})