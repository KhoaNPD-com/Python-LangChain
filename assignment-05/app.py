# =====================================
# Install dependency (run once)
# =====================================
# !pip install llama-cpp-python

from llama_cpp import Llama
import os
import urllib.request


# =====================================
# Model Class
# =====================================
class LlamaModel:
    def __init__(self, model_path, n_ctx=4096):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found: {model_path}")

        try:
            self.llm = Llama(
                model_path=model_path,
                n_ctx=n_ctx,
                verbose=False  # ✅ remove noisy logs
            )
            print("[INFO] Model loaded successfully")
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")

    def generate(self, prompt, max_tokens=800):
        try:
            output = self.llm(
                prompt,
                max_tokens=max_tokens,
                temperature=0.5,
                top_p=0.9,
                stop=["</s>"]
            )

            text = output["choices"][0]["text"].strip()

            # ✅ Retry if bad output
            if not text or len(text) < 50 or "thank you" in text.lower():
                output = self.llm(
                    prompt,
                    max_tokens=max_tokens,
                    temperature=0.4,
                    top_p=0.9,
                    stop=["</s>"]
                )
                text = output["choices"][0]["text"].strip()

            return text if text else "[WARNING] Empty output"

        except Exception as e:
            raise RuntimeError(f"Generation failed: {e}")


# =====================================
# Downloader Class
# =====================================
class ModelDownloader:
    def __init__(self, url, file_name):
        self.url = url
        self.file_name = file_name

    def download(self):
        if os.path.exists(self.file_name):
            print("[INFO] Model already exists")
            return self.file_name

        try:
            print("[INFO] Downloading model...")
            urllib.request.urlretrieve(self.url, self.file_name)
            print("[INFO] Download complete")
            return self.file_name
        except Exception as e:
            raise RuntimeError(f"Download failed: {e}")


# =====================================
# Resume Generator Class
# =====================================
class ResumeGenerator:
    def __init__(self, model):
        self.model = model

    def build_prompt(self, data):
        return f"""[INST]
You are a resume generation AI.

STRICT RULES:
- Return ONLY the resume
- DO NOT say "thank you"
- DO NOT add explanations
- Use EXACT format below

FORMAT:

Name: ...
Contact:
- Email: ...
- Phone: ...

Summary:
...

Skills:
- ...

Experience:
- ...

Education:
- ...

Projects:
- ...

Generate resume from:

Name: {data['name']}
Email: {data['email']}
Phone: {data['phone']}
Skills: {', '.join(data['skills'])}
Experience: {data['experience']}
Education: {data['education']}
Projects: {data['projects']}

[/INST]"""

    def generate_resume(self, data):
        try:
            prompt = self.build_prompt(data)
            return self.model.generate(prompt)
        except Exception as e:
            return f"[ERROR] {e}"


# =====================================
# App Controller
# =====================================
class ResumeApp:
    def __init__(self):
        self.model_file = "llama-2-7b-chat.Q4_K_M.gguf"
        self.model_url = (
            "https://huggingface.co/TheBloke/"
            "Llama-2-7B-Chat-GGUF/resolve/main/"
            "llama-2-7b-chat.Q4_K_M.gguf"
        )

    def run(self):
        try:
            # Download model
            downloader = ModelDownloader(self.model_url, self.model_file)
            model_path = downloader.download()

            # Load model
            model = LlamaModel(model_path)

            # Resume generator
            generator = ResumeGenerator(model)

            # =====================================
            # Dummy Inputs (NO input())
            # =====================================
            samples = [
                {
                    "name": "Nguyen Van A",
                    "email": "a@gmail.com",
                    "phone": "0123456789",
                    "skills": ["Python", "Machine Learning", "SQL"],
                    "experience": "2 years ML Engineer at FPT",
                    "education": "Bachelor of Computer Science",
                    "projects": "Fraud detection system using XGBoost"
                },
                {
                    "name": "Tran Thi B",
                    "email": "b@gmail.com",
                    "phone": "0987654321",
                    "skills": ["React", "Node.js", "MongoDB"],
                    "experience": "3 years Fullstack Developer",
                    "education": "Software Engineering Degree",
                    "projects": "E-commerce web app"
                },
                {
                    "name": "Le Van C",
                    "email": "c@gmail.com",
                    "phone": "0111222333",
                    "skills": ["Embedded C", "AUTOSAR", "MCAL"],
                    "experience": "4 years Embedded Engineer",
                    "education": "Electrical Engineering",
                    "projects": "Automotive ECU development"
                }
            ]

            # =====================================
            # Generate Resumes
            # =====================================
            for i, data in enumerate(samples):
                print(f"\n================ SAMPLE {i+1} INPUT ================\n")
                print(data)

                print(f"\n================ SAMPLE {i+1} OUTPUT ================\n")
                resume = generator.generate_resume(data)
                print(resume)

        except Exception as e:
            print(f"[FATAL ERROR] {e}")


# =====================================
# Run
# =====================================
if __name__ == "__main__":
    app = ResumeApp()
    app.run()