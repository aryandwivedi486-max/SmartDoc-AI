# SmartDoc AI

[![Open Live App](https://img.shields.io/badge/🚀_Open-Live_App-FF4B4B?style=for-the-badge)](https://smartdoc-ai-udixf9d2cfhzg8fxkwzjua.streamlit.app/)

> **Try SmartDoc AI:** [Launch the deployed application](https://smartdoc-ai-udixf9d2cfhzg8fxkwzjua.streamlit.app/) — upload a PDF and ask questions about its content.

A Retrieval-Augmented Generation (RAG) application that lets users ask questions about PDF documents. It uses Gemini for embeddings and answer generation, FAISS for similarity search, and Streamlit for the web interface.

## Features

- Upload one or more PDF documents.
- Extract text while preserving page numbers.
- Split text into overlapping chunks.
- Convert text chunks into embeddings using Gemini.
- Find relevant chunks using FAISS similarity search.
- Generate answers using Gemini with retrieved document context.
- Display source filenames, page numbers, similarity scores, and retrieved text.
- Adjust the number of retrieved chunks and similarity threshold.

## How It Works

1. Upload PDF documents.
2. Extract text page by page.
3. Split the text into smaller overlapping chunks.
4. Convert each chunk into an embedding using Gemini.
5. Store the vectors in a FAISS index.
6. Convert the user's question into an embedding.
7. Retrieve relevant chunks from FAISS.
8. Send the question and retrieved context to Gemini.
9. Display the answer and source pages.

## Tech Stack

- Python
- Streamlit
- Google Gemini API (google-genai)
- FAISS
- NumPy
- PyPDF
- python-dotenv

## Project Structure

    SmartDoc-AI/
    ├── app.py
    ├── src/
    │   ├── __init__.py
    │   └── rag.py
    ├── requirements.txt
    ├── .gitignore
    └── README.md

## Run Locally

1. Clone this repository:
   
       git clone https://github.com/aryandwivedi486-max/SmartDoc-AI.git
       cd SmartDoc-AI

2. Create and activate a virtual environment:

       python -m venv .venv

   On Windows:

       .venv\Scripts\activate

3. Install dependencies:

       pip install -r requirements.txt

4. Create a .env file in the project root with these settings:

       GEMINI_API_KEY=your_gemini_api_key
       GEMINI_EMBEDDING_MODEL=gemini-embedding-001
       GEMINI_GENERATION_MODEL=your_working_gemini_model

5. Run the app:

       streamlit run app.py

## Deploy on Streamlit Community Cloud

1. Sign in to Streamlit Community Cloud using GitHub.
2. Create a new app and select this repository.
3. Set the main file path to app.py.
4. Add these values in the app's Secrets settings:

       GEMINI_API_KEY = "your_gemini_api_key"
       GEMINI_EMBEDDING_MODEL = "gemini-embedding-001"
       GEMINI_GENERATION_MODEL = "your_working_gemini_model"

5. Deploy the app.

Never commit your API key or local .env file to GitHub.

## Limitations

- Scanned PDFs need OCR; this version extracts selectable text.
- The FAISS index is stored in memory and is rebuilt when PDFs are processed.
- Gemini API access, internet connectivity, quotas, and model availability affect usage.
- Retrieval quality depends on chunking, embeddings, and the similarity threshold.
- This is an educational prototype, not a production document-management system.

## Future Improvements

- Add OCR support for scanned PDFs.
- Support more document formats.
- Save document indexes between sessions.
- Add user authentication and document management.
- Improve retrieval with reranking and hybrid search.

## Author

Aryan Dwivedi  
B.Tech Computer Science (Data Science)
