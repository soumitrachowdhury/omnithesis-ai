from crewai import Agent

from llm import get_groq_llm


def create_editor():
    """
    Creates the Editor Agent.
    Its job is to review the draft report and improve clarity, consistency, and polish.
    """
    llm = get_groq_llm()

    return Agent(
        role='Editor',
        goal='Review the draft report and improve clarity, structure, accuracy, and presentation quality.',
        backstory=(
            "You are a meticulous academic editor who strengthens reports by improving clarity, "
            "organization, and readability. You focus on consistency, concise wording, and making "
            "the final report feel polished and professional."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )