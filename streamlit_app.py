import streamlit as st
from dotenv import load_dotenv
from app.rag_handler import RAGHandler

# Load environment variables
load_dotenv()

# --- Streamlit Application ---

# Set the title for the Streamlit app
st.title("Interactúa con tus documentos PDF")
st.markdown("""
Esta aplicación te permite cargar un documento PDF y hacerle preguntas.
El sistema utilizará un modelo de lenguaje para encontrar las respuestas en el texto.
""")

# Initialize or get the RAG handler from the session state
if 'rag_handler' not in st.session_state:
    st.session_state.rag_handler = RAGHandler()

# File uploader for PDF
uploaded_file = st.file_uploader("Carga tu documento PDF", type="pdf")

if uploaded_file is not None:
    # Process the PDF
    with st.spinner('Procesando el PDF...'):
        try:
            pdf_bytes = uploaded_file.getvalue()
            st.session_state.rag_handler.process_pdf(pdf_bytes)
            st.success(f"¡El archivo '{uploaded_file.name}' ha sido procesado con éxito!")
            st.info("Ahora puedes hacer preguntas sobre el contenido del documento.")
        except Exception as e:
            st.error(f"Error al procesar el PDF: {e}")

# Only show the query input if a PDF has been processed
if st.session_state.rag_handler.vector_store is not None:
    st.markdown("---")
    st.header("Haz una pregunta")

    # Text input for the user's question
    question = st.text_input("Escribe tu pregunta aquí:")

    if st.button("Obtener respuesta"):
        if question:
            with st.spinner("Buscando la respuesta..."):
                try:
                    answer = st.session_state.rag_handler.answer_question(question)
                    st.success("Respuesta:")
                    st.write(answer)
                except Exception as e:
                    st.error(f"Error al obtener la respuesta: {e}")
        else:
            st.warning("Por favor, escribe una pregunta.")
else:
    st.info("Por favor, carga un documento PDF para comenzar.")