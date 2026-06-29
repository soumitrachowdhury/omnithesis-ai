from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="OmniThesis AI Backend")

# MISTAKE #2 - MUST HAVE /health endpoint for Render free tier / UptimeRobot
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "Hello World! OmniThesis AI API is running."}
