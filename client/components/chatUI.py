import streamlit as st
from utils.api import ask_question


def render_chat():
    st.subheader("💬 Chat with your assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render existing chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    # Input and response
    user_input = st.chat_input("Type your question....")
    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        response = ask_question(user_input)
        if response.status_code == 200:
            data = response.json()
            answer = data["response"]
            sources = data.get("sources", [])
            metrics = data.get("metrics", {})
            ragas = data.get("ragas", {})

            st.chat_message("assistant").markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

            # ── Query Metrics ──────────────────────────────────
            if metrics:
                with st.expander("📊 Query Metrics"):
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("⏱ Latency", f"{metrics.get('latency_seconds', 0)}s")
                    col2.metric("🔢 Total Tokens", metrics.get('total_tokens', 0))
                    col3.metric("📥 Prompt Tokens", metrics.get('prompt_tokens', 0))
                    col4.metric("💰 Est. Cost", f"${metrics.get('estimated_cost_usd', 0)}")

            # ── RAGAS Evaluation Scores ────────────────────────
            if ragas:
                with st.expander("🧪 RAGAS Evaluation Scores"):
                    col1, col2, col3 = st.columns(3)
                    col1.metric(
                        "Faithfulness",
                        ragas.get("faithfulness", "N/A"),
                        help="How factually consistent is the answer with the context?"
                    )
                    col2.metric(
                        "Answer Relevancy",
                        ragas.get("answer_relevancy", "N/A"),
                        help="How relevant is the answer to the question?"
                    )
                    col3.metric(
                        "Context Precision",
                        ragas.get("context_precision", "N/A"),
                        help="How precise is the retrieved context?"
                    )
                    if ragas.get("error"):
                        st.warning(f"RAGAS error: {ragas['error']}")

            # ── Sources ────────────────────────────────────────
            if sources:
                with st.expander("📄 Sources"):
                    for src in sources:
                        if src:
                            st.markdown(f"- `{src}`")
        else:
            st.error(f"Error: {response.text}")