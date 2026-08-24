from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

models_to_test = [
    "gemini-2.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.7-flash"
]

for model in models_to_test:
    print(f"Testing model: {model}...")
    try:
        response = client.models.generate_content(
            model=model,
            contents="Respond with only one word: Success"
        )
        print(f"-> {model} works! Response: {response.text.strip()}")
    except Exception as e:
        print(f"-> {model} failed: {e}\n")
