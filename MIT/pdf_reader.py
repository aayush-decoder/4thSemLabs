import fitz
import re
def extract_questions(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text() + "\n"

    # Normalize spaces
    text = re.sub(r"\s+", " ", text)

    # Match:
    # 1 Write ...
    # 2 Write ...
    pattern = re.compile(
        r"(\d+)\s+(Write instruction.*?)(?=\s+\d+\s+Write instruction|\Z)",
        re.IGNORECASE
    )

    matches = pattern.findall(text)

    return [(int(q_no), q_text.strip()) for q_no, q_text in matches]
