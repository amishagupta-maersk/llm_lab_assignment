import os

from dotenv import load_dotenv
import uvicorn
from fastapi_mcp import FastApiMCP
from mcpAgents.McpResumeChecker import app

# Load environment variables
load_dotenv()

# Initialize and mount FastAPI MCP server
mcp_server = FastApiMCP(app, include_operations=["resume_check"])
mcp_server.mount()

# Start the FastAPI application using Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
