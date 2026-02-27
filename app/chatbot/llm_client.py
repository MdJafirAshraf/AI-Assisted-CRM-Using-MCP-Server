from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.tools.base import ToolException
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import SystemMessage, HumanMessage
from app.chatbot.handle_error import handle_tool_error
from dotenv import load_dotenv

load_dotenv()

# Global Model (Stateless, safe to reuse)
model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
)

async def process_query(query: str, base_url: str, access_token: str = None) -> str:
    """
    Process query using MCP tools via LangChain agent.
    Instantiates a FRESH client per request to inject the correct Bearer token.
    """
    
    # This dictionary is recreated for every single request
    connection_config = {
        "mcpstore": {
            "url": base_url,
            "transport": "streamable_http",
            "headers": {
                "Authorization": f"Bearer {access_token}"
            } if access_token else {}
        }
    }

    try:
        mcp_client = MultiServerMCPClient(connection_config)
        
        # This establishes the connection using the headers defined above
        tools = await mcp_client.get_tools()
        
        # Create Agent
        agent = create_agent(model, tools)

        system_msg = '''You are a CRM assistant. Format results clearly. Never mention tools.'''
        messages = [
            SystemMessage(content=system_msg),
            HumanMessage(content=query)
        ]

        # Invoke
        response = await agent.ainvoke({"messages": messages})
        final_response = response["messages"][-1].content
        print("\nFinal Response:", final_response)

        return final_response
    
    except ToolException as e:
        return handle_tool_error(e)

    except Exception as e:
        print(f"Error processing query: {e}") 
        return "Something went wrong. Please try again."
