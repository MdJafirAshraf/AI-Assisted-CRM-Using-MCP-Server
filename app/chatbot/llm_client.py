from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.tools.base import ToolException
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import SystemMessage, HumanMessage
from app.chatbot.handle_error import handle_tool_error

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize model
model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
)


async def process_query(query: str, base_url: str) -> str:
    """Process query using MCP tools via LangChain agent."""

    # Initialize MCP Client
    client = MultiServerMCPClient(
        {
            "mcpstore": {
                "url": base_url,
                "transport": "streamable_http",
            }
        }
    )

    # Fetch tools from MCP server
    tools = await client.get_tools()

    # Create tool-calling agent
    agent = create_agent(model, tools)

    # Correct message format
    system_msg = '''You are a CRM assistant. Format results clearly. Never mention tools.'''
    messages = [
        SystemMessage(content=system_msg),
        HumanMessage(content=query)
    ]

    try:
        response = await agent.ainvoke({"messages": messages})
        final_response = response["messages"][-1].content
        print("\nFinal Response:", final_response)

        return final_response
    
    except ToolException as e:
        return handle_tool_error(e)

    except Exception as e:
        return "Something went wrong. Please try again."