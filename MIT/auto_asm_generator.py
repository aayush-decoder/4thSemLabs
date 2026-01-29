import os
from pdf_reader import extract_questions
from gemini_8085 import setup_gemini, generate_8085

# ===== USER INPUT =====
API_KEY = input("Enter Gemini API Key: ").strip()
PDF_PATH = input("Enter PDF path: ").strip()
NUM = int(input("Enter data value (decimal): "))

# ===== HEX HANDLING =====
if NUM > 100:
    VALUE = hex(NUM).upper().replace("0X", "") + "H"
else:
    VALUE = str(NUM) + "H"

model = setup_gemini(API_KEY)
questions = extract_questions(PDF_PATH)

os.makedirs("asm_files", exist_ok=True)

for q_no, q_text in questions:
    print(f"Generating q{q_no}.asm")

    asm_code = generate_8085(model, q_text, VALUE)

    with open(f"asm_files/q{q_no}.asm", "w") as f:
        f.write(asm_code + "\n")

print("\nDone! ASM files generated successfully.")
