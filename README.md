# AI Resume Intelligence Tool  
**JD → Tailored Resume in <45 Seconds**

A self-serving AI tool that reads a job description, compares it with a **master resume**, and generates a **clean, relevant, ATS-aligned tailored resume** in seconds.

Built to remove the repetitive manual resume-editing loop during job applications.

> **Impact:** What previously took **15–20 minutes** of manual tailoring now takes **one click** and typically **<45 seconds** to generate a downloadable tailored resume.

---

## Overview

Job applications often require repeatedly editing resumes to match each job description.  
This project solves that problem by creating an **AI-driven resume intelligence pipeline** that:

- Understands job descriptions semantically  
- Prioritizes relevant skills and experience  
- Rewrites resume content contextually  
- Produces an ATS-friendly tailored resume instantly  

The goal was to build something **practical and usable in a real daily workflow**, not just a demo.

---

## Key Features

- One-click **Job Description capture via Chrome Extension**
- **Master Resume strategy** (single reusable source of truth)
- AI-powered **semantic comparison & contextual rewriting**
- **ATS-aligned formatting and keyword relevance**
- Fast generation (**usually <45 seconds**)
- Modular pipeline:  
  **Parse → Compare → Rewrite → Export**

---

## High-Level Architecture

**Inputs**
- Master Resume (PDF / DOCX / TXT)
- Job Description (captured from browser or pasted)

**Processing Pipeline**
1. Resume parsing & normalization  
2. Job description extraction  
3. Semantic comparison using LLM  
4. Relevance prioritization & contextual rewrite  
5. Tailored resume export  

**Output**
- Job-specific tailored resume (PDF/DOCX)

---

## Tech Stack

- **Python** — backend orchestration  
- **OpenAI API** — semantic reasoning & text generation  
- **Chrome Extension** — one-click JD capture and trigger  
- Document utilities for **PDF/DOCX parsing and export**

---

## Getting Started

### Prerequisites

- Python **3.10+**
- Node.js **18+** (for Chrome extension, if applicable)
- OpenAI API key

---

### Installation

bash
git clone <your-repo-url>
cd <repo-folder>

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -r requirements.txt

Environment Configuration

Create a .env file in the project root:

OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4.1-mini
BASE_RESUME_PATH=./data/resume/master_resume.pdf
OUTPUT_DIR=./outputs

Run the Application

If using an API server (example FastAPI):

uvicorn app.main:app --reload --port 8000


Or script-based execution:

python main.py

Chrome Extension Setup
Load Unpacked Extension

Open Chrome → chrome://extensions

Enable Developer mode

Click Load unpacked

Select the project’s extension/ folder

Usage Flow
One-Click Tailoring (Extension)

Open any job posting page

Click the extension → Tailor Resume

Job description is captured automatically

Tailored resume is generated and saved to OUTPUT_DIR / Downloads

Manual Tailoring (No Extension)
python main.py --jd ./data/jd.txt


Output will appear in:

./outputs
























