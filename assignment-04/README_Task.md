README

1. How to run the script

Step 1: Install dependencies
pip install openai tenacity python-dotenv

Step 2: Create a .env file
OPENAI_API_KEY=
OPENAI_ENDPOINT=

Step 3: Run the script
python app.py

2. Design choices

Batching:

- Used sequential batch processing for simplicity and stability
- Each input is processed independently in a loop
- Added a small delay (time.sleep) between requests to reduce rate limit issues
- If one item fails, the rest of the batch continues

Function calling:

- Used OpenAI tools (function calling) to enforce structured JSON output
- Defined schema "draft_support_email" to standardize responses
- Eliminates need for manual text parsing

Retry mechanism:

- Implemented using tenacity library
- wait_random_exponential(min=1, max=10) for backoff strategy
- stop_after_attempt(5) limits retry attempts
- Retries only on RateLimitError and APIError
- Helps maintain stability under API limits

3. Challenges and solutions

Challenge: API rate limits
Solution:

- Added exponential backoff retry mechanism
- Introduced delay between batch requests

Challenge: Unstructured outputs
Solution:

- Used function calling with predefined schema
- Extracted structured JSON from tool_calls

Challenge: Partial failures in batch
Solution:

- Wrapped each request in try/except
- Logged errors and continued processing
- Stored error results instead of stopping execution

Challenge: Response parsing errors
Solution:

- Separated parsing logic into dedicated function
- Added exception handling for JSON parsing

4. Summary

- Supports batch processing of multiple inputs
- Ensures structured output using function calling
- Handles rate limits with retry strategy
- Provides robust error handling
- Designed for reliability and easy extension
