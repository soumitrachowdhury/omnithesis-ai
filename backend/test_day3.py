from dotenv import load_dotenv

load_dotenv()

import time
from unittest.mock import patch

from crew import run_omnithesis_crew
from fastapi.testclient import TestClient
from main import app


def test_full_crew():
    print("Testing Full OmniThesis Crew...")
    start_time = time.perf_counter()

    result = run_omnithesis_crew(
        topic="motion generation for human animation",
        background="computer vision background, intermediate Python skills, limited probabilistic modeling experience",
    )

    print("\n\n=== FINAL RESULT ===")
    print(result)
    elapsed_seconds = time.perf_counter() - start_time
    print(f"\n\n=== TOTAL EXECUTION TIME: {elapsed_seconds:.2f} seconds ===")


def test_generate_report_endpoint_smoke():
    print("Testing /generate-report endpoint smoke test...")
    client = TestClient(app)

    def fake_runner(topic, background="", progress_callback=None):
        if progress_callback:
            progress_callback("research", "running", "Searching ArXiv...")
            progress_callback("research", "completed", "Found candidate papers.")
            progress_callback("domain", "running", "Summarizing the field and key ideas...")
            progress_callback("domain", "completed", "Domain overview ready.")
            progress_callback("curation", "running", "Ranking papers by relevance...")
            progress_callback("curation", "completed", "Paper list curated.")
            progress_callback("feasibility", "running", "Assessing difficulty for the background provided...")
            progress_callback("feasibility", "completed", "Feasibility assessment complete.")
            progress_callback("writing", "running", "Drafting the full report in markdown...")
            progress_callback("writing", "completed", "Draft report assembled.")
            progress_callback("editing", "running", "Polishing structure, clarity, and flow...")
            progress_callback("editing", "completed", "Final report polished.")
        return "# Mock Report\n\nGenerated for smoke test."

    with patch("main.run_omnithesis_crew", side_effect=fake_runner) as mocked_runner:
        response = client.post(
            "/generate-report",
            json={
                "topic": "motion generation for human animation",
                "python_skill_level": "intermediate",
                "ml_experience": "some experience",
                "additional_background": "computer vision background",
            },
        )

        print("POST status code:", response.status_code)
        payload = response.json()
        print("POST response JSON:", payload)

        job_id = payload["job_id"]
        deadline = time.time() + 5
        status_payload = None

        while time.time() < deadline:
            status_response = client.get(f"/report-status/{job_id}")
            status_payload = status_response.json()
            print("Status poll:", status_payload)
            if status_payload.get("status") == "completed":
                break
            time.sleep(0.1)

    print("Mock called:", mocked_runner.called)
    print("Final status:", status_payload)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "api":
        test_generate_report_endpoint_smoke()
    else:
        test_full_crew()