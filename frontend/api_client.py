import requests


# ==========================================================
# Configuration
# ==========================================================

BASE_URL = "http://127.0.0.1:8000"

TIMEOUT = 120


# ==========================================================
# Health API
# ==========================================================

def get_health():

    response = requests.get(

        f"{BASE_URL}/health",

        timeout=TIMEOUT

    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Upload API
# ==========================================================

def upload_file(file):

    files = {

        "file": file

    }

    response = requests.post(

        f"{BASE_URL}/upload",

        files=files,

        timeout=TIMEOUT

    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Documents API
# ==========================================================

def get_documents():

    response = requests.get(

        f"{BASE_URL}/documents",

        timeout=TIMEOUT

    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# OCR Extract API
# ==========================================================

def extract_ocr(file):

    files = {

        "file": file

    }

    response = requests.post(

        f"{BASE_URL}/ocr/extract",

        files=files,

        timeout=TIMEOUT

    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# OCR Chunk API
# ==========================================================

def generate_chunks(file):

    files = {

        "file": file

    }

    response = requests.post(

        f"{BASE_URL}/ocr/chunk",

        files=files,

        timeout=TIMEOUT

    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Embedding Status API
# ==========================================================

def get_embedding_status():

    response = requests.get(

        f"{BASE_URL}/embeddings/status",

        timeout=TIMEOUT

    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Create Embeddings API
# ==========================================================

def create_document_embeddings(filename):

    response = requests.post(

        f"{BASE_URL}/embeddings/create",

        json={

            "filename": filename

        },

        timeout=TIMEOUT

    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Embedding Search API
# ==========================================================

def search_embeddings(

    query,

    top_k=5

):

    response = requests.post(

        f"{BASE_URL}/embeddings/search",

        json={

            "query": query,

            "top_k": top_k

        },

        timeout=TIMEOUT

    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Multi-document Search API
# ==========================================================

def search_documents(

    query,

    top_k=5

):

    response = requests.post(

        f"{BASE_URL}/search",

        json={

            "query": query,

            "top_k": top_k

        },

        timeout=TIMEOUT

    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Chat Status API
# ==========================================================

def get_chat_status():

    """
    GET /chat/status
    """

    response = requests.get(

        f"{BASE_URL}/chat/status",

        timeout=TIMEOUT

    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Ask Question API
# ==========================================================

def ask_question(

    question,

    top_k=3

):

    """
    POST /chat/ask
    """

    payload = {

        "question": question,

        "top_k": top_k

    }

    response = requests.post(

        f"{BASE_URL}/chat/ask",

        json=payload,

        timeout=TIMEOUT

    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Document Summary API
# ==========================================================

def summarize_document(

    context

):

    """
    POST /chat/summary
    """

    payload = {

        "context": context

    }

    response = requests.post(

        f"{BASE_URL}/chat/summary",

        json=payload,

        timeout=TIMEOUT

    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Generic Prompt API (Optional)
# ==========================================================

def generate_response(

    prompt

):

    """
    POST /chat/generate
    """

    response = requests.post(

        f"{BASE_URL}/chat/generate",

        params={

            "prompt": prompt

        },

        timeout=TIMEOUT

    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Information Extraction API
# ==========================================================

def extract_information(
    text,
    extraction_type="all"
):

    response = requests.post(

        f"{BASE_URL}/extraction",

        json={

            "text": text,

            "extraction_type":
                extraction_type

        },

        timeout=TIMEOUT

    )

    response.raise_for_status()

    return response.json()