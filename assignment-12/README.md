# README

## Project: Satellite Image Cloud Detection using OpenAI (Multimodal LLM)

---

## 1. Objective

Build a lightweight application that:

* Accepts satellite images (via URLs)
* Uses a **multimodal Large Language Model (LLM)** to analyze images
* Classifies each image as:
  * **Cloudy**
  * **Clear**
* Returns prediction along with **accuracy score**

 No traditional ML model training required

Fully API-driven inference

---

## 2. Step-by-Step Solution Approach

### Step 1: Install Dependencies

**Shell**

**pip install openai pillow requests pydantic python-dotenv**


### Step 2: Configure Environment Variables

Create a `.env` file:

---

### Step 3: Prepare Input Images

Use dummy image URLs (auto input):

**Python**

**image_urls = [**

**    "https://images.pexels.com/photos/53594/blue-clouds-day-fluffy-53594.jpeg",**

**    "https://images.pexels.com/photos/28466908/pexels-photo-28466908.jpeg",**

**    "https://images.pexels.com/photos/32049610/pexels-photo-32049610.jpeg"**

**]**

### Step 4: Convert Image → Base64

**Python**

**image_bytes = response.content**

**image_base64 = base64.b64encode(image_bytes).decode("utf-8")**


---

### Step 5: Construct Multimodal Prompt

**Python**

**messages = [**

**    {**

**        "role": "system",**

**        "content": "Classify into Cloudy or Clear with accuracy"**

**    },**

**    {**

**        "role": "user",**

**        "content": [**

**            {"type": "text", "text": "Classify this image"},**

**            {**

**                "type": "image_url",**

**                "image_url": f"data:image/jpeg;base64,{image_base64}"**

**            }**

**        ]**

**    }**

**]**

Mix of **text + image input** (multimodal)

---

### Step 6: Call OpenAI API

**Python**

**completion = client.chat.completions.create(**

**    model=os.getenv('OPENAI_MODEL_GPT_4O'),**

**    messages=messages,**

**    temperature=0**

**)**


### Step 7: Parse Structured Output

**Python**

**parsed = CloudResponse.model_validate_json(raw_output)**

Ensures:

* Reliable JSON output
* Production-safe parsing

---

### Step 8: Display Results

**Python**

**print(f"Prediction: {parsed.result}")**

**print(f"Accuracy: {parsed.accuracy}%")**


## 3. Sample Output

```
[INFO] Processing Image 1
[RESULT] Prediction: Cloudy
[RESULT] Accuracy: 94.2%

[INFO] Processing Image 2
[RESULT] Prediction: Clear
[RESULT] Accuracy: 96.5%
```

---

## 4. LangChain Multimodal Support (Concept Reference)

LangChain allows passing image data using structured message formats:

**Python**

**{**

**  "type": "image_url",**

**  "image_url": "data:image/jpeg;base64,..."**

**}**

Key Concept

* LLMs like GPT-4o support **Vision + Language**
* Images are passed alongside text in the same message
* No separate CV model required

### Reference (Conceptual)

* LangChain Chat Models support **multimodal message content**
* Structure:
  * `text`
  * `image_url`

---

## 5. Key Concepts Learned

### 1. Multimodal LLM

* Combine **image + text input**
* Enables visual reasoning using LLMs

---

### 2. API-Based Inference

* No training needed
* Direct prediction using model API

---

### 3. Base64 Image Encoding

* Required for embedding image into request payload

---

### 4. Structured Output (Pydantic)

* Enforces:
  * `result`
  * `accuracy`
* Prevents parsing errors

---

### 5. Prompt Engineering

* Restrict output format
* Improve model reliability

---

## 6. Challenges Encountered

| Challenge                      | Solution                         |
| ------------------------------ | -------------------------------- |
| Unstructured model output      | Enforced JSON response           |
| Image format issues            | Used Base64 encoding             |
| API errors (endpoint/base_url) | Configured environment variables |
| Model inconsistency            | Set temperature = 0              |

---

## 7. Limitations

* Accuracy depends on model reasoning
* Not specialized satellite model
* No batch optimization for large datasets

---

## 8. Future Improvements

* Add Streamlit web UI
* Batch dataset processing
* Confidence calibration
* Fine-tuned cloud detection model

---

## 9. Knowledge & Experience Gained

### Practical Skills

* Using OpenAI multimodal API
* Handling image data in APIs
* Structuring LLM outputs
* Debugging API integrations

---

### Conceptual Understanding

* Difference between:

  * Traditional CV models (CNN)
  * LLM-based vision models
* Learned that:
  LLM can replace ML pipelines for simple tasks

  Faster development with fewer dependencies

---

### Engineering Insight

* Importance of:
  * Clean prompt design
  * Output validation
  * Error handling

---

## 10. Conclusion

This project demonstrates a **modern approach to image classification** using LLMs:

No model training required

Simple integration via API

Scalable and flexible

Using  **OpenAI GPT-4o multimodal capabilities** , we built a fast, lightweight cloud detection system suitable for real-world applications.
