<div align="center">

# OmniThesis AI

### Multi-Agent Academic Research Assistant

**Six AI agents. One research topic. A complete structured report — in under 2 minutes.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-omnithesis--ai.onrender.com-4f86f7?style=for-the-badge&logo=render)](https://omnithesis-ai.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-FF6B6B?style=for-the-badge)](https://crewai.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey?style=for-the-badge)](LICENSE)

---

<img width="1366" height="1812" alt="OmniThesis AI UI" src="https://github.com/user-attachments/assets/39f7fd07-f6f4-4692-957a-8eeebee87c20" />

---

[🚀 Try the Live Demo](https://omnithesis-ai.onrender.com) · [📖 How It Works](#how-it-works) · [⚙️ Local Setup](#local-setup) · [🏗️ Architecture](#architecture)

</div>

---

## What Is OmniThesis AI?

OmniThesis AI is a **multi-agent AI research assistant** designed to help students and early-stage researchers navigate unfamiliar research topics, explore relevant literature, assess feasibility, and identify practical directions for further investigation. You give it a research topic and a bit of background about yourself — it dispatches six specialized AI agents that search real academic databases, curate the best papers, assess how approachable the topic is for your skill level, and write a full structured research report.

**The problem it solves:** Starting a literature review is one of the hardest parts of academic research. Most students spend days searching databases, reading abstracts, and trying to understand a new field before they can even frame a proper research question. OmniThesis AI compresses that process to under two minutes.

> **No hallucination policy:** Papers are sourced exclusively from ArXiv and Semantic Scholar APIs. The LLM never invents titles, authors, or venues — it only analyzes papers the search tools actually return.

---

## Live Demo

**🌐 [https://omnithesis-ai.onrender.com](https://omnithesis-ai.onrender.com)**

> The app is hosted on Render's free tier. If it takes 10–15 seconds to respond on first load, the server is waking up from sleep — this is normal. Once awake, report generation takes approximately 90–120 seconds.

---

## Features

- **Real paper discovery** — searches ArXiv and Semantic Scholar, not the LLM's memory
- **Domain explanation** — explains what the field is, who works on it, and what the open problems are
- **Intelligent curation** — ranks papers by relevance, credibility, and fit for the topic
- **Personalised feasibility rating** — rates the topic Easy / Medium / Hard for your specific background and identifies your skill gaps
- **Full structured report** — 8-section markdown report including Executive Summary, Research Trends, Top Papers, Learning Path, and Suggested Research Directions
- **Live progress tracker** — watch each of the six agents work in real time
- **PDF export** — download the finished report as a PDF directly from the browser, no extra software needed

---

## Report Sections

Every generated report contains the following sections:

1. Executive Summary
2. Domain Overview
3. Current Research Trends
4. Top Research Papers *(with citations and links)*
5. Feasibility Assessment *(personalised to your background)*
6. Key Challenges
7. Recommended Learning Path
8. Suggested Research Directions

---

## How It Works

OmniThesis AI runs six AI agents sequentially. Each agent has a single specialised role and passes its output to the next:

```
Your Input (topic + background)
        │
        ▼
┌─────────────────────┐
│  1. Research Scout  │  Searches ArXiv + Semantic Scholar
│                     │  → Returns a list of real papers with links
└─────────┬───────────┘
          │ 15s pause (rate limit)
          ▼
┌─────────────────────┐
│  2. Domain Analyst  │  Reads the papers, maps the field
│                     │  → Returns field overview, concepts, trends
└─────────┬───────────┘
          │ 15s pause (rate limit)
          ▼
┌─────────────────────┐
│  3. Paper Curator   │  Ranks and filters papers by quality
│                     │  → Returns top 8–12 papers with justification
└─────────┬───────────┘
          │ 15s pause (rate limit)
          ▼
┌────────────────────────┐
│  4. Feasibility Analyst│  Scores topic difficulty for your background
│                        │  → Returns rating + skill gaps + advice
└─────────┬──────────────┘
          │ 15s pause (rate limit)
          ▼
┌─────────────────────┐
│  5. Report Writer   │  Synthesises all outputs into a report draft
│                     │  → Returns full 8-section markdown report
└─────────┬───────────┘
          │ 15s pause (rate limit)
          ▼
┌─────────────────────┐
│  6. Editor          │  Polishes clarity, flow, and presentation
│                     │  → Returns final, publication-ready report
└─────────┬───────────┘
          │
          ▼
   Rendered in browser → Download as PDF
```

The 15-second pauses between agents are intentional — they prevent hitting the LLM provider's free-tier rate limits without reducing the quality of the agents' outputs. Every agent call is also wrapped in automatic retry-with-backoff, so a transient rate-limit or server error (HTTP 429/500/502/503/504) is retried instead of failing the whole run.

---

## Demo Walkthrough

<img width="827" height="592" alt="Report Form" src="https://github.com/user-attachments/assets/c55c1eb7-07b3-41d8-bdd5-737257bb9027" />

**Step 1 — Enter your topic and background**

Open [https://omnithesis-ai.onrender.com](https://omnithesis-ai.onrender.com), type your research topic (e.g. *"skeleton-based human action prediction for human-robot collaboration"*), select your Python skill level and ML experience, then click **Generate Report**.

---

<img width="711" height="493" alt="Progress Tracker" src="https://github.com/user-attachments/assets/f8f8b3b8-1522-4e32-9995-574e650b4bfc" />

**Step 2 — Watch the agents work**

The progress tracker shows each of the six agents activating in sequence. The tracker updates live every few seconds. Total time is approximately 90–120 seconds.

---

<img width="679" height="595" alt="Generated Report" src="https://github.com/user-attachments/assets/d530e02d-a250-421a-9fee-572d94b089c6" />

**Step 3 — Read and download your report**

The finished report is rendered as formatted HTML in the browser. Click **Download as PDF** to print it — the print stylesheet removes all navigation elements and produces a clean, readable PDF.

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| AI Agents | [CrewAI](https://crewai.com/) | Orchestrates the 6-agent sequential pipeline |
| LLM | [Google Gemini API](https://aistudio.google.com/) — Gemini 3.1 Flash-Lite | Powers all agent reasoning and writing |
| Paper Search | [ArXiv API](https://arxiv.org/help/api/) | Discovers real academic papers |
| Paper Search | [Semantic Scholar API](https://www.semanticscholar.org/product/api) | Discovers real academic papers |
| Backend | [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11) | REST API, async background pipeline, status polling |
| Frontend | Vanilla HTML + CSS + JS | Single self-contained file, no framework needed |
| Report Rendering | [Marked.js](https://marked.js.org/) | Converts agent markdown output to formatted HTML |
| PDF Export | Browser `window.print()` | Zero-dependency, Docker-safe PDF generation |
| Containerisation | [Docker](https://www.docker.com/) | Reproducible builds, consistent deploys |
| Hosting | [Render](https://render.com/) | Free-tier cloud hosting (Singapore region) |
| Uptime Monitoring | [UptimeRobot](https://uptimerobot.com/) | Pings `/health` every 5 minutes to prevent Render sleep |

---

## Architecture

### Request Flow

When you click **Generate Report**, here is exactly what happens:

```
Browser                    FastAPI Backend              Background Thread
   │                            │                              │
   │  POST /generate-report     │                              │
   │ ─────────────────────────► │                              │
   │                            │  Creates a report task       │
   │                            │  with a unique ID            │
   │                            │ ────────────────────────────►│
   │  { task_id, status_url }   │                              │  6 agents run
   │ ◄───────────────────────── │                              │  sequentially
   │                            │                              │  (~90-120 sec)
   │  GET /report-status/{id}   │                              │
   │ ─────────────────────────► │                              │
   │  { stage, state, elapsed } │                              │
   │ ◄───────────────────────── │                              │
   │       (polls every 2s)     │                              │
   │                            │  ◄───────────────────────────│
   │                            │  Stage updates written       │
   │  GET /report-status/{id}   │  to in-memory store          │
   │ ─────────────────────────► │                              │
   │  { status: "completed",    │                              │
   │    report: "# Report..." } │                              │
   │ ◄───────────────────────── │                              │
   │                            │                              │
   │  Renders report via        │                              │
   │  Marked.js                 │                              │
```

**Why background tasks?** The 6-agent pipeline takes approximately 90–120 seconds. A standard HTTP request would time out in the browser long before it finished. The background task system returns a task ID immediately (HTTP 202), runs the pipeline on a separate thread, and lets the frontend poll for updates.

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the frontend (index.html) |
| `GET` | `/health` | Returns `{"status": "ok"}` — used by UptimeRobot |
| `POST` | `/generate-report` | Starts the 6-agent pipeline, returns a task ID immediately |
| `GET` | `/report-status/{task_id}` | Returns current stage, progress, and the finished report |

### Project Structure

```
omnithesis-ai/
├── backend/
│   ├── agents/
│   │   ├── domain_analyst.py
│   │   ├── editor.py
│   │   ├── feasibility_analyst.py
│   │   ├── paper_curator.py
│   │   ├── report_writer.py
│   │   └── research_scout.py
│   ├── tools/
│   │   ├── arxiv_tool.py
│   │   └── semantic_scholar_tool.py
│   ├── crew.py
│   ├── llm.py
│   └── main.py
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── style.css
├── .dockerignore
├── Dockerfile
├── LICENSE
├── README.md
└── requirements.txt
```

---

## Local Setup

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- A free [Google Gemini API key](https://aistudio.google.com/) *(takes 2 minutes to create)*
- A [Semantic Scholar API key](https://www.semanticscholar.org/product/api) *(optional — the app works without one)*

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/soumitrachowdhury/omnithesis-ai.git
cd omnithesis-ai

# 2. Set up your environment variables
cp .env.example .env
# Open .env in any text editor and paste your GEMINI_API_KEY
```

Your `.env` file should look like this:

```env
GEMINI_API_KEY=your_gemini_key_here
SEMANTIC_SCHOLAR_API_KEY=your_key_here   # optional
```

```bash
# 3. Build the Docker image
docker build -t omnithesis-ai .

# 4. Run the container
docker run -p 8000:8000 --env-file .env omnithesis-ai
```

```
# 5. Open in your browser
http://localhost:8000
```

> ⚠️ **Important:** Always run the container with `docker run --env-file .env`. Do not use the Docker Desktop "Run" button — it does not inject environment variables from your `.env` file, so the app will start but immediately fail when it tries to call the Gemini API.

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | **Yes** | Your Google Gemini API key for Gemini 3.1 Flash-Lite |
| `SEMANTIC_SCHOLAR_API_KEY` | No | Optional. Enables higher rate limits on Semantic Scholar searches |

---

## AI Model Details

| Property | Value |
|---|---|
| Model | Gemini 3.1 Flash-Lite |
| Provider | Google (Gemini API) |
| Temperature | 0.1 (low — keeps outputs factual and consistent) |
| Framework | CrewAI with a custom litellm compatibility patch |
| Agent strategy | Sequential — each agent receives the full output of all previous agents |

**Why Gemini?** The project originally ran on Groq's `llama-3.3-70b-versatile`, but Groq deprecated that model in August 2026. The pipeline was migrated to Google's Gemini API, which offers a free tier with a noticeably higher rate-limit ceiling than Groq's. That headroom is used alongside — not instead of — the existing safeguards: a `max_rpm` cap on the CrewAI crew, the 15-second pauses between agent calls, and automatic retry-with-backoff on rate-limit/server errors.

**Why Gemini 3.1 Flash-Lite?** It's a fast, low-cost model in Gemini's Flash-Lite tier with solid instruction-following for long-form structured writing, and it's available on Gemini's free tier — a good fit for report generation without added cost.

---

## Planned Improvements

These features were intentionally left out of the initial version to meet the project deadline. They represent the natural next steps for making OmniThesis AI more production-ready:

| Feature | Description |
|---|---|
| Improved UI/UX | The current interface is functional but minimal. A redesigned UI with better typography, paper cards, and a cleaner report viewer would significantly improve the user experience |
| Bring your own API key | Allow users to paste their own Gemini key in the UI so the app is not tied to a single shared quota |
| Persistent report history | Currently, reports disappear when the server restarts because they are stored in memory. A database (SQLite or PostgreSQL) would give users a history of past reports |
| User accounts | Let users save, name, and revisit their generated reports |
| Real-time streaming progress | Replace the current polling approach with WebSockets or Server-Sent Events for smoother live updates |
| Report cancellation | Allow users to stop a generation mid-way instead of waiting for it to finish or time out |
| More paper sources | Add Google Scholar, PubMed, or IEEE Xplore as additional search sources |
| Citation export | Let users download the paper list as a BibTeX or RIS file for use in reference managers |

---

## License

This project is licensed under [CC BY-NC-ND 4.0](LICENSE).

You are free to share and reference this work for non-commercial purposes with attribution. You may not modify it or use it commercially.

---

## Author

**Soumitra Chowdhury**

---

<div align="center">

Built with CrewAI · Gemini · FastAPI · Docker · Render

</div>
