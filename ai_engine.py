
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")


def ask_ai(question):

    if not API_KEY:
        return "Groq API key is not configured."

    try:
        client = Groq(api_key=API_KEY)

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Abhinav AI, a professional personal "
                        "AI assistant. Always reply in English. "
                        "Be friendly, intelligent and concise."
                    )
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            max_tokens=1000
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error: {str(e)}"
