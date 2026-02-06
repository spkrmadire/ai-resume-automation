import os
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from services.render_service import render_docx


load_dotenv()

app = FastAPI(title="AI Resume Tailor (Local)")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("MODEL_NAME", "gpt-5-mini")
BASE_RESUME_PATH = os.getenv("BASE_RESUME_PATH", "../data/base_resume.txt")
RESUME_NAME = os.getenv("RESUME_NAME", "Your Name")
RESUME_TITLE = os.getenv("RESUME_TITLE", "")
RESUME_CONTACT = os.getenv("RESUME_CONTACT", "")


OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs"))
os.makedirs(OUTPUT_DIR, exist_ok=True)


class TailorRequest(BaseModel):
    company: str
    role: str
    job_description: str


class TailorResponse(BaseModel):
    output_txt: str
    saved_txt_to: str
    saved_docx_to: str



def load_base_resume_text() -> str:
    if not os.path.exists(BASE_RESUME_PATH):
        raise FileNotFoundError(
            f"Base resume not found at {BASE_RESUME_PATH}. "
            f"Create it at ./data/base_resume.txt and try again."
        )
    with open(BASE_RESUME_PATH, "r", encoding="utf-8") as f:
        return f.read().strip()


@app.post("/tailor", response_model=TailorResponse)
def tailor(req: TailorRequest):
    base_resume_text = load_base_resume_text()

    system = (
        "You are an expert ATS resume writer.\n"
        "Rules:\n"
        "1) Do NOT invent experience, employers, titles, dates, tools, certifications, or projects.\n"
        "2) Only rewrite/reorder content that is already present in the base resume.\n"
        "3) Align wording to the job description using equivalent truthful phrasing.\n"
        "4) Keep it concise and ATS-friendly.\n"
        "Output plain text with these sections: Summary, Skills, Experience, Education.\n"
    )

    user = f"""
JOB DESCRIPTION:
{req.job_description}

BASE RESUME (source of truth):
{base_resume_text}

TASK:
- Produce a tailored 1-page ATS-friendly resume in plain text.
- Summary: 3 lines max, tailored to the JD.
- Skills: grouped, include only skills present in base resume.
- Experience: strongest 3–6 bullets per role, rewritten to match JD language truthfully.
- Education: as-is.
"""

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )

    tailored_text = resp.choices[0].message.content.strip()


    safe_company = req.company.replace(" ", "_").replace("/", "_")
    safe_role = req.role.replace(" ", "_").replace("/", "_")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_company}_{safe_role}_{ts}.txt"
    out_path = os.path.join(OUTPUT_DIR, filename)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(tailored_text)
    docx_path = os.path.join(OUTPUT_DIR, f"{safe_company}_{safe_role}_{ts}.docx")

    # TODO: later we can read these from config or from your base resume header
    render_docx(
    out_path=docx_path,
    name=RESUME_NAME,
    title_line=RESUME_TITLE,
    contact_line=RESUME_CONTACT,
    tailored_text=tailored_text,
)

       

    return TailorResponse(
    output_txt=tailored_text,
    saved_txt_to=out_path,
    saved_docx_to=docx_path,
)

