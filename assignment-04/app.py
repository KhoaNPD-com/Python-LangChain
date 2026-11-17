import os
import time
import json
import logging
import openai
from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type

# ==============================
# LOAD ENV
# ==============================
load_dotenv()

client = openai.OpenAI(
    base_url=os.getenv("OPENAI_ENDPOINT"),  
    api_key=os.getenv("OPENAI_API_KEY")
)

# ==============================
# LOGGING
# ==============================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==============================
# FUNCTION SCHEMA
# ==============================
tools = [
    {
        "type": "function",
        "function": {
            "name": "draft_support_email",
            "description": "Generate a structured customer support email",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_issue": {"type": "string"},
                    "tone": {"type": "string"},
                    "response": {"type": "string"}
                },
                "required": ["customer_issue", "tone", "response"]
            }
        }
    }
]

# ==============================
# RETRY CALL
# ==============================
@retry(
    retry=retry_if_exception_type((openai.RateLimitError, openai.APIError)),
    wait=wait_random_exponential(min=1, max=10),
    stop=stop_after_attempt(5),
    reraise=True
)
def call_openai(prompt, issue, tone):
    logger.info(f"Calling API for issue: {issue}")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Always return a complete email in the 'response' field."},
            {
                "role": "user",
                "content": f"{prompt}\nIssue: {issue}\nTone: {tone}\nGenerate the full email response."
            }
        ],
        tools=tools,
        tool_choice={
            "type": "function",
            "function": {"name": "draft_support_email"}
        }
    )

    return response

# ==============================
# PARSER
# ==============================
def parse_response(resp):
    try:
        msg = resp.choices[0].message

        if msg.tool_calls:
            args = msg.tool_calls[0].function.arguments
            return json.loads(args)

        return {"error": "No tool_calls returned"}

    except Exception as e:
        logger.error(f"Parse error: {e}")
        return {"error": str(e)}

# ==============================
# BATCH PROCESS
# ==============================
def batch_process(inputs, delay=1):
    results = []

    for i, item in enumerate(inputs):
        try:
            res = call_openai(
                item["prompt"],
                item["customer_issue"],
                item["tone"]
            )

            parsed = parse_response(res)
            results.append(parsed)

            logger.info(f"Processed {i+1}/{len(inputs)}")
            time.sleep(delay)

        except Exception as e:
            logger.error(f"Error at item {i}: {e}")
            results.append({"error": str(e)})

    return results

# ==============================
# SAMPLE INPUTS
# ==============================
batch_inputs = [
    {
        "prompt": "Write a support email",
        "customer_issue": "Order not delivered after 10 days",
        "tone": "formal"
    },
    {
        "prompt": "Write a support email",
        "customer_issue": "Received damaged product",
        "tone": "friendly"
    },
    {
        "prompt": "Write a support email",
        "customer_issue": "Cannot login to account",
        "tone": "professional"
    }
]

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    outputs = batch_process(batch_inputs)

    print("\n===== FINAL OUTPUT =====")
    for i, out in enumerate(outputs):
        print(f"\nCase {i+1}:")
        print(json.dumps(out, indent=2))