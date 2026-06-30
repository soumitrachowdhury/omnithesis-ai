from crewai import Agent

from llm import get_groq_llm


def create_domain_analyst():
    """
    Creates the Domain Analyst Agent.
    Its job is to explain the research field, core concepts, and current directions.
    """
    llm = get_groq_llm()

    return Agent(
        role='Domain Analyst',
        goal='Analyze the research domain and explain its core concepts, trends, and context clearly.',
        backstory=(
            "You are an expert research analyst who understands how to summarize complex academic "
            "fields into clear, structured insights. You focus on what the field is about, why it "
            "matters, and what directions researchers are actively pursuing."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )