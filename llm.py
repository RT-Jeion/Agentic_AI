import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from the .env file
load_dotenv()
api = os.getenv("GEMINI_API_KEY")
# Initialize the client (it automatically looks for GEMINI_API_KEY in the environment)
def call_llm(user_input):
    client = genai.Client(api_key=api)

    # Define the system prompt
    system_instruction = "You are a helpful, witty, and concise AI chatbot companion. don't answer long.."

    # Start the chat session
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7,
        )
    )

    print("Chatbot initialized! Type 'quit' to exit.\n")
        
    response = chat.send_message(user_input)
    print(f"Bot: {response.text}\n")
    return response.text    