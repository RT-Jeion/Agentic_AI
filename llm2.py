import os
import asyncio
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

async def call_llm(user_input, user):

    # users info
    user_id = int(user.id)
    username = user.username
    name = user.full_name
    db_name = name

    client = Groq(api_key=api_key)

    # Define the system prompt
    system_instruction = "You are a helpful, witty, and concise AI chatbot companion. don't answer long.."

    # Start the chat session
    chat_completion = client.chat.completions.create(
    messages=[
        # Set an optional system message. This sets the behavior of the
        # assistant and can be used to provide specific instructions for
        # how it should behave throughout the conversation.
        {
            "role": "system",
            "content": system_instruction
        },
        # Set a user message for the assistant to respond to.
        {
            "role": "user",
            "content": user_input,
        }
    ],

    # The language model which will generate the completion.
    model="meta-llama/llama-4-scout-17b-16e-instruct"
)

# Print the completion returned by the LLM.
    response = chat_completion.choices[0].message.content

        
    print(f"Bot: {response}\n")
    return response 
