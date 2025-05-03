import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-2.0-flash')

def summarize_text(text):
    try:
        prompt = f"Summarize the following YouTube transcript into 5 bullet points:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing: {e}")
        return "Sorry, I couldn't summarize this video."
