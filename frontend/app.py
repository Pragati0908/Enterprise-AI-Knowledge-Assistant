import streamlit as st

from components.sidebar import render_sidebar

from api_client import get_health, upload_file

st.set_page_config(
    page_title="Enterprise AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)

def load_css():

    with open(

        "assets/styles.css"

    ) as f:

        st.markdown(

            f"<style>{f.read()}</style>",

            unsafe_allow_html=True
        )


load_css()


page = render_sidebar()

st.title("🤖 Enterprise AI Knowledge Assistant")

st.subheader(page)

if page == "Home":

    st.write("Dashboard")

    try:

        health = get_health()

        st.success("Backend connected successfully.")

        st.json(health)

    except Exception:

        st.error(
            "Cannot connect to FastAPI backend. "
            "Make sure the backend server is running."
        )

elif page == "Upload Documents":

    st.title("📂 Upload Documents")

    uploaded_file = st.file_uploader(

        "Choose a file",

        type=[
            "pdf",
            "docx",
            "pptx",
            "xlsx"
        ]
    )

    if uploaded_file:

        st.info(

            f"Selected file: {uploaded_file.name}"

        )

        if st.button("Upload"):

            try:

                result = upload_file(
                    uploaded_file
                )

                st.success(

                    "File uploaded successfully."

                )

                st.json(result)

            except Exception:

                st.error(

                    "Upload failed. "
                    "Make sure the FastAPI backend is running."

                )

elif page == "Documents":

    st.write("Document list")

elif page == "Chat":

    st.write("AI Chat")

elif page == "Settings":

    st.write("System settings")

