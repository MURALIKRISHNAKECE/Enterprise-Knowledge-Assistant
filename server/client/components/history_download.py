import streamlit as st


def render_history_download():
    if st.session_state.get("messages"):
        total = len(st.session_state.messages)
        user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])

        st.markdown(f"""
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px;
             padding:0.6rem 0.8rem; margin-bottom:0.6rem; font-size:0.78rem; color:#475569;">
            💬 {user_msgs} question(s) · {total} messages
        </div>
        """, unsafe_allow_html=True)

        chat_text = "\n\n".join(
            [f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages]
        )
        st.download_button(
            label="⬇ Download Chat History",
            data=chat_text,
            file_name="chat_history.txt",
            mime="text/plain",
            use_container_width=True
        )

        if st.button("🗑 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    else:
        st.markdown("""
        <div style="font-size:0.78rem; color:#94a3b8; padding:0.5rem 0;">
            No conversation yet
        </div>
        """, unsafe_allow_html=True)
        