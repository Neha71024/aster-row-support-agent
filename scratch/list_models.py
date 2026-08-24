from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

try:
    print("Available models:")
    # Retrieve all models and print their names
    for model in client.models.list():
        print(f"- {model.name} (Supported actions: {model.supported_actions})")
except Exception as e:
    print("Error listing models:", e)
