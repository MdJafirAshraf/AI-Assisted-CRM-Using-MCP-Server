from fastmcp import Client

# connect HTTP server
client = Client("http://127.0.0.1:8000/llm/mcp/")

async def call_mcp():
    async with client:
        # Basic server interaction
        await client.ping()
        
        # List available operations
        tools = await client.list_tools()
        resources = await client.list_resources()
        resource_templates= await client.list_resource_templates()
        prompts = await client.list_prompts()
        
        print("\n===============================Tools===============================\n")
        print("\n".join([tool.name for tool in tools]))
        print("\n===============================Resources===============================\n")
        print("\n".join([resource.name for resource in resources]))
        print("\n===============================Resource Templates===============================\n")
        print("\n".join([resource_template.name for resource_template in resource_templates]))
        print("\n===============================Prompts===============================\n")
        print("\n".join([prompt.name for prompt in prompts]))

        
        # Call tools
        try:
            result = await client.call_tool("list_contacts_api_contacts_get")
            print("\n===============================Read Users Tool Result===============================\n")
            print(result.content[0].text)

            result = await client.call_tool("create_contact_api_contacts_post", {"name": "John Doe", "email": "john.doe@example.com"})
            print("\n===============================Create Contact Tool Result===============================\n")
            print(result.content[0].text)

            result = await client.call_tool("get_contact_api_contacts", {"contact_id": 1})
            print("\n===============================Read Contact Tool Result===============================\n")
            print(result.content[0].text)

            result = await client.call_tool("update_contact_api_contacts", {"contact_id": 1, "name": "Sam Smith", "email": "sam.smith@example.com"})
            print("\n===============================Update Contact Tool Result===============================\n")
            print(result.content[0].text)

            result = await client.call_tool("delete_contact_api_contacts", {"contact_id": 1})
            print("\n===============================Delete Contact Tool Result===============================\n")
            print(result.content[0].text)

        except Exception as e:
            print("\n===============================Tool Error===============================\n")
            print(e)


if __name__ == "__main__":
    import asyncio
    asyncio.run(call_mcp())