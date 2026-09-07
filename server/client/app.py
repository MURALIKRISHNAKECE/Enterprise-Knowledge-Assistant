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
html, body, [class*="css"] { font-family: system-ui, -apple-system, sans-serif !important; }
section[data-testid="stSidebar"] { background: #f1f5f9 !important; border-right: 1px solid #e2e8f0 !important; }
.block-container { padding: 1.5rem 2rem 1rem 2rem !important; }
div[data-testid="metric-container"] { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; }
.stExpander { border: 1px solid #e2e8f0 !important; border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="margin-bottom:1.2rem;">
        <p style="font-size:1rem;font-weight:600;color:#0f172a;margin:0;">🧠 Enterprise AI</p>
        <p style="font-size:0.75rem;color:#64748b;margin:0;">Knowledge Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown('<p style="font-size:0.7rem;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.4rem;">Documents</p>', unsafe_allow_html=True)
    render_uploader()
    st.divider()
    st.markdown('<p style="font-size:0.7rem;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.4rem;">Session</p>', unsafe_allow_html=True)
    render_history_download()
    st.markdown("""
    <div style="margin-top:2rem;font-size:0.68rem;color:#94a3b8;text-align:center;">
        Groq · Pinecone · LangChain · FastEmbed
    </div>
    """, unsafe_allow_html=True)

col1, col2 = st.columns([6, 1])
with col1:
    st.markdown("""
    <div style="background:white;border:1px solid #e2e8f0;border-radius:10px;
         padding:0.9rem 1.2rem;margin-bottom:1rem;display:flex;align-items:center;gap:10px;">
        <div>
            <p style="margin:0;font-size:1rem;font-weight:600;color:#0f172a;">Enterprise Knowledge Assistant</p>
            <p style="margin:0;font-size:0.75rem;color:#64748b;">Ask questions about your documents</p>
        </div>
        <div style="margin-left:auto;background:#f0fdf4;border:1px solid #86efac;
             border-radius:6px;padding:0.2rem 0.6rem;font-size:0.7rem;color:#15803d;
             font-weight:500;display:flex;align-items:center;gap:4px;">
            <span style="width:6px;height:6px;background:#22c55e;border-radius:50%;display:inline-block;"></span>
            Online
        </div>
    </div>
    """, unsafe_allow_html=True)

render_chat()