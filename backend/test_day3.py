from dotenv import load_dotenv

load_dotenv()

import time

from crew import run_omnithesis_crew


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


if __name__ == "__main__":
    test_full_crew()