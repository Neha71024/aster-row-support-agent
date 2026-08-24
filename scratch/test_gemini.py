import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

def mock_tool(arg: str) -> str:
    """A mock tool for testing."""
    return f"Result for {arg}"

try:
    print("Testing connection...")
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Hello, respond in exactly one word: 'Success'."
    )
    print("Gemini response:", response.text.strip())

    print("\nTesting tools registration...")
    config = types.GenerateContentConfig(
        tools=[mock_tool],
        system_instruction="Use mock_tool if asked."
    )
    print("Tool config generated successfully!")
except Exception as e:
    print("Error during test:", e)
