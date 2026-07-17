import os

from utils.constants import (
    SUPPORTED_EXTENSIONS,
    MAX_FILE_SIZE,
)


def validate_pdf(uploaded_file):
    """
    Validate uploaded PDF.
    """

    if uploaded_file is None:
        return False, "No file uploaded."

    extension = os.path.splitext(uploaded_file.name)[1].lower()

    if extension not in SUPPORTED_EXTENSIONS:
        return False, "Only PDF files are allowed."

    if uploaded_file.size > MAX_FILE_SIZE:
        return False, "File size exceeds 20 MB."

    return True, "Valid PDF."