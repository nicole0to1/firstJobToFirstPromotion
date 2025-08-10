# MCP Weather Alert Server

A Multi-Agent Communication Protocol (MCP) server that provides real-time weather alerts and interactive weather analysis capabilities. This server integrates with the National Weather Service API to deliver current weather advisories and warnings for any US state.

## 🚀 Features

- **Real-time Weather Alerts**: Get current weather alerts, warnings, and advisories for any US state
- **Interactive Weather Analysis**: AI-powered prompts that analyze weather data and provide actionable recommendations
- **MCP Protocol**: Built using the modern MCP (Multi-Agent Communication Protocol) framework
- **Stdio Transport**: Simple local development setup using standard input/output communication
- **Async Operations**: Built with Python's asyncio for efficient concurrent operations

## 🛠️ Prerequisites

- Python 3.8 or higher
- Virtual environment support
- Internet connection (for weather API access)

## 📦 Installation

### 1. Clone or Download the Project

```bash
# If you have the files locally, navigate to the project directory
cd /path/to/MCPExample
```

### 2. Set Up Virtual Environment

```bash
# Create a virtual environment
python3 -m venv venv_mcp

# Activate the virtual environment
# On macOS/Linux:
source venv_mcp/bin/activate

# On Windows:
# venv_mcp\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install required packages
pip install mcp httpx
```

## 🚀 Usage

### Starting the Server

The MCP server runs in the background and communicates with clients via stdio transport.

```bash
# Activate virtual environment
source venv_mcp/bin/activate

# Start the server
python3 mcp_server.py
```

**Note**: The server will start and wait for client connections. You can stop it with `Ctrl+C`.

### Using the Client

The project includes an interactive client that demonstrates the server's capabilities:

```bash
# Activate virtual environment
source venv_mcp/bin/activate

# Run the interactive client
python3 mcp_client.py
```

The client provides an interactive shell where you can:
- Get weather alerts for any US state (e.g., "CA" for California)
- View available MCP tools and prompts
- Exit with "exit" or "quit"

### Example Client Session

```
Welcome to the Weather Alert Shell! Ask weather alerts by providing state i.e. 'CA'. 
Type 'exit' or 'quit' to leave.

Available prompts: ['ewa:Generates a prompt to understand the alerts and prepare for extreme weather for a specific location.']
Available tools: ['get_weather_alerts']

You: CA
Starting MCP Echo Client...
Client attempting to connect to server...
Tool 'get_weather_alerts' returned: 
Event: Heat Advisory
Area: West Side Mountains north of 198; Los Banos - Dos Palos...
Severity: Moderate
Description: * WHAT...High temperatures up to 105 expected...
Instructions: Drink plenty of fluids, stay in an air-conditioned room...

Prompt 'ewa' returned: 
Generates a prompt to understand the alerts and prepare for extreme weather for a specific location.
You are an expert weather analyst.
Please use the 'get_weather_alerts' tool to find the weather for **CA**.
Based on the weather data, provide a detailed analysis including:
- The current situation.
- Recommendations for what to do.

Client finished.
You: exit
Goodbye!
```

## 🔧 Available Tools

### 1. `get_weather_alerts`

**Purpose**: Retrieves current weather alerts for a specified US state

**Parameters**:
- `state` (str): Two-letter US state code (e.g., "CA", "NY", "TX")

**Returns**: Formatted weather alert information including:
- Event type (Heat Advisory, Extreme Heat Warning, etc.)
- Affected areas
- Severity level
- Description of conditions
- Safety instructions

**Example**:
```python
result = await session.call_tool("get_weather_alerts", {"state": "CA"})
```

### 2. `ewa` (Extreme Weather Analysis)

**Purpose**: Generates AI prompts for analyzing weather data and providing recommendations

**Parameters**:
- `location` (str): The location to analyze weather for

**Returns**: Structured prompt for LLM analysis including:
- Current weather situation assessment
- Actionable recommendations
- Safety guidelines

**Example**:
```python
prompt_result = await session.get_prompt("ewa", {"location": "CA"})
```

## 🏗️ Architecture

### Server Components

- **FastMCP Server**: Built using the `mcp.server.fastmcp` framework
- **Weather API Integration**: Uses `httpx` for HTTP requests to the National Weather Service API
- **Tool Registration**: Tools are registered using the `@mcp.tool()` decorator
- **Prompt Registration**: Prompts are registered using the `@mcp.prompt()` decorator

### Client Components

- **MCP Client**: Uses `mcp.client.stdio` for stdio transport
- **Session Management**: Manages client-server communication sessions
- **Interactive Shell**: Provides user-friendly interface for testing server capabilities

### Communication Flow

1. Client launches server as subprocess
2. Client establishes MCP session with server
3. Client discovers available tools and prompts
4. Client calls tools or retrieves prompts as needed
5. Server processes requests and returns results
6. Client displays results to user

## 🌐 API Integration

The server integrates with the **National Weather Service (NWS) API**:

- **Base URL**: `https://api.weather.gov`
- **Endpoint**: `/alerts/active/area/{state}`
- **Format**: GeoJSON
- **Rate Limits**: NWS API has generous rate limits for public use
- **Data**: Real-time weather alerts, warnings, and advisories

## 🔍 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Ensure virtual environment is activated and dependencies are installed
2. **Connection Issues**: Check that the server is running and accessible
3. **API Errors**: Verify internet connection and NWS API availability

### Debug Mode

Enable detailed error logging by checking the server output and client error messages.

## 📚 MCP Protocol Details

This project demonstrates the **Multi-Agent Communication Protocol (MCP)**:

- **Transport**: Stdio (standard input/output) for local development
- **Tools**: Server exposes callable functions to clients
- **Prompts**: Server provides structured prompts for AI analysis
- **Session Management**: Clients establish and manage communication sessions

## 🤝 Contributing

To extend the server with new capabilities:

1. **Add New Tools**: Use `@mcp.tool()` decorator
2. **Add New Prompts**: Use `@mcp.prompt()` decorator
3. **Integrate New APIs**: Follow the pattern in `make_nws_request()`
4. **Update Client**: Modify client code to use new capabilities

## 📄 License

This project is provided as-is for educational and development purposes.

## 🙏 Acknowledgments

- **National Weather Service**: For providing the weather alerts API
- **MCP Framework**: For the Multi-Agent Communication Protocol implementation
- **Python Community**: For the excellent async libraries and tools

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your Python environment and dependencies
3. Ensure the server is running before using the client
4. Check the National Weather Service API status

---

**Happy Weather Monitoring! 🌤️**
