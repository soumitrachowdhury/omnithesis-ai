from dotenv import load_dotenv
load_dotenv()

from crewai import Task, Crew, Process
from agents.research_scout import create_research_scout

def test_research_scout():
    print("Testing Research Scout Agent...")
    
    # 1. Create Agent
    scout_agent = create_research_scout()
    
    # 2. Define Task
    search_task = Task(
        description="Search for the most recent and highly relevant papers on 'motion prediction for autonomous driving'. "
                    "Use both ArXiv and Semantic Scholar tools. Compile a concise list of at least 3 real papers with their titles, authors, and links.",
        expected_output="A markdown formatted list of at least 3 real papers with their titles, authors, summary, and links.",
        agent=scout_agent
    )
    
    # 3. Create Crew and run
    crew = Crew(
        agents=[scout_agent],
        tasks=[search_task],
        process=Process.sequential,
        verbose=True
    )
    
    result = crew.kickoff()
    
    print("\n\n=== FINAL RESULT ===")
    print(result)

if __name__ == "__main__":
    test_research_scout()
