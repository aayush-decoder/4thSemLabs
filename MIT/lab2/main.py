import os

# ===== USER INPUT =====
num = int(input("Enter a number (decimal): "))

# Convert to hex if > 100
if num > 100:
    value = hex(num).upper().replace("0X", "") + "H"
else:
    value = str(num) + "H"

print(f"Using value: {value}")

# ===== PROGRAMS =====
programs = {
    1: f"""LXI H, 0008H
MOV B, M
HLT
""",

    2: f"""LXI H, 0008H
MVI B, {value}
MOV M, B
HLT
""",

    3: f"""MVI A, 38H
MVI B, {value}
ADD B
OUT 02H
HLT
""",

    4: f"""MVI A, 2AH
ADI {value}
STA 003FH
HLT
""",

    5: f"""LXI H, 0008H
MVI M, {value}
MVI A, 10H
ADD M
HLT
""",

    6: f"""MVI A, 99H
MVI B, {value}
SUB B
OUT 02H
HLT
""",

    7: f"""MVI A, 0C1H
SUI {value}
STA 003FH
HLT
""",

    8: f"""LXI H, 0008H
MVI M, {value}
MVI A, 95H
SUB M
HLT
""",

    9: f"""MVI A, {value}
STA 0008H
HLT
""",

    10: f"""MVI A, 93H
STA 003EH
MVI A, B7H
STA 0005H
LDA 003EH
MOV B, A
LDA 0005H
ADD B
OUT 07FH
HLT
""",

    11: f"""MVI A, 4FH
STA 007FH
MVI A, 78H
OUT 0005H
LDA 007FH
ADI 78H
OUT 07FH
HLT
"""
}

os.makedirs("asm_files", exist_ok=True)

for q_no, code in programs.items():
    with open(f"q{q_no}.asm", "w") as f:
        f.write(code)

print("done!!!")
