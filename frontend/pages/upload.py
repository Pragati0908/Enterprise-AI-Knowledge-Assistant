import streamlit as st

from api_client import upload_file


st.title("Upload Documents")

uploaded_file = st.file_uploader(

    "Choose file",

    type=["pdf", "docx", "txt"]
)

if uploaded_file:

    result = upload_file(

        uploaded_file
    )

    st.success(

        result
    )