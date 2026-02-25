from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.chatbot import process_chat_message

router = APIRouter(tags=["Chatbot"])


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@router.post("/api/chat", summary="Chat with CRM AI assistant", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest, request: Request):
    """
    Send a natural-language message to the CRM chatbot.
    The AI assistant can perform CRM operations like creating leads,
    finding top contacts, removing records, and answering queries.
    """
    base_url = str(request.base_url).rstrip("/")
    reply = await process_chat_message(payload.message, base_url)
    return ChatResponse(reply=reply)
