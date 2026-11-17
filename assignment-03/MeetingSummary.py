"""
AI-Powered Meeting Summarizer using Azure OpenAI

Requirements:
- Set environment variables:
  AZURE_OPENAI_ENDPOINT
  AZURE_OPENAI_API_KEY
  AZURE_DEPLOYMENT_NAME

- pip install openai
"""

import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# =============================
# CONFIGURATION
# =============================

client = openai.OpenAI(
    base_url=os.getenv("OPENAI_ENDPOINT"),
    api_key=os.getenv("OPENAI_API_KEY")
)


# =============================
# SAMPLE TRANSCRIPTS (AUTO INPUT)
# =============================
meeting_transcripts = [
    """[Project Sync]
Anna: Project chatbot is progressing.
Minh: Backend intent handling done, API testing ongoing.
Trang: Frontend has display bugs.
Anna: Update Jira today. Any blockers?
Trang: Need DevOps access.
Anna: Will arrange access.""",

    """[Marketing Strategy Meeting]
John: Campaign launch next Monday.
Lisa: Budget approved: $10,000.
David: Social media ads ready.
John: Final review Friday.
Lisa: Assign monitoring team.""",

    """[Dev Standup]
Dev1: Fixed login bug.
Dev2: Working on dashboard API.
Dev3: Need clarification on requirements.
Manager: Provide docs by tomorrow.""",

    """[AI Research Meeting]
Alice: Testing new Transformer model.
Bob: Accuracy improved by 5%.
Charlie: Need more training data.
Alice: Schedule retraining.""",

    """[Client Call]
Client: Want faster reporting.
Team: Will optimize query performance.
Client: Deadline next Friday.
Team: Will deliver updated version.""" 
]


# =============================
# SUMMARIZATION FUNCTION
# =============================
def summarize_meeting(transcript):
    prompt = f"""
    Summarize the following meeting transcript with:
    - Key Points
    - Decisions
    - Action Items

    Transcript:
    {transcript}
    """

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=[
            {"role": "system", "content": "You are an expert meeting summarizer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=400
    )

    return response.choices[0].message.content


# =============================
# MAIN EXECUTION
# =============================
def main():
    print("=" * 60)
    print("AI-Powered Meeting Summarizer\n")

    for i, transcript in enumerate(meeting_transcripts, 1):
        print("=" * 60)
        print(f"Meeting {i} Transcript:\n{transcript}\n")

        summary = summarize_meeting(transcript)

        print("Summary:\n")
        print(summary)
        print("\n")


if __name__ == "__main__":
    main()