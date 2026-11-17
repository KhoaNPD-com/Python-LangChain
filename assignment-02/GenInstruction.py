import os
import openai 
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env
load_dotenv()

# Step 1: Mock Input Data
task_descriptions = [
    "Install the battery module in the rear compartment, connect to the high-voltage harness, and verify torque on fasteners.",
    "Calibrate the ADAS (Advanced Driver Assistance Systems) radar sensors on the front bumper using factory alignment targets.",
    "Apply anti-corrosion sealant to all exposed welds on the door panels before painting.",
    "Perform leak test on coolant system after radiator installation. Record pressure readings and verify against specifications.",
    "Program the infotainment ECU with the latest software package and validate connectivity with dashboard display."
]

# Step 2: Azure OpenAI Client Setup
client = openai.OpenAI(
    base_url=os.getenv("OPENAI_ENDPOINT"),
    api_key=os.getenv("OPENAI_API_KEY")
)

# deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")

# Step 3: Prompt Function
def generate_instruction(task):
    prompt = f"""
You are an expert automotive manufacturing supervisor.

Generate clear, structured work instructions for factory workers.

Requirements:
- Numbered steps
- Include safety precautions
- Include required tools/equipment
- Include acceptance criteria/quality checks
- Keep instructions concise and practical

Task:
\"\"\"{task}\"\"\"

Work Instructions:
"""

    # response = client.chat.completions.create(
    #     model=deployment_name,
    #     messages=[{"role": "user", "content": prompt}],
    #     temperature=0,
    # )

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return response.choices[0].message.content


# Step 4: Generate Instructions for All Tasks
results = []

for i, task in enumerate(task_descriptions, start=1):
    instructions = generate_instruction(task)

    results.append({
        "ID": i,
        "Task Description": task,
        "Generated Work Instructions": instructions
    })

# Step 5: Save Output to Excel
df = pd.DataFrame(results)
output_file = "work_instructions_output.xlsx"
df.to_excel(output_file, index=False, engine="openpyxl")

print(f"Work instructions generated and saved to {output_file}")