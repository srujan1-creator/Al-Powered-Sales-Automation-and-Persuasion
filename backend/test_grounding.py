import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents="What is the stock price of Google today?",
            config=types.GenerateContentConfig(
                tools=[{"google_search": {}}]
            )
        )
        print("Success! Gemini response:")
        print(response.text)
    except Exception as e:
        print("Error:", e)
else:
    print("No API key set in .env")
