import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def get_self_consistent_answers(prompt, attempts=3):
    answers = []
    for _ in range(attempts):
        try:
            response = model.generate_content(prompt)
            answers.append(response.text)
        except Exception as e:
            answers.append(f"[Error] {str(e)}")
    return answers