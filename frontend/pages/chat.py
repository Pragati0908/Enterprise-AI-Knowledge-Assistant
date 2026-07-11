import streamlit as st

st.title("AI Chat")

question = st.text_input(

    "Ask a question"
)

if st.button("Send"):

    st.write(

        "Chat integration starts Next Week"
    )