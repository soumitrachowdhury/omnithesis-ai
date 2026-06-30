from crewai import Agent

from llm import get_groq_llm


def create_paper_curator():
    """
    Creates the Paper Curator Agent.
    Its job is to filter, rank, and validate the strongest papers for the report.
    """
    llm = get_groq_llm()

    return Agent(
        role='Paper Curator',
        goal='Select the most relevant, credible, and high-quality papers for the research report.',
        backstory=(
            "You are a meticulous academic curator who reviews paper relevance, quality, and fit. "
            "You prioritize real papers, strong methodology, and clear connection to the topic, "
            "and you only surface papers that are useful for a rigorous research report."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )