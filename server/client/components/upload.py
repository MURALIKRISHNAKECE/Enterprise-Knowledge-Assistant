import streamlit as st
from utils.api import upload_pdfs_api


def render_uploader():
    uploaded_files = st.file_uploader(
        "Upload PDF documents",
        type="pdf",
        accept_multiple_files=True,
        help="Upload one or more PDF files to index them for querying"
    )

    if uploaded_files:
        st.markdown(f"""
        <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:8px;
             padding:0.5rem 0.8rem; margin:0.5rem 0; font-size:0.78rem; color:#166534;">
            ✅ {len(uploaded_files)} file(s) selected
        </div>
        """, unsafe_allow_html=True)

    if st.button("⬆ Upload to Knowledge Base"):
        if uploaded_files:
            with st.spinner("Indexing documents..."):
                response = upload_pdfs_api(uploaded_files)
                if response.status_code == 200:
                    st.success("✅ Documents indexed successfully")
                else:
                    st.error(f"Upload failed: {response.text}")
        else:
            st.warning("Please select at least one PDF file first.")