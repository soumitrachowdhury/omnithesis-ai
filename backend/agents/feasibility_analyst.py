from crewai import Agent

from llm import get_groq_llm


def create_feasibility_analyst():
    """
    Creates the Feasibility Analyst Agent.
    Its job is to assess how difficult the topic is for the user's background.
    """
    llm = get_groq_llm()

    return Agent(
        role='Feasibility Analyst',
        goal='Evaluate the research topic difficulty against the user background and give practical guidance.',
        backstory=(
            "You are an experienced academic mentor who can judge whether a research topic is "
            "easy, medium, or hard for a student based on their background. You identify skill "
            "gaps, explain the challenge level clearly, and give practical advice for getting started."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )