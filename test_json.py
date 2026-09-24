import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents='Return this as JSON: {"hello": "world"}',
    config={
        "response_mime_type": "application/json"
    }
)

print(response.text)

