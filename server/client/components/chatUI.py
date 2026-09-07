import streamlit as st
from utils.api import ask_question


def render_chat():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Empty state
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align:center; padding: 3rem 1rem;">
            <div style="font-size:3rem; margin-bottom:1rem;">💬</div>
            <h3 style="color:#0f172a; font-size:1rem; font-weight:600; margin-bottom:0.5rem;">
                Start a conversation
            </h3>
            <p style="color:#64748b; font-size:0.85rem;">
                Upload a PDF document and ask any question about its content.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and "metrics" in msg:
                _render_metrics(msg["metrics"], msg.get("ragas", {}), msg.get("sources", []))

    # Input
    user_input = st.chat_input("Ask a question about your documents...")
    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            with st.spinner("Searching documents..."):
                response = ask_question(user_input)

            if response.status_code == 200:
                data = response.json()
                answer = data["response"]
                sources = data.get("sources", [])
                metrics = data.get("metrics", {})
                ragas = data.get("ragas", {})

                st.markdown(answer)
                _render_metrics(metrics, ragas, sources)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "metrics": metrics,
                    "ragas": ragas,
                    "sources": sources
                })
            else:
                st.error(f"Error: {response.text}")


def _render_metrics(metrics, ragas, sources):
    if metrics:
        with st.expander("📊 Query Metrics", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("⏱ Latency", f"{metrics.get('latency_seconds', 0)}s")
            col2.metric("🔢 Total Tokens", metrics.get('total_tokens', 0))
            col3.metric("📥 Prompt Tokens", metrics.get('prompt_tokens', 0))
            col4.metric("💰 Est. Cost", f"${metrics.get('estimated_cost_usd', 0)}")

    if ragas:
        with st.expander("🧪 RAGAS Evaluation", expanded=False):
            col1, col2, col3 = st.columns(3)
            col1.metric("Faithfulness", ragas.get("faithfulness", "N/A"))
            col2.metric("Answer Relevancy", ragas.get("answer_relevancy", "N/A"))
            col3.metric("Context Precision", ragas.get("context_precision", "N/A"))
            if ragas.get("error"):
                st.warning(f"Evaluation error: {ragas['error']}")

    if sources:
        unique_sources = list(set([s for s in sources if s]))
        if unique_sources:
            with st.expander("📄 Sources", expanded=False):
                for src in unique_sources:
                    st.markdown(f"- `{src}`")