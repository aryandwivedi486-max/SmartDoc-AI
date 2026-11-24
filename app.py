import streamlit as st
from src.rag import build_knowledge_base, answer_question

st.set_page_config(page_title="SmartDoc AI", page_icon="📄", layout="wide")

st.title("📄 SmartDoc AI")
st.caption("Ask questions about your PDF documents using RAG.")

with st.sidebar:
    st.header("Settings")
    top_k = st.slider("Relevant chunks to retrieve", 1, 5, 3)
    threshold = st.slider("Minimum similarity score", 0.0, 1.0, 0.30, 0.05)
    st.info("Upload PDFs and then ask questions.")

uploaded_files = st.file_uploader(
    "Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

if "knowledge_base" not in st.session_state:
    st.session_state.knowledge_base = None

if "chat" not in st.session_state:
    st.session_state.chat = []

if st.button("Process PDFs", disabled=not uploaded_files):
    try:
        with st.spinner("Processing PDFs..."):
            st.session_state.knowledge_base = build_knowledge_base(uploaded_files)
            st.session_state.chat = []
        st.success("PDFs processed successfully!")
    except Exception as e:
        st.error(f"Error: {e}")

if st.session_state.knowledge_base:
    st.divider()
    st.subheader("Ask Your Documents")

    for message in st.session_state.chat:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask something about your PDFs...")

    if question:
        st.session_state.chat.append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Finding the answer..."):
                try:
                    result = answer_question(
                        question,
                        st.session_state.knowledge_base,
                        top_k=top_k,
                        threshold=threshold
                    )

                    st.markdown(result["answer"])

                    if result["sources"]:
                        st.markdown("**Sources:**")
                        for source in result["sources"]:
                            st.write(
                                f'{source["filename"]} - Page {source["page"]} '
                                f'(similarity: {source["score"]:.2f})'
                            )
                            with st.expander("View Retrieved Text"):
                                st.write(source["text"])

                    st.session_state.chat.append({
                        "role": "assistant",
                        "content": result["answer"]
                    })
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.warning("Upload PDFs and click Process PDFs to begin.")

st.caption("SmartDoc AI | Python | Gemini | FAISS | Streamlit")
