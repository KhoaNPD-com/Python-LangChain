import pandas as pd
import openai

import os


# -----------------------------
# CONFIG
# -----------------------------
from dotenv import load_dotenv
load_dotenv()

client = openai.OpenAI(
    base_url=os.getenv("OPENAI_ENDPOINT"),
    api_key=os.getenv("OPENAI_GPT_4O_API_KEY")
)


CATEGORIES = [
    "Traffic",
    "Customer Issue",
    "Vehicle Issue",
    "Weather",
    "Sorting/Labeling Error",
    "Human Error",
    "Technical System Failure",
    "Other"
]

# -----------------------------
# PREPROCESS
# -----------------------------
def preprocess(text):
    return str(text).lower().strip()

# -----------------------------
# KEYWORD BASELINE
# -----------------------------
KEYWORDS = {
    "Traffic": ["traffic", "jam", "congestion"],
    "Customer Issue": ["customer", "not available", "reschedule"],
    "Vehicle Issue": ["vehicle", "broke", "engine", "failure"],
    "Weather": ["rain", "storm", "weather", "flood"],
    "Sorting/Labeling Error": ["label", "sorting", "incorrect"],
    "Human Error": ["forgot", "mistake"],
    "Technical System Failure": ["system", "outage", "server"]
}

def keyword_classify(text):
    text = preprocess(text)
    for category, kws in KEYWORDS.items():
        if any(kw in text for kw in kws):
            return category
    return "Other"

# -----------------------------
# LLM CLASSIFIER (fallback)
# -----------------------------
def llm_classify(log_text):
    prompt = f"""
Classify the following logistics delay log into one category:

{CATEGORIES}

Log: "{log_text}"

Return ONLY the category name.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a logistics classification assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()

# -----------------------------
# FINAL PIPELINE
# -----------------------------
def classify_log(log_text):
    base = keyword_classify(log_text)

    if base != "Other":
        return base  # fast path

    return llm_classify(log_text)

# -----------------------------
# LOAD CSV
# -----------------------------
df = pd.read_csv("dataset.csv")


df["predicted_category"] = df["log_entry"].apply(classify_log)

# -----------------------------
# SAVE OUTPUT
# -----------------------------
df.to_csv("classified_logs.csv", index=False)

print(df.head())
