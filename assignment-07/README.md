# Text-to-Speech (TTS) with Hugging Face

## Objective

- Clone a pre-trained Text-to-Speech (TTS) model from Hugging Face
- Perform inference to convert text into speech
- Save the generated speech as an audio file

---

## Installation

Install required dependencies:

Be aware that a model will be downloaded at the first time running.

```bash
pip install torch transformers soundfile datasets sentencepiece
```

<h2> How to run

python app.py


## Challenges Faced & Solutions

### 1. Missing Speaker Embeddings

* ❌ Issue: SpeechT5 requires speaker embeddings; without them, generation fails
* ✅ Solution: Used `cmu-arctic-xvectors` dataset to provide embeddings

---

### 2. Model Complexity

* ❌ Issue: TTS pipeline involves multiple components (processor, model, vocoder)
* ✅ Solution: Carefully loaded each component and connected them step-by-step

---

### 3. Audio Output Format

* ❌ Issue: Raw model output is not directly playable
* ✅ Solution: Converted output to `.wav` using `soundfile`

---

### 4. Performance

* ❌ Issue: Inference can be slow on CPU
* ✅ Solution: Disabled gradients and used small input text for faster execution

---

## Optional Improvements

* Add GPU support (`model.to("cuda")`)
* Create batch processing for multiple inputs
* Build a CLI tool (no manual input)
* Deploy with Hugging Face Spaces (Gradio UI)
