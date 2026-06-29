from crewai import Agent
from tools.arxiv_tool import search_arxiv
from tools.semantic_scholar_tool import search_semantic_scholar
from llm import get_groq_llm

def create_research_scout():
    """
    Creates the Research Scout Agent for Day 2.
    Its job is to search ArXiv and Semantic Scholar for real academic papers.
    """
    llm = get_groq_llm()
    
    return Agent(
        role='Research Scout',
        goal='Find the most relevant and high-quality academic papers for the given research topic.',
        backstory=(
            "You are an expert academic researcher. Your job is to search through scholarly databases "
            "like ArXiv and Semantic Scholar to find real, authoritative papers on a specific topic. "
            "You never invent or hallucinate paper titles, authors, or links. You only provide information "
            "that is returned by your search tools."
        ),
        verbose=True,
        allow_delegation=False,
        tools=[search_arxiv, search_semantic_scholar],
        llm=llm
    )
