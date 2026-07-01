from pathlib import Path
from threading import Lock, Thread
from time import time
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from crew import run_omnithesis_crew

app = FastAPI(title="OmniThesis AI Backend")
BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if FRONTEND_DIR.exists():
    app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")


JOBS: dict[str, dict] = {}
JOBS_LOCK = Lock()
STAGE_ORDER = ["research", "domain", "curation", "feasibility", "writing", "editing"]
STAGE_INDEX = {stage: index for index, stage in enumerate(STAGE_ORDER)}
STAGE_ESTIMATE_SECONDS = 18


class GenerateReportRequest(BaseModel):
    topic: str
    python_skill_level: str | None = None
    ml_experience: str | None = None
    additional_background: str | None = None


def _create_job(payload: GenerateReportRequest) -> str:
    job_id = str(uuid4())
    now = time()

    with JOBS_LOCK:
        JOBS[job_id] = {
            "job_id": job_id,
            "status": "queued",
            "stage": None,
            "stage_state": None,
            "message": "Queued",
            "topic": payload.topic,
            "background": None,
            "report": None,
            "error": None,
            "started_at": now,
            "updated_at": now,
            "elapsed_seconds": 0,
            "estimated_remaining_seconds": STAGE_ESTIMATE_SECONDS * len(STAGE_ORDER),
        }

    return job_id


def _update_job(job_id: str, **changes):
    with JOBS_LOCK:
        job = JOBS[job_id]
        job.update(changes)
        job["updated_at"] = time()
        job["elapsed_seconds"] = max(int(job["updated_at"] - job["started_at"]), 0)

        if job.get("stage") in STAGE_INDEX:
            completed_stages = STAGE_INDEX[job["stage"]]
            remaining_stages = max(len(STAGE_ORDER) - completed_stages - 1, 0)
            job["estimated_remaining_seconds"] = remaining_stages * STAGE_ESTIMATE_SECONDS
        else:
            job["estimated_remaining_seconds"] = STAGE_ESTIMATE_SECONDS * len(STAGE_ORDER)


def _build_background(payload: GenerateReportRequest) -> str:
    background_parts = []

    if payload.python_skill_level:
        background_parts.append(f"Python skill level: {payload.python_skill_level}")

    if payload.ml_experience:
        background_parts.append(f"ML experience: {payload.ml_experience}")

    if payload.additional_background:
        background_parts.append(payload.additional_background)

    return "; ".join(background_parts)


def _run_job(job_id: str, payload: GenerateReportRequest):
    background = _build_background(payload)
    _update_job(job_id, status="running", background=background, stage="research", stage_state="running", message="Searching ArXiv and Semantic Scholar...")

    def progress_callback(stage: str, state: str, message: str):
        _update_job(job_id, stage=stage, stage_state=state, message=message)

    try:
        report = run_omnithesis_crew(topic=payload.topic, background=background, progress_callback=progress_callback)
        _update_job(job_id, status="completed", stage="editing", stage_state="completed", message="Report generation complete.", report=str(report), error=None)
    except Exception as exc:
        _update_job(job_id, status="failed", error=str(exc), message="The pipeline did not complete.")

# MISTAKE #2 - MUST HAVE /health endpoint for Render free tier / UptimeRobot
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def read_root():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)

    return {"message": "Hello World! OmniThesis AI API is running."}


@app.post("/generate-report", status_code=202)
async def generate_report(payload: GenerateReportRequest):
    job_id = _create_job(payload)
    worker = Thread(target=_run_job, args=(job_id, payload), daemon=True)
    worker.start()

    return {
        "job_id": job_id,
        "status_url": f"/report-status/{job_id}",
        "message": "Report generation started.",
    }


@app.get("/report-status/{job_id}")
def report_status(job_id: str):
    with JOBS_LOCK:
        job = JOBS.get(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job["job_id"],
        "status": job["status"],
        "stage": job["stage"],
        "stage_state": job["stage_state"],
        "message": job["message"],
        "topic": job["topic"],
        "background": job["background"],
        "report": job["report"],
        "error": job["error"],
        "elapsed_seconds": job["elapsed_seconds"],
        "estimated_remaining_seconds": job["estimated_remaining_seconds"],
        "started_at": job["started_at"],
        "updated_at": job["updated_at"],
    }
