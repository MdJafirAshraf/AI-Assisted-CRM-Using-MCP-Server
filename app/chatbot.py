"""
CRM Chatbot Engine
─
Uses Google Gemini LLM to interpret natural-language user messages,
decide which CRM API to call, execute the operation via httpx,
and return a friendly response.
"""

import json
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

SYSTEM_PROMPT = """You are an AI assistant for a CRM (Customer Relationship Management) system.
You can perform CRM operations by outputting a JSON tool call. The user speaks in natural language.

Available tools (use exactly these names and parameters):

1. list_contacts() → GET /api/contacts
2. get_contact(contact_id: int) → GET /api/contacts/{contact_id}
3. create_contact(name, email, phone?, company?, position?, status?, notes?) → POST /api/contacts
4. update_contact(contact_id, name?, email?, phone?, company?, position?, status?, notes?) → PUT /api/contacts/{contact_id}
5. delete_contact(contact_id: int) → DELETE /api/contacts/{contact_id}

6. list_leads() → GET /api/leads
7. get_lead(lead_id: int) → GET /api/leads/{lead_id}
8. create_lead(name, email?, company?, source?, status?, value?, notes?) → POST /api/leads
9. update_lead(lead_id, name?, email?, company?, source?, status?, value?, notes?) → PUT /api/leads/{lead_id}
10. delete_lead(lead_id: int) → DELETE /api/leads/{lead_id}

11. list_deals() → GET /api/deals
12. get_deal(deal_id: int) → GET /api/deals/{deal_id}
13. create_deal(title, contact_id?, value?, stage?, probability?, expected_close?, notes?) → POST /api/deals
14. update_deal(deal_id, title?, contact_id?, value?, stage?, probability?, expected_close?, notes?) → PUT /api/deals/{deal_id}
15. delete_deal(deal_id: int) → DELETE /api/deals/{deal_id}

16. list_tasks() → GET /api/tasks
17. get_task(task_id: int) → GET /api/tasks/{task_id}
18. create_task(title, description?, related_to?, related_id?, priority?, status?, due_date?) → POST /api/tasks
19. update_task(task_id, title?, description?, related_to?, related_id?, priority?, status?, due_date?) → PUT /api/tasks/{task_id}
20. delete_task(task_id: int) → DELETE /api/tasks/{task_id}

RULES:
- If you need to perform an operation, respond with EXACTLY one JSON block wrapped in ```json ... ``` with:
  {"tool": "<tool_name>", "params": {<param_key: param_value>}}
- If the user just asks a question or makes a greeting, respond with a normal friendly text (no JSON).
- If the user asks "who is the top lead" or similar, call list_leads() first to get the data, then you can answer.
- For deletion by name/email: first call the list endpoint to find the ID, then call the delete endpoint.
- Always be helpful and concise.
"""


async def call_gemini(messages: list[dict]) -> str:
    """Call Google Gemini API and return the text response."""
    if not GEMINI_API_KEY:
        return "⚠️ Gemini API key not configured. Please set GEMINI_API_KEY in your .env file."

    payload = {
        "contents": messages,
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 1024,
        },
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        if resp.status_code != 200:
            return f"⚠️ Gemini API error ({resp.status_code}): {resp.text[:200]}"
        data = resp.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return "⚠️ Unexpected response from Gemini."


def parse_tool_call(text: str) -> dict | None:
    """Extract a JSON tool call from the LLM response if present."""
    if "```json" in text:
        try:
            json_str = text.split("```json")[1].split("```")[0].strip()
            return json.loads(json_str)
        except (json.JSONDecodeError, IndexError):
            return None
    # Try parsing the entire response as JSON
    try:
        parsed = json.loads(text.strip())
        if "tool" in parsed:
            return parsed
    except json.JSONDecodeError:
        pass
    return None


