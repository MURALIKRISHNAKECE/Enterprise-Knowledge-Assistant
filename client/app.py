import streamlit as st
from components.upload import render_uploader
from components.history_download import render_history_download
from components.chatUI import render_chat

st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: system-ui, -apple-system, sans-serif !important;
}
.stApp {
    background-color: #f8fafc !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #f8fafc !important;
}
[data-testid="stHeader"] {
    background-color: #ffffff !important;
    border-bottom: 1px solid #e2e8f0 !important;
}
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
}
[data-testid="stSidebar"] * {
    color: #0f172a !important;
}
[data-testid="stSidebar"] .stButton > button {
    background-color: #3b82f6 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    width: 100% !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #2563eb !important;
}
.block-container {
    padding: 1.5rem 2rem 1rem 2rem !important;
    background-color: #f8fafc !important;
}
[data-testid="stChatInput"] textarea {
    background-color: #ffffff !important;
    color: #0f172a !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
}
[data-testid="stChatMessageContent"] {
    background-color: #ffffff !important;
    color: #0f172a !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
}
div[data-testid="metric-container"] {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    color: #0f172a !important;
}
.stExpander {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
}
.stFileUploader {
    background-color: #f8fafc !important;
    border: 1.5px dashed #cbd5e1 !important;
    border-radius: 8px !important;
}
p, h1, h2, h3, label, span {
    color: #0f172a !important;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="padding:0.5rem 0 1rem 0;border-bottom:1px solid #e2e8f0;margin-bottom:1rem;">
        <p style="font-size:1rem;font-weight:600;color:#0f172a;margin:0;">🧠 Enterprise AI</p>
        <p style="font-size:0.75rem;color:#64748b;margin:0;">Knowledge Assistant</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p style="font-size:0.7rem;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.4rem;">📄 Documents</p>', unsafe_allow_html=True)
    render_uploader()

    st.divider()

    st.markdown('<p style="font-size:0.7rem;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.4rem;">💾 Session</p>', unsafe_allow_html=True)
    render_history_download()

    st.markdown("""
    <div style="margin-top:2rem;padding:0.6rem;background:#f8fafc;border:1px solid #e2e8f0;
         border-radius:8px;text-align:center;">
        <p style="font-size:0.68rem;color:#94a3b8;margin:0;">
            Groq · Pinecone · LangChain · FastEmbed
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="background:#ffffff;border:1px solid #e2e8f0;border-radius:10px;
     padding:0.9rem 1.2rem;margin-bottom:1rem;display:flex;align-items:center;gap:10px;">
    <div style="width:40px;height:40px;background:#eff6ff;border-radius:8px;
         display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0;">🧠</div>
    <div>
        <p style="margin:0;font-size:1rem;font-weight:600;color:#0f172a;">
            Enterprise Knowledge Assistant
        </p>
        <p style="margin:0;font-size:0.75rem;color:#64748b;">
            Upload documents and ask questions — answers grounded in your content
        </p>
    </div>
    <div style="margin-left:auto;background:#f0fdf4;border:1px solid #86efac;
         border-radius:6px;padding:0.25rem 0.6rem;display:flex;align-items:center;gap:5px;">
        <span style="width:6px;height:6px;background:#22c55e;border-radius:50%;display:inline-block;"></span>
        <span style="font-size:0.7rem;color:#15803d;font-weight:500;">Online</span>
    </div>
</div>
""", unsafe_allow_html=True)

render_chat()