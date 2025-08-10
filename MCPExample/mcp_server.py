# mcp_server.py
import asyncio
import os
from mcp.server.fastmcp import FastMCP

from typing import Any
import httpx

# Initialize the FastMCP server with a name
# The name "echo_server" will be used by clients to identify this server
mcp = FastMCP("echo_server")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

@mcp.prompt()
def ewa(location: str) -> str:
    """
    Generates a prompt to understand the alerts and prepare for extreme weather for a specific location.
    Args:
        location (str): The location to analyze the weather for.
    Returns:
        str: A structured prompt for the LLM.
    """
    return f"""
    You are an expert weather analyst.
    Please use the 'get_weather_alerts' tool to find the weather for **{location}**.
    Based on the weather data, provide a detailed analysis including:
    - The current situation.
    - Recommendations for what to do.
    """

@mcp.tool()
async def get_weather_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)



async def main():
    print("Starting MCP Echo Server 1...")
    # Run the server over standard I/O (stdio)
    # This is suitable for local development and simple examples
    await mcp.run_stdio_async()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except asyncio.CancelledError:
        print("MCP Echo Server stopped.")
    except Exception as e:
        print(f"An error occurred in the server: {e}")