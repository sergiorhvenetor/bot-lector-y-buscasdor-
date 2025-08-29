from langchain.tools import tool
from pypdf import PdfReader
from app.config.model import cohere
from langchain_core.messages import HumanMessage
import os

@tool
def summarize_pdf(file_path: str) -> str:
    """
    Summarizes the content of a PDF file.

    Args:
        file_path: The path to the PDF file.

    Returns:
        A summary of the PDF content.
    """
    if not os.path.exists(file_path):
        return "Error: File not found."

    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        if not text:
            return "Error: Could not extract text from the PDF."

        prompt = f"Please summarize the following text extracted from a PDF:\n\n{text}"

        message = HumanMessage(content=prompt)
        response = cohere.invoke([message])

        return response.content
    except Exception as e:
        return f"An error occurred while processing the PDF: {e}"
