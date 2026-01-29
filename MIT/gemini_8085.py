import google.generativeai as genai

def setup_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")

def generate_8085(model, question, value):
    prompt = f"""
You are an expert in 8085 microprocessor programming.

Rules:
- Generate ONLY valid GNUSim8085 assembly code
- Use uppercase hex digits
- Always suffix hex values with H
- End program with HLT
- Do NOT add comments or explanations

Replace all variable data with this value: {value}

Question:
{question}
"""

    response = model.generate_content(prompt)
    return response.text.strip()
