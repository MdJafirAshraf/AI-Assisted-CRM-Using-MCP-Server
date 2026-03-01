from fastapi import APIRouter, Depends, Request

from app.models.users import User
from app.schemas.chat import ChatRequest, ChatResponse
from app.chatbot.llm_client import process_query
from app.dependencies.auth import get_current_user


router = APIRouter(tags=["Chatbot"])


@router.post("/api/chat", summary="Chat with CRM AI assistant", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest, request: Request, current_user: User = Depends(get_current_user)):
    """
    Send a natural-language message to the CRM chatbot.
    The AI assistant can perform CRM operations like creating leads,
    finding top contacts, removing records, and answering queries.
    """
    base_url = str(request.base_url).rstrip("/") + '/llm/mcp'  # Base URL for internal API calls
    print(f"Received chat query: {payload.message}, using MCP base URL: {base_url}")

    access_token = request.cookies.get("access_token")

    reply = await process_query(
        query=payload.message, 
        base_url=base_url,
        access_token=access_token,
        user_id=current_user.id
    )

    return ChatResponse(reply=reply)
