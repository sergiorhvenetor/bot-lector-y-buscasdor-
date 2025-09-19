import io
from typing import Optional

from langchain_community.vectorstores import FAISS
from langchain_cohere import CohereEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from pypdf import PdfReader

from app.config.model import cohere as cohere_chat_model


class RAGHandler:
    """
    Handles the logic for the Retrieval-Augmented Generation (RAG) system.
    This class manages a FAISS vector store in memory.
    """
    def __init__(self):
        self.vector_store: Optional[FAISS] = None
        # Using a Cohere model for embeddings. Make sure the API key is set in the environment.
        self.embeddings = CohereEmbeddings(model="embed-english-light-v3.0")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.prompt_template = ChatPromptTemplate.from_template(
            "Answer the user's question based only on the following context:\n\n"
            "{context}\n\n"
            "Question: {question}"
        )
        self.chat_model = cohere_chat_model

    def process_pdf(self, pdf_bytes: bytes):
        """
        Processes a PDF file from bytes, creates a vector store, and stores it in memory.
        """
        try:
            pdf_file = io.BytesIO(pdf_bytes)
            reader = PdfReader(pdf_file)
            text = "".join(page.extract_text() for page in reader.pages if page.extract_text())

            if not text:
                raise ValueError("Could not extract any text from the provided PDF.")

            documents = self.text_splitter.split_text(text)

            # Create a new vector store from the document chunks
            self.vector_store = FAISS.from_texts(texts=documents, embedding=self.embeddings)
            print("PDF processed successfully and vector store created.")

        except Exception as e:
            # Log the exception for debugging
            print(f"An error occurred during PDF processing: {e}")
            # Re-raise or handle as appropriate
            raise ValueError(f"Failed to process PDF. Error: {e}")


    def answer_question(self, question: str) -> str:
        """
        Answers a question based on the content of the processed PDF.
        """
        if not self.vector_store:
            return "No PDF has been processed yet. Please upload a PDF document first."

        try:
            retriever = self.vector_store.as_retriever()

            # Retrieve relevant documents
            relevant_docs = retriever.invoke(question)

            # Format the context from the documents
            context = "\n\n".join([doc.page_content for doc in relevant_docs])

            # Create the chain using LangChain Expression Language (LCEL)
            rag_chain = (
                self.prompt_template | self.chat_model
            )

            # Invoke the chain with the context and question
            response = rag_chain.invoke({"context": context, "question": question})

            return response.content
        except Exception as e:
            print(f"An error occurred during question answering: {e}")
            return f"An error occurred while trying to answer the question. Error: {e}"

# The handler will be instantiated on application startup in main.py