def build_api_request(tool_call: dict, base_url: str) -> tuple[str, str, dict]:
    """Convert a tool call dict to (method, url, params)."""
    tool = tool_call["tool"]
    params = tool_call.get("params", {})

    mapping = {
        "list_contacts":  ("GET",    "/api/contacts",   {}),
        "get_contact":    ("GET",    f"/api/contacts/{params.get('contact_id', '')}",  {}),
        "create_contact": ("POST",   "/api/contacts",   {k: v for k, v in params.items()}),
        "update_contact": ("PUT",    f"/api/contacts/{params.pop('contact_id', '')}",  params),
        "delete_contact": ("DELETE", f"/api/contacts/{params.get('contact_id', '')}",  {}),

        "list_leads":     ("GET",    "/api/leads",      {}),
        "get_lead":       ("GET",    f"/api/leads/{params.get('lead_id', '')}",        {}),
        "create_lead":    ("POST",   "/api/leads",      {k: v for k, v in params.items()}),
        "update_lead":    ("PUT",    f"/api/leads/{params.pop('lead_id', '')}",        params),
        "delete_lead":    ("DELETE", f"/api/leads/{params.get('lead_id', '')}",        {}),

        "list_deals":     ("GET",    "/api/deals",      {}),
        "get_deal":       ("GET",    f"/api/deals/{params.get('deal_id', '')}",        {}),
        "create_deal":    ("POST",   "/api/deals",      {k: v for k, v in params.items()}),
        "update_deal":    ("PUT",    f"/api/deals/{params.pop('deal_id', '')}",        params),
        "delete_deal":    ("DELETE", f"/api/deals/{params.get('deal_id', '')}",        {}),

        "list_tasks":     ("GET",    "/api/tasks",      {}),
        "get_task":       ("GET",    f"/api/tasks/{params.get('task_id', '')}",        {}),
        "create_task":    ("POST",   "/api/tasks",      {k: v for k, v in params.items()}),
        "update_task":    ("PUT",    f"/api/tasks/{params.pop('task_id', '')}",        params),
        "delete_task":    ("DELETE", f"/api/tasks/{params.get('task_id', '')}",        {}),
    }

    if tool not in mapping:
        return None, None, None

    method, path, query_params = mapping[tool]
    return method, f"{base_url}{path}", query_params


async def execute_api_call(method: str, url: str, params: dict) -> dict | list | str:
    """Execute an internal CRM API call."""
    async with httpx.AsyncClient(timeout=15) as client:
        if method == "GET":
            resp = await client.get(url, params=params)
        elif method == "POST":
            resp = await client.post(url, json=params)
        elif method == "PUT":
            resp = await client.put(url, json=params)
        elif method == "DELETE":
            resp = await client.delete(url, params=params)
        else:
            return "Unsupported method"

        if resp.status_code >= 400:
            return f"API error ({resp.status_code}): {resp.text[:200]}"
        return resp.json()


async def process_chat_message(user_message: str, base_url: str) -> str:
    """
    Main chatbot flow:
    1. Send user message + system prompt to Gemini
    2. If Gemini returns a tool call → execute it → summarise result
    3. If Gemini returns plain text → return it directly
    """

    # Step 1: Ask LLM what to do
    messages = [
        {"role": "user", "parts": [{"text": SYSTEM_PROMPT + "\n\nUser message: " + user_message}]},
    ]

    llm_response = await call_gemini(messages)

    # Step 2: Check for tool call
    tool_call = parse_tool_call(llm_response)
    if not tool_call:
        # Plain text answer from the LLM
        return llm_response

    # Step 3: Execute the API call
    method, url, params = build_api_request(tool_call, base_url)
    if not method:
        return f"I understood you want to use tool '{tool_call.get('tool')}', but I don't know how to handle it yet."

    api_result = await execute_api_call(method, url, params)

    # Step 4: Ask LLM to summarise the result in natural language
    summary_messages = [
        {
            "role": "user",
            "parts": [
                {
                    "text": (
                        f"The user asked: \"{user_message}\"\n"
                        f"I called the CRM API: {method} {url}\n"
                        f"API response:\n{json.dumps(api_result, indent=2, default=str)[:2000]}\n\n"
                        "Please provide a concise, friendly summary of the result for the user. "
                        "If it's a list, highlight the key items. If it's a creation/deletion, confirm what was done. "
                        "Do NOT output any JSON tool calls. Just respond in plain text."
                    )
                }
            ],
        }
    ]

    summary = await call_gemini(summary_messages)
    return summary
