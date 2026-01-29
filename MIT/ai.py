import fitz
import re
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
PDF_PATH = os.getenv("PDF_PATH")
NUM = os.getenv("DATA_VALUE")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY missing in .env")

if not PDF_PATH:
    raise RuntimeError("PDF_PATH missing in .env")

if not NUM:
    raise RuntimeError("DATA_VALUE missing in .env")

NUM = int(NUM)

# ========= HEX CONVERSION =========
VALUE = hex(NUM).upper().replace("0X", "") + "H" if NUM > 100 else str(NUM) + "H"

# ========= PDF READER =========
def extract_questions(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text() + "\n"

    text = re.sub(r"\s+", " ", text)

    questions = re.findall(
        r"(\d+)\s+(Write instruction.*?)(?=\s+\d+\s+Write instruction|\Z)",
        text,
        re.IGNORECASE
    )

    return [(int(n), q.strip()) for n, q in questions]

# ========= GEMINI =========
def setup_gemini():
    genai.configure(api_key=API_KEY)
    return genai.GenerativeModel("gemini-2.5-flash")

# ========= RESPONSE CLEANER =========
def clean_llm_response(text: str) -> str:
    text = text.strip()

    # Remove ``` or ```json fences
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)

    return text.strip()

def generate_all_8085(model, questions, value):
    questions_json = json.dumps(
        {str(q_no): q_text for q_no, q_text in questions},
        indent=2
    )

    prompt = f"""
You are an expert in 8085 microprocessor programming.

TASK:
Convert ALL questions below into GNUSim8085 compatible assembly.

STRICT RULES:
- Output ONLY valid JSON
- JSON keys must be question numbers
- JSON values must be ONLY 8085 assembly code
- Uppercase HEX, suffix H
- End every program with HLT
- No comments, no explanations

Replace all data values with: {value}

QUESTIONS JSON:
{questions_json}
"""

    response = model.generate_content(prompt)

    raw_text = response.text
    print("----- RAW GEMINI RESPONSE -----")
    print(raw_text)
    print("-------------------------------")

    cleaned = clean_llm_response(raw_text)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        raise RuntimeError("❌ Gemini did not return valid JSON")

# ========= MAIN =========
model = setup_gemini()
questions = extract_questions(PDF_PATH)

if not questions:
    raise RuntimeError("❌ No questions extracted from PDF")

asm_map = generate_all_8085(model, questions, VALUE)

os.makedirs("asm_files", exist_ok=True)

for q_no, asm_code in asm_map.items():
    with open(f"asm_files/q{q_no}.asm", "w") as f:
        f.write(asm_code.strip() + "\n")

print("✨ DONE: ASM files generated using only .env configuration")
