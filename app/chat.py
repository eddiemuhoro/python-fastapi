# chat.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Literal, Optional
from fastapi.responses import JSONResponse
from .database import get_db
from .crud import create_conversation, get_conversation, create_message, get_messages_by_conversation
from sqlalchemy.ext.asyncio import AsyncSession
from openai import OpenAI
import os

router = APIRouter()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Define Pydantic models
class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str
    name: Optional[str] = None
    user_id: Optional[str] = '12'
    is_new: Optional[bool] = False

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

@router.post("/api/chat")
async def post_chat(chat_request: ChatRequest, db: AsyncSession = Depends(get_db)):
    try:
        user_id = chat_request.messages[0].user_id or "anonymous"

        # Retrieve existing conversation or create a new one
        conversation = await get_conversation(db=db, user_id=user_id)
        if chat_request.messages[0].is_new or not conversation:
            conversation = await create_conversation(db=db, user_id=user_id)

        last_user_message = next((msg for msg in reversed(chat_request.messages) if msg.role == "user"), None)
        # Save user messages
        if last_user_message:
            await create_message(db=db, conversation_id=conversation.id, role="user", content=last_user_message.content)

        system_message = {
            "role": "system",
            "content": "You are a travel assistant providing detailed information on travel document requirements."
        }
        openai_messages = [system_message] + [msg.dict() for msg in chat_request.messages]

        # Generate assistant response
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=openai_messages,
        )
        reply = response.choices[0].message.content

        # Save assistant message
        await create_message(db=db, conversation_id=conversation.id, role="assistant", content=reply)

        return JSONResponse(content={"reply": reply}, status_code=200)

    except Exception as e:
        print("OpenAI API error:", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/chat/{conversation_id}/history")
async def get_chat_history(conversation_id: int, db: AsyncSession = Depends(get_db)):
    try:
        messages = await get_messages_by_conversation(db, conversation_id)
        return [
            {"role": msg.role, "content": msg.content, "timestamp": msg.timestamp}
            for msg in messages
        ]
    except Exception as e:
        print("Error loading messages:", e)
        raise HTTPException(status_code=500, detail=str(e))
