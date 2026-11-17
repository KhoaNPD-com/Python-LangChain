# Step 1: Import libraries
from transformers import VitsModel, AutoTokenizer
import torch
import numpy as np
import soundfile as sf
from IPython.display import Audio

# Step 2: Load model + tokenizer from Hugging Face
model_name = "facebook/mms-tts-eng"

model = VitsModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Step 3: Input text
text = "Welcome to AI Application Engineer"

# Step 4: Tokenize
inputs = tokenizer(text, return_tensors="pt")

# Step 5: Generate speech
with torch.no_grad():
    output = model(**inputs).waveform

# Convert tensor → numpy
waveform = output.squeeze().cpu().numpy()

# Step 6A: Play audio (Jupyter)
print("Playing generated audio...")
Audio(waveform, rate=model.config.sampling_rate)

# Step 6B: Save audio to file
sf.write("output.wav", waveform, model.config.sampling_rate)
print("Saved audio to output.wav")