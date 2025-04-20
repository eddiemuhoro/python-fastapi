from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Literal, Optional
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables from .env file
load_dotenv(dotenv_path="app/.env")

# Retrieve the OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key is not set. Please check your .env file.")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

router = APIRouter()

# Define the structure for chat messages
class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str
    name: Optional[str] = None

# Define the structure for the chat request
class ChatRequest(BaseModel):
    messages: List[ChatMessage]

# Define the POST endpoint for chat
@router.post("/api/chat")
async def post_chat(chat_request: ChatRequest):
    try:
        # Create a chat completion using the OpenAI client
        response = client.chat.completions.create(
            model="gpt-4.1-nano",  # Ensure this model is available to your account
            messages=[msg.model_dump() for msg in chat_request.messages],
        )
        # Extract the reply from the response
        reply = response.choices[0].message.content
        return JSONResponse(content={"reply": reply}, status_code=200)

    except Exception as e:
        print("OpenAI API error:", e)
        raise HTTPException(status_code=500, detail=str(e))
