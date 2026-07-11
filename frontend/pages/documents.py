import streamlit as st

from api_client import get_documents


st.title("Documents")

documents = get_documents()

st.json(documents)