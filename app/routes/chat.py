from fastapi import APIRouter, Request

from app.schemas.chat import ChatRequest, ChatResponse
from app.chatbot.llm_client import process_query


router = APIRouter(tags=["Chatbot"])


@router.post("/api/chat", summary="Chat with CRM AI assistant", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest, request: Request):
    """
    Send a natural-language message to the CRM chatbot.
    The AI assistant can perform CRM operations like creating leads,
    finding top contacts, removing records, and answering queries.
    """
    base_url = str(request.base_url).rstrip("/") + '/llm/mcp'  # Base URL for internal API calls
    print(f"Received chat query: {payload.message}, using MCP base URL: {base_url}")

    reply = await process_query(
        query=payload.message, 
        base_url=base_url
    )

    return ChatResponse(reply=reply)
