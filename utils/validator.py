"""
Validation utilities for uploaded PDF files.
"""

import os

from utils.constants import (
    SUPPORTED_EXTENSIONS,
    MAX_FILE_SIZE,
)


def validate_pdf(filename: str, file_size: int) -> tuple[bool, str]:
    """
    Validate an uploaded PDF by filename and size.

    Framework-agnostic on purpose: works whether the caller is FastAPI's
    UploadFile (which has .filename / needs os.path.getsize) or Streamlit's
    UploadedFile (which has .name / .size) — the caller passes plain values
    instead of the file object itself.

    Checks:
    1. Filename is present.
    2. File extension is supported.
    3. File size is within the allowed limit.

    Returns:
        (True, message) if valid
        (False, error_message) if invalid
    """

    # Empty filename
    if not filename:
        return False, "Invalid file."

    # Check extension
    extension = os.path.splitext(filename)[1].lower()

    if extension not in SUPPORTED_EXTENSIONS:
        return False, "Only PDF files are allowed."

    # Check file size
    if file_size > MAX_FILE_SIZE:
        max_size_mb = MAX_FILE_SIZE // (1024 * 1024)
        return False, f"File size exceeds {max_size_mb} MB."

    return True, "Valid PDF."
