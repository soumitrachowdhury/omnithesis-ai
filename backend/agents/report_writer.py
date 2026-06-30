from crewai import Agent

from llm import get_groq_llm


def create_report_writer():
    """
    Creates the Report Writer Agent.
    Its job is to compile the research findings into a structured markdown report.
    """
    llm = get_groq_llm()

    return Agent(
        role='Report Writer',
        goal='Write a clear, well-structured markdown report from the gathered research insights.',
        backstory=(
            "You are a skilled technical writer who turns research findings into polished, "
            "structured reports. You organize content clearly, keep the writing concise and "
            "academic, and ensure the final output is ready for presentation."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )