import streamlit as st
from utils.api import upload_pdfs_api

def render_uploader():
    st.header("Upload HR documents (.PDFs)")
    uploaded_files = st.file_uploader("Upload multiple PDFs", type="pdf", accept_multiple_files=True)
    if st.button("Upload to DB"):
        if uploaded_files:
            with st.spinner("Uploading and processing..."):
                response = upload_pdfs_api(uploaded_files)
                if response.status_code == 200:
                    st.success("Uploaded successfully")
                else:
                    st.error(f"Error: {response.text}")
        else:
            st.warning("Please select at least one PDF file first.")

