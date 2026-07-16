"""
mcp_server.py

Utility functions (MCP Tools)
"""

import os
import platform
from datetime import datetime

from config import DATA_FOLDER


class MCPServer:

    @staticmethod
    def current_time():
        """
        Return current system time.
        """
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    @staticmethod
    def list_documents():
        """
        Return uploaded PDF files.
        """

        if not os.path.exists(DATA_FOLDER):
            return []

        return [
            file
            for file in os.listdir(DATA_FOLDER)
            if file.endswith(".pdf")
        ]

    @staticmethod
    def search_document(keyword):
        """
        Search uploaded document.
        """

        keyword = keyword.lower()

        return [
            file
            for file in MCPServer.list_documents()
            if keyword in file.lower()
        ]

    @staticmethod
    def document_count():
        """
        Total uploaded documents.
        """
        return len(MCPServer.list_documents())

    @staticmethod
    def system_info():
        """
        Basic system information.
        """

        return {
            "Operating System": platform.system(),
            "Python Version": platform.python_version()
        }