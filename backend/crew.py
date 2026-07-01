import time
from typing import Callable, Optional

from crewai import Crew, Process, Task

from agents.domain_analyst import create_domain_analyst
from agents.editor import create_editor
from agents.feasibility_analyst import create_feasibility_analyst
from agents.paper_curator import create_paper_curator
from agents.report_writer import create_report_writer
from agents.research_scout import create_research_scout


def _run_single_step(agent, description: str, expected_output: str):
    task = Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    return crew.kickoff()


def _emit_progress(
    progress_callback: Optional[Callable[[str, str, str], None]],
    stage: str,
    state: str,
    message: str,
):
    if progress_callback:
        progress_callback(stage, state, message)


def run_omnithesis_crew(
    topic: str,
    background: str = "",
    progress_callback: Optional[Callable[[str, str, str], None]] = None,
):
    research_scout = create_research_scout()
    domain_analyst = create_domain_analyst()
    paper_curator = create_paper_curator()
    feasibility_analyst = create_feasibility_analyst()
    report_writer = create_report_writer()
    editor = create_editor()

    _emit_progress(progress_callback, "research", "running", "Searching ArXiv and Semantic Scholar...")
    research_description = (
        f"Search real academic papers for the topic '{topic}'. Use ArXiv and Semantic Scholar as the only sources. "
        "Return a grounded list of papers with titles, authors, years, and links. Do not invent titles, authors, or venues. "
        "Prefer papers that are directly relevant, recent enough to reflect the state of the field, and useful for a capstone research report."
    )
    research_expected = (
        "A markdown list of at least several real candidate papers with concise citations and links."
    )
    research_output = _run_single_step(research_scout, research_description, research_expected)

    time.sleep(15)

    _emit_progress(progress_callback, "research", "completed", "Found candidate papers.")
    _emit_progress(progress_callback, "domain", "running", "Summarizing the field and key ideas...")
    domain_description = (
        f"Analyze the research domain for '{topic}'. Explain what the field is, why it matters, who works on it, "
        "the core concepts a newcomer must understand, and the current research directions that are actively being explored. "
        "Ground the explanation in the research results collected so far and keep the wording suitable for a student-facing report.\n\n"
        f"Research findings to build on:\n{research_output}"
    )
    domain_expected = (
        "A markdown domain overview with the field summary, core concepts, trends, and open challenges."
    )
    domain_output = _run_single_step(domain_analyst, domain_description, domain_expected)

    time.sleep(15)

    _emit_progress(progress_callback, "domain", "completed", "Domain overview ready.")
    _emit_progress(progress_callback, "curation", "running", "Ranking papers by relevance...")
    curation_description = (
        f"Curate the best papers for a report on '{topic}'. Review the research findings and select the most relevant, credible, "
        "and high-quality papers. Rank the papers, explain why each one belongs, and prefer papers that help build a solid academic narrative. "
        "Reject weak or tangential papers. The output should support a rigorous report, not a generic summary.\n\n"
        f"Research findings:\n{research_output}\n\nDomain analysis:\n{domain_output}"
    )
    curation_expected = (
        "A markdown list of curated papers with short justification for each selection."
    )
    curation_output = _run_single_step(paper_curator, curation_description, curation_expected)

    time.sleep(15)

    _emit_progress(progress_callback, "curation", "completed", "Paper list curated.")
    _emit_progress(progress_callback, "feasibility", "running", "Assessing difficulty for the background provided...")
    feasibility_description = (
        f"Assess the feasibility of the research topic '{topic}' for a student with the following background: {background or 'not provided'}. "
        "Rate the topic as Easy, Medium, or Hard for this student and explain the skill gaps, what makes the topic demanding, "
        "and what practical steps would help the student get started. Keep the guidance realistic and specific to the topic.\n\n"
        f"Domain analysis:\n{domain_output}\n\nCurated papers:\n{curation_output}"
    )
    feasibility_expected = (
        "A markdown feasibility assessment with difficulty rating, skill gaps, and practical next steps."
    )
    feasibility_output = _run_single_step(
        feasibility_analyst,
        feasibility_description,
        feasibility_expected,
    )

    time.sleep(15)

    _emit_progress(progress_callback, "feasibility", "completed", "Feasibility assessment complete.")
    _emit_progress(progress_callback, "writing", "running", "Drafting the full report in markdown...")
    writing_description = (
        f"Write a full structured markdown research report for '{topic}'. The report must synthesize the research findings, "
        "domain analysis, curated papers, and feasibility assessment into a coherent, student-friendly academic report. "
        "Include the following sections: Executive Summary, Domain Overview, Current Research Trends, Top Research Papers, "
        "Feasibility Assessment, Key Challenges, Recommended Learning Path, and Suggested Research Directions. "
        "Use clear headings, polished academic language, and readable markdown formatting.\n\n"
        f"Research findings:\n{research_output}\n\nDomain analysis:\n{domain_output}\n\nCurated papers:\n{curation_output}\n\nFeasibility assessment:\n{feasibility_output}"
    )
    writing_expected = (
        "A structured markdown report ready for review and presentation."
    )
    writing_output = _run_single_step(report_writer, writing_description, writing_expected)

    time.sleep(15)

    _emit_progress(progress_callback, "writing", "completed", "Draft report assembled.")
    _emit_progress(progress_callback, "editing", "running", "Polishing structure, clarity, and flow...")
    editing_description = (
        f"Edit the draft markdown report for '{topic}'. Improve clarity, structure, consistency, transitions, and presentation quality "
        "while preserving the meaning and factual content. Fix awkward phrasing, tighten repetitive passages, and make sure the final report reads like a polished capstone deliverable.\n\n"
        f"Draft report:\n{writing_output}"
    )
    editing_expected = (
        "A polished markdown report with improved clarity and presentation quality."
    )
    final_output = _run_single_step(editor, editing_description, editing_expected)

    _emit_progress(progress_callback, "editing", "completed", "Final report polished.")

    return final_output