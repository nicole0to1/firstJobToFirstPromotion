# mcp_client.py
import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import traceback

def setup_env():
    global venv_python
    venv_python = os.path.join(os.getcwd(), 'venv_mcp', 'bin', 'python3')
    if not os.path.exists(venv_python):
        print(f"Virtual environment Python not found at: {venv_python}")
        return

async def list_mcp_prompts():
    print("Listing MCP Server Prompts...")

    # Configure the server parameters
    server_params = StdioServerParameters(
        command=venv_python,
        args=['mcp_server.py']
    )

    try:
        # Connect to the server using stdio_client
        print("Client attempting to connect to server...")
        async with stdio_client(server_params) as streams:
            # Create client session
           # Create the client session with the streams
            async with ClientSession(*streams) as session:
                # Initialize the session
                await session.initialize()
            
                # List available prompts
                prompts_result = await session.list_prompts()
                # Extract tool names from the result
                prompts = [prompt.name+":"+prompt.description for prompt in prompts_result.prompts] if hasattr(prompts_result, 'prompts') else []
                print(f"Available prompts: {prompts}")

                # List available tools
                tools_result = await session.list_tools()
                # Extract tool names from the result
                tools = [tool.name for tool in tools_result.tools] if hasattr(tools_result, 'tools') else []
                print(f"Available tools: {tools}")

    except Exception as e:
        print(f"An error occurred listing prompts in the client: {e}")
        traceback.print_exc()

async def run_mcp_client(state: str):
    print("Starting MCP Echo Client...")

    # Configure the server parameters
    server_params = StdioServerParameters(
        command=venv_python,
        args=['mcp_server.py']
    )

    try:
        # Connect to the server using stdio_client
        print("Client attempting to connect to server...")
        async with stdio_client(server_params) as streams:
            # Create client session
           # Create the client session with the streams
            async with ClientSession(*streams) as session:
                # Initialize the session
                await session.initialize()

                result = await session.call_tool("get_weather_alerts", {"state": state})
                print("Tool 'get_weather_alerts' returned: ")
                print(result.content[0].text)

                prompt_result = await session.get_prompt("ewa", {"location": state})
                print("Prompt 'ewa' returned: ")
                print(prompt_result.description)
                print(prompt_result.messages[0].content.text)
            
    except Exception as e:
        print(f"An error occurred in the client: {e}")
        traceback.print_exc()

    print("Client finished.")

if __name__ == "__main__":
    # Ensure mcp_server.py exists in the same directory
    if not os.path.exists('mcp_server.py'):
        print("Error: 'mcp_server.py' not found in the current directory.")
        print("Please create 'mcp_server.py' as described above.")
        exit(1)
    print("Welcome to the Weather Alert Shell! Ask weather alerts by prividing state i.e. 'CA'. \nType 'exit' or 'quit' to leave.")
    setup_env()
    asyncio.run(list_mcp_prompts())
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        asyncio.run(run_mcp_client(user_input))