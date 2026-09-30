"""
Ambient Indian AI Medical Scribe - POC backend.

Run (e.g. inside Termux):
    pip install fastapi uvicorn python-multipart openai
    export GROQ_API_KEY="gsk_..."
    uvicorn app:app --host 127.0.0.1 --port 8000
"""

import json
import os
import shutil
import tempfile

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

WHISPER_MODEL = "whisper-large-v3"
LLM_MODEL = os.environ.get("SCRIBE_LLM_MODEL", "llama-3.1-70b-versatile")

WHISPER_PROMPT = (
    "Indian doctor OPD conversation, Hinglish, Pet me dard, Sugar, BP, "
    "Crocin, Pantocid, reports, chhaati me jalan."
)

MASTER_SYSTEM_PROMPT = '''You are an advanced, specialized AI Medical Scribe embedded inside a local EMR system for an Indian hospital Outpatient Department (OPD). Your core job is to process messy, unstructured, and highly phonetic transcripts of Indian doctor-patient encounters and convert them into a structured, clinical document.

The input transcript you receive will be highly colloquial, phonetically spelled, and heavily "code-mixed" (Hinglish/Regional Indian languages blended with English).

Execute your task following these strict steps:

1. LANGUAGE TRANSLATION & CLINICAL MAPPING:
- Actively translate all regional or Hindi symptom descriptions into formal medical English.
  * Example: "Pet me dard" -> Abdominal pain.
  * Example: "Chhaati me jalan" -> Heartburn / Dyspepsia.
  * Example: "Sir ghoom raha hai" -> Dizziness / Vertigo.
  * Example: "Bohat thand lag ke bukhar aya" -> High-grade fever with chills.
- Recognize common Indian abbreviations used in speech: "BP" (Blood Pressure), "Sugar" (Diabetes Mellitus), "Report dekh lo" (Review investigations).

2. PHARMACY AND BRAND MAPPING:
- Accurately capture Indian pharmaceutical brand names or generic shorthands spoken during the consultation.
- Translate spoken frequencies into structured instructions:
  * "Subah shaam" or "Do baar" -> Twice daily (BD).
  * "Khane se pehle" -> Before food (AC).
  * "Khane ke baad" -> After food (PC).
  * "Ek goli" -> 1 tablet.
- Map common brands correctly (e.g., Crocin/Calpol -> Paracetamol, Pantocid/Pan -> Pantoprazole, Augmentin -> Amoxicillin-Clavulanate).

3. OUTPUT FORMAT (MANDATORY STRUCTURE):
Your final response must strictly be valid JSON with no conversational preamble, no markdown code block wrappers (do not use ```json), and no closing remarks. Output ONLY the raw JSON object matching this schema:

{
  "clinical_summary": {
    "subjective": {
      "chief_complaint": "String describing main symptoms with duration",
      "history_of_present_illness": "Brief prose summary of the patient's history as discussed"
    },
    "objective": {
      "vitals_mentioned": "String listing any BP, PR, SpO2, or weight mentioned, or 'Not assessed'",
      "physical_examination": "Any physical signs discussed or 'Not performed'"
    },
    "assessment": {
      "differential_diagnosis": ["Array of likely diagnoses mapped to general ICD-10 principles"]
    },
    "plan": {
      "medications": [
        {
          "brand_or_generic_name": "Name of drug",
          "dosage_form": "Tablet / Capsule / Syrup / Injection",
          "strength": "e.g., 40mg, 500mg, or 'As specified'",
          "frequency": "e.g., Once daily before breakfast / BD / TDS",
          "duration": "e.g., 5 days, 1 week"
        }
      ],
      "investigations_ordered": ["Array of labs, X-rays, or Ultrasounds requested"],
      "advice_and_lifestyle": ["Array of dietary restrictions or lifestyle advice given"],
      "follow_up": "Timeline or criteria for next visit"
    }
  }
}

CRITICAL CONSTRAINT:
Do not hallucinate facts. If the doctor or patient did not explicitly mention vitals, examinations, or specific durations, leave those fields blank or state "Not mentioned". Rely strictly on the context provided in the transcript.
'''

_client = None


def get_client() -> OpenAI:
    """Groq-backed OpenAI client, created on first use so the server can boot without a key."""
    global _client
    if _client is None:
        _client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.environ.get("GROQ_API_KEY"),
        )
    return _client

app = FastAPI(title="Ambient Indian AI Medical Scribe POC")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def transcribe_audio(path: str) -> str:
    with open(path, "rb") as audio:
        result = get_client().audio.transcriptions.create(
            model=WHISPER_MODEL,
            file=audio,
            prompt=WHISPER_PROMPT,
            response_format="json",
        )
    return result.text.strip()


def structure_transcript(transcript: str) -> dict:
    completion = get_client().chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": MASTER_SYSTEM_PROMPT},
            {"role": "user", "content": f"Transcript:\n{transcript}"},
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )
    content = completion.choices[0].message.content or "{}"
    return json.loads(content)


@app.get("/")
def health():
    return {"status": "ok", "whisper_model": WHISPER_MODEL, "llm_model": LLM_MODEL}


@app.post("/process-audio")
async def process_audio(file: UploadFile = File(...)):
    if not os.environ.get("GROQ_API_KEY"):
        raise HTTPException(status_code=500, detail="GROQ_API_KEY environment variable is not set.")

    content_type = (file.content_type or "").lower()
    filename = (file.filename or "").lower()
    suffix = ".mp4" if ("mp4" in content_type or filename.endswith((".mp4", ".m4a"))) else ".webm"

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        if os.path.getsize(tmp_path) == 0:
            raise HTTPException(status_code=400, detail="Uploaded audio file is empty.")

        transcript = transcribe_audio(tmp_path)
        if not transcript:
            raise HTTPException(status_code=422, detail="No speech detected in the recording.")

        clinical_json = structure_transcript(transcript)
        return {"transcript": transcript, "clinical_json": clinical_json}
    except HTTPException:
        raise
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=502, detail=f"LLM returned invalid JSON: {exc}")
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Processing failed: {exc}")
    finally:
        await file.close()
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
