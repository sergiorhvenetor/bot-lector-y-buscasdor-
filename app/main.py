from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from app.rag_handler import RAGHandler

# Load environment variables
load_dotenv()

# --- Simplified Approach ---
# Instantiate the RAG handler directly at the global scope.
# This relies on the server running with a single worker process to maintain state.
rag_handler_instance = RAGHandler()

app = FastAPI(
    title="Servicio RAG con PDF",
    description="API para cargar un PDF y hacerle preguntas.",
)

# Pydantic model for the query request body
class QueryRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    """A simple endpoint to confirm the server is running."""
    return {"message": "¡Ah del barco! El servicio RAG está en funcionamiento."}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Endpoint to upload a PDF file.
    The file is processed and stored in the in-memory vector store.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")

    try:
        pdf_bytes = await file.read()
        rag_handler_instance.process_pdf(pdf_bytes)
        return {"message": f"File '{file.filename}' processed successfully. You can now ask questions."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {e}")

@app.post("/query")
async def query(request: QueryRequest):
    """
    Endpoint to ask a question about the uploaded PDF.
    """
    try:
        answer = rag_handler_instance.answer_question(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get an answer: {e}")
