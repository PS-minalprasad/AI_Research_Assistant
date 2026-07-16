from mcp.server.fastmcp import FastMCP
import os
import platform
from datetime import datetime

DATA_FOLDER = "data"

mcp = FastMCP("AI Research Assistant")


@mcp.tool()
def current_time() -> str:
    """Return current system time."""
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


@mcp.tool()
def list_documents() -> list[str]:
    """Return uploaded PDF files."""

    if not os.path.exists(DATA_FOLDER):
        return []

    return [
        file
        for file in os.listdir(DATA_FOLDER)
        if file.endswith(".pdf")
    ]


@mcp.tool()
def document_count() -> int:
    """Return total uploaded documents."""
    return len(list_documents())


@mcp.tool()
def system_info() -> dict:
    """Return system information."""

    return {
        "os": platform.system(),
        "python": platform.python_version()
    }


if __name__ == "__main__":
    mcp.run()