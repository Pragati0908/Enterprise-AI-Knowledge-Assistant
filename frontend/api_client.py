import requests


BASE_URL = "http://127.0.0.1:8000"


# ==========================================================
# Health API
# ==========================================================

def get_health():

    response = requests.get(

        f"{BASE_URL}/health"

    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Upload API
# ==========================================================

def upload_file(

    file

):

    files = {

        "file": file

    }

    response = requests.post(

        f"{BASE_URL}/upload",

        files=files

    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Documents API
# ==========================================================

def get_documents():

    response = requests.get(

        f"{BASE_URL}/documents"

    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# OCR Extract API
# ==========================================================

def extract_ocr(

    file

):

    files = {

        "file": file

    }

    response = requests.post(

        f"{BASE_URL}/ocr/extract",

        files=files

    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# OCR Chunk API
# ==========================================================

def generate_chunks(

    file

):

    files = {

        "file": file

    }

    response = requests.post(

        f"{BASE_URL}/ocr/chunk",

        files=files

    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Embedding Status API
# ==========================================================

def get_embedding_status():

    response = requests.get(

        f"{BASE_URL}/embeddings/status"

    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Create Document Embeddings API
# ==========================================================

def create_document_embeddings(

    filename

):

    response = requests.post(

        f"{BASE_URL}/embeddings/create",

        json={

            "filename": filename

        }

    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Similarity Search API
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

        }

    )

    response.raise_for_status()

    return response.json()