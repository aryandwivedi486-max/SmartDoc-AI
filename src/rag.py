from io import BytesIO
import os
import re

import faiss
import numpy as np
import streamlit as st

from google import genai
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()


def get_setting(name, default=None):
    try:
        return st.secrets[name]
    except Exception:
        return os.getenv(name, default)


def get_client():
    api_key = get_setting("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing. Add it to .env or Streamlit secrets.")
    return genai.Client(api_key=api_key)


def extract_pdf_pages(uploaded_file):
    pdf = PdfReader(BytesIO(uploaded_file.getvalue()))
    pages = []

    for page_number, page in enumerate(pdf.pages, start=1):
        text = page.extract_text() or ""
        text = re.sub(r"\s+", " ", text).strip()

        if text:
            pages.append({
                "filename": uploaded_file.name,
                "page": page_number,
                "text": text
            })

    return pages


def split_into_chunks(text, chunk_size=900, overlap=150):
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start = end - overlap

    return chunks


def embed_text(text, client):
    model = get_setting("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")
    result = client.models.embed_content(model=model, contents=text)

    return np.array(
        result.embeddings[0].values,
        dtype="float32"
    )


def build_knowledge_base(uploaded_files):
    all_chunks = []
    client = get_client()

    for file in uploaded_files:
        pages = extract_pdf_pages(file)

        for page in pages:
            chunks = split_into_chunks(page["text"])

            for chunk in chunks:
                all_chunks.append({
                    "filename": page["filename"],
                    "page": page["page"],
                    "text": chunk
                })

    if not all_chunks:
        raise ValueError("No readable text found in PDFs. Scanned PDFs need OCR.")

    vectors = []
    for chunk in all_chunks:
        vectors.append(embed_text(chunk["text"], client))

    matrix = np.array(vectors, dtype="float32")
    faiss.normalize_L2(matrix)

    index = faiss.IndexFlatIP(matrix.shape[1])
    index.add(matrix)

    return {
        "index": index,
        "chunks": all_chunks,
        "document_count": len(uploaded_files)
    }


def answer_question(question, knowledge_base, top_k=3, threshold=0.30):
    client = get_client()

    query_vector = embed_text(question, client)
    query_vector = query_vector.reshape(1, -1)
    faiss.normalize_L2(query_vector)

    scores, indices = knowledge_base["index"].search(
        query_vector,
        min(top_k, len(knowledge_base["chunks"]))
    )

    relevant_chunks = []

    for score, index in zip(scores[0], indices[0]):
        if index < 0 or score < threshold:
            continue

        chunk = knowledge_base["chunks"][int(index)]
        relevant_chunks.append({
            **chunk,
            "score": float(score)
        })

    if not relevant_chunks:
        return {
            "answer": "I couldn't find this information in the uploaded PDFs.",
            "sources": []
        }

    context = ""
    for item in relevant_chunks:
        context += (
            f'Source: {item["filename"]}, Page: {item["page"]}\n'
            f'{item["text"]}\n\n'
        )

    prompt = f"""
You are SmartDoc AI.

Answer the question using ONLY the provided context.
Do not use outside knowledge or guess answers.
If the answer is not available in the context, say that
the information was not found in the uploaded documents.

CONTEXT:
{context}

QUESTION:
{question}
"""

    generation_model = get_setting("GEMINI_GENERATION_MODEL")
    if not generation_model:
        raise ValueError(
            "GEMINI_GENERATION_MODEL is missing. Add your working Gemini model name to .env or Streamlit secrets."
        )

    response = client.models.generate_content(
        model=generation_model,
        contents=prompt
    )

    sources = []
    for item in relevant_chunks:
        sources.append({
            "filename": item["filename"],
            "page": item["page"],
            "score": item["score"],
            "text": item["text"]
        })

    return {
        "answer": response.text or "No response generated.",
        "sources": sources
    }
