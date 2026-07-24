import requests

BASE_URL = "http://127.0.0.1:8000"


def get_health():

    response = requests.get(

        f"{BASE_URL}/health"

    )

    return response.json()


def upload_file(file):

    files = {

        "file": file

    }

    response = requests.post(

        f"{BASE_URL}/upload",

        files=files

    )

    return response.json()


def get_documents():

    response = requests.get(

        f"{BASE_URL}/documents"

    )

    return response.json()


def extract_ocr(file):

    files = {

        "file": file

    }

    response = requests.post(

        f"{BASE_URL}/ocr/extract",

        files=files

    )

    return response.json()


def generate_chunks(file):

    files = {

        "file": file

    }

    response = requests.post(

        f"{BASE_URL}/ocr/chunk",

        files=files

    )

    return response.json()