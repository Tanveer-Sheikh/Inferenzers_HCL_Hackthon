"""
LLM utility module - extracted from LLM.ipynb
Handles text enhancement and field extraction using OpenAI
"""
import os
import re
import json
from typing import Dict
from openai import OpenAI


# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "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"
MODEL_NAME = "gpt-4o-mini"
MAX_CHARS = 1500


def get_client():
    """Get OpenAI client"""
    key = os.getenv("OPENAI_API_KEY") or OPENAI_API_KEY
    if not key or "PASTE" in key:
        raise ValueError("Set OPENAI_API_KEY env or replace with your key.")
    return OpenAI(api_key=key)


def chat(prompt, max_tokens=400):
    """Send a chat completion request to OpenAI"""
    client = get_client()
    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0,
    )
    return resp.choices[0].message.content.strip()


def enhance_text(raw_text, max_tokens=196):
    """Clean and normalize OCR text"""
    clipped = raw_text[:MAX_CHARS]
    prompt = (
        "Clean and normalize this OCR text from a filled form. "
        "Keep all fields, fix spacing/casing, and remove obvious OCR artifacts only. "
        "Do NOT invent values. Return the cleaned text.\n"
        f"OCR text:\n{clipped}"
    )
    return chat(prompt, max_tokens=max_tokens)


FIELD_SCHEMA = {
    "name": "",
    "dob": "",
    "address": "",
    "city": "",
    "state": "",
    "zip": "",
    "phone": "",
    "email": "",
    "gender": "",
    "marital_status": "",
    "occupation": "",
    "emergency_contact_name": "",
    "emergency_contact_phone": "",
    "policy_number": "",
    "date": "",
}


def clean_value(text):
    """Clean extracted value"""
    return re.sub(r"\s+", " ", text).strip(" ,;:-")


def enforce_formats(fields):
    """Enforce format rules on extracted fields"""
    out = dict(fields)
    if out.get("name"):
        name = re.sub(r"[^A-Za-z .'-]", "", out["name"])
        name = re.split(r"\bDOB\b", name, flags=re.IGNORECASE)[0]
        out["name"] = name.strip()
    for k in ["dob", "date"]:
        if out.get(k):
            val = re.sub(r"[^0-9/\\-]", "", out[k])
            out[k] = val.strip("-/")
    for k in ["phone", "emergency_contact_phone"]:
        if out.get(k):
            phone = re.sub(r"[^0-9+]", "", out[k])
            out[k] = phone
    if out.get("zip"):
        out["zip"] = re.sub(r"[^0-9]", "", out["zip"])
    if out.get("email"):
        email = out["email"].lower()
        m = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", email)
        out["email"] = m.group(0) if m else ""
    return out


def heuristic_extract(clean_text):
    """Heuristic extraction as fallback"""
    out = {}
    name_match = re.search(r"Name[:\s]+([A-Za-z][A-Za-z\s.'-]{1,40})", clean_text, re.IGNORECASE)
    dob_match = re.search(r"DOB[:\s]+([0-9]{1,2}[\-/][0-9]{1,2}[\-/][0-9]{2,4})", clean_text, re.IGNORECASE)
    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", clean_text)
    phone_match = re.search(r"Phone[:\s#]*([+\d][\d\s()\-]{7,20})", clean_text, re.IGNORECASE)
    if name_match:
        out["name"] = clean_value(name_match.group(1))
    if dob_match:
        out["dob"] = clean_value(dob_match.group(1))
    if email_match:
        out["email"] = clean_value(email_match.group(0))
    if phone_match:
        out["phone"] = clean_value(phone_match.group(1))
    return out


def extract_fields(clean_text, max_tokens=196):
    """Extract structured fields from cleaned text"""
    clipped = clean_text[:MAX_CHARS]
    schema_lines = "\n".join([f"- {k}" for k in FIELD_SCHEMA.keys()])
    prompt = (
        "Extract the following fields from the cleaned OCR form text. "
        "Respond ONLY as a single-line JSON object with exactly these keys. "
        "If a field is missing, use an empty string. Do NOT add text outside JSON.\n"
        f"Fields:\n{schema_lines}\n"
        f"Clean text:\n{clipped}"
    )
    text = chat(prompt, max_tokens=max_tokens)
    parsed = None
    try:
        parsed = json.loads(text)
    except Exception:
        parsed = None

    fields = {k: "" for k in FIELD_SCHEMA.keys()}
    if isinstance(parsed, dict):
        for k in fields.keys():
            if k in parsed and isinstance(parsed[k], str):
                fields[k] = clean_value(parsed.get(k, ""))
    else:
        fields["raw_extraction"] = text

    # Fallback to heuristics
    heur = heuristic_extract(clipped)
    for k, v in heur.items():
        if not fields.get(k):
            fields[k] = v

    fields = enforce_formats(fields)
    return fields


def process_ocr_text(raw_ocr_text):
    """Process OCR text: enhance and extract fields"""
    enhanced = enhance_text(raw_ocr_text)
    fields = extract_fields(enhanced)
    
    # Build QA context
    qa_context = (
        "Structured fields:\n" + str(fields) + "\n\n" + "Clean text:\n" + enhanced
    )
    
    return {
        "enhanced_text": enhanced,
        "fields": fields,
        "qa_context": qa_context
    }


def answer_query(question, context, max_tokens=128):
    """Answer a question based on the context"""
    prompt = (
        "Answer the user's question using only the provided context from a filled form. "
        "Prefer the structured fields; if a field is empty, you may cite the clean text. "
        "If the answer is missing, say 'Not found in context.'\n"
        f"Context:\n{context}\n"
        f"Question: {question}"
    )
    return chat(prompt, max_tokens=max_tokens)
