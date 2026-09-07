# 🧠 Enterprise Knowledge Assistant

> A production-grade RAG system that answers employee questions from uploaded company documents — built with FastAPI, Groq LLM, FastEmbed, Pinecone, BM25, and Streamlit.

---

## 📖 Overview

The **Enterprise Knowledge Assistant** is a Retrieval-Augmented Generation (RAG) application that enables employees to upload internal documents and get accurate, source-grounded answers in natural language.

Designed for use cases such as:

- HR policies and onboarding guides
- Legal and compliance documents
- Research papers and technical manuals
- Product documentation and FAQs
- Training materials and internal knowledge bases

Users upload a PDF; the assistant chunks, embeds, and indexes the content — then answers questions grounded strictly in the document, eliminating hallucination risk.

---

## ⚙️ Tech Stack

| Layer | Technology | Role |
|---|---|---|
| **Frontend** | Streamlit | PDF upload UI and conversational chat interface |
| **Backend** | FastAPI | REST API for document ingestion, retrieval, and LLM orchestration |
| **LLM** | Groq (`openai/gpt-oss-20b`) | Fast, low-latency response generation |
| **Embeddings** | FastEmbed (`BAAI/bge-small-en-v1.5`) | Lightweight local embeddings (~50MB, 384 dims) |
| **RAG Framework** | LangChain + LangChain Classic | Document loading, chunking, retrieval chain, prompt management |
| **Vector Store** | Pinecone | Persistent semantic search over embedded document chunks |
| **Keyword Search** | BM25 (rank-bm25) | Exact keyword matching for hybrid retrieval |
| **Reranking** | Reciprocal Rank Fusion | Combines dense + BM25 results for better precision |
| **Evaluation** | Heuristic RAGAS metrics | Faithfulness, Answer Relevancy, Context Precision |
| **Deployment** | Render (Cloud) | Public demo hosting for backend and frontend |

---

## 🏗️ Architecture

```
User (Browser)
     │
     ▼
┌─────────────────┐
│  Streamlit UI   │  ← PDF upload + chat + metrics display
└────────┬────────┘
         │ HTTP (REST)
         ▼
┌──────────────────────────────────────────┐
│            FastAPI Backend               │
│  /upload_pdfs/   │   /ask/              │
└──────┬───────────┴──────────┬───────────┘
       │                      │
       ▼                      ▼
┌─────────────┐      ┌────────────────────────────┐
│  FastEmbed  │      │   Hybrid Retrieval         │
│  + Pinecone │      │   Dense (Pinecone)         │
│  Indexing   │      │   + BM25 Keyword           │
│  + BM25     │      │   + RRF Reranking          │
└─────────────┘      └────────────┬───────────────┘
                                  │
                                  ▼
                     ┌────────────────────┐
                     │  LangChain Chain   │
                     │  + Groq LLM        │
                     └────────┬───────────┘
                              │
                              ▼
                     ┌────────────────────┐
                     │  RAGAS Evaluation  │
                     │  + Metrics Logging │
                     └────────────────────┘
```

**Document ingestion flow:**
1. PDF uploaded via Streamlit → sent to FastAPI `/upload_pdfs/` endpoint
2. LangChain loads and chunks the PDF (chunk size: 600, overlap: 150)
3. FastEmbed embeds chunks locally (BAAI/bge-small-en-v1.5, 384 dims)
4. Embeddings upserted to Pinecone; BM25 index built and persisted locally

**Query flow:**
1. User question sent to FastAPI `/ask/` endpoint
2. Question embedded using FastEmbed
3. Dense retrieval: top-5 chunks from Pinecone
4. BM25 retrieval: top-5 chunks from local index
5. Reciprocal Rank Fusion merges and reranks both result sets
6. Top-5 fused chunks passed to Groq LLM via LangChain chain
7. Grounded answer + RAGAS scores + latency returned to Streamlit UI

---

## 🚀 Features

- **Hybrid retrieval** — BM25 + dense embeddings combined with Reciprocal Rank Fusion for higher precision
- **FastEmbed** — lightweight 50MB local embedding model, 11x faster than HuggingFace sentence-transformers
- **RAGAS evaluation** — per-query Faithfulness, Answer Relevancy, and Context Precision scores
- **Latency tracking** — end-to-end query latency logged and displayed per response
- **Source attribution** — every answer cites the source document
- **Modular backend** — FastAPI with structured logging, middleware, and separated route handlers
- **Chat history export** — download full conversation as `.txt`

---

## 📁 Project Structure

```
Enterprise Knowledge Assistant (RAG System)/
├── .env                          # API keys (not committed)
├── .env.example                  # Key template for onboarding
├── pyproject.toml                # Project metadata and dependencies
├── README.md
│
├── server/
│   ├── main.py                   # FastAPI app entry point
│   ├── logger.py                 # Structured logging setup
│   ├── DockerFile                # Docker config
│   ├── requirements.txt
│   ├── middlewares/
│   │   └── exception_handlers.py # Global error handling
│   ├── modules/
│   │   ├── llm.py                # Groq LLM + prompt template
│   │   ├── load_vectorstore.py   # FastEmbed + Pinecone + BM25 indexing
│   │   ├── query_handlers.py     # Chain invocation + latency tracking
│   │   └── evaluation.py        # Heuristic RAGAS evaluation
│   ├── routes/
│   │   ├── ask_question.py       # /ask/ endpoint — hybrid retrieval + RRF
│   │   └── upload_pdfs.py        # /upload_pdfs/ endpoint
│   └── uploaded_docs/            # Uploaded PDFs stored here
│
└── client/
    ├── app.py                    # Streamlit app entry point
    ├── config.py                 # API base URL config
    ├── requirements.txt
    ├── .streamlit/
    │   └── config.toml           # Light theme config
    ├── components/
    │   ├── chatUI.py             # Chat interface + metrics display
    │   ├── upload.py             # PDF upload component
    │   └── history_download.py  # Chat history export
    └── utils/
        └── api.py                # HTTP calls to backend
```

---

## 🔧 Prerequisites

- Python 3.11+
- [Groq API key](https://console.groq.com/)
- [Pinecone API key](https://www.pinecone.io/)

No Hugging Face token required — FastEmbed downloads models automatically.

---

## 🛠️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/enterprise-knowledge-assistant.git
cd "Enterprise Knowledge Assistant (RAG System)"
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn streamlit langchain langchain-community langchain-groq \
    langchain-classic langchain-core langchain-text-splitters pinecone fastembed \
    python-dotenv pypdf tqdm rank-bm25 datasets ragas
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=enterprise-index
PINECONE_ENVIRONMENT=us-east-1
HOST=0.0.0.0
PORT=8000
API_BASE_URL=http://localhost:8000
```

### 5. Run the backend

```bash
cd server
uvicorn main:app --reload --port 8000
```

### 6. Run the frontend

```bash
cd client
streamlit run app.py --theme.base="light" --theme.backgroundColor="#f8fafc" \
    --theme.secondaryBackgroundColor="#f1f5f9" \
    --theme.textColor="#0f172a" --theme.primaryColor="#3b82f6"
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check + endpoint listing |
| `POST` | `/upload_pdfs/` | Upload PDFs; triggers chunking, embedding, and Pinecone + BM25 indexing |
| `POST` | `/ask/` | Submit a question; returns answer, sources, metrics, and RAGAS scores |

---

## 📊 Performance Results

Measured on `HR-Policy.pdf` (18KB, 25 chunks):

| Metric | HuggingFace Embeddings | FastEmbed (current) |
|---|---|---|
| Model size | ~438MB | ~50MB |
| Startup time | ~15–20s | ~2–3s |
| Query latency | ~22s | **~2s** |
| Speed improvement | baseline | **~11x faster** |

**Sample RAGAS scores (HR Policy document):**

| Question | Faithfulness | Answer Relevancy | Context Precision |
|---|---|---|---|
| "What is the probation period?" | 0.881 | 1.000 | 0.452 |
| "Explain work hours" | 0.615 | 1.000 | 0.269 |
| "What are public holidays?" | 0.349 | 0.000 | 0.191 |

---

## ⚠️ Trade-offs & Design Decisions

| Decision | Trade-off |
|---|---|
| FastEmbed over HuggingFace | 11x faster, smaller model, but slightly lower embedding quality on domain-specific text |
| Heuristic RAGAS over full RAGAS | Avoids OpenAI dependency; scores are approximate (word overlap), not LLM-judged |
| BM25 persisted to disk (`.pkl`) | Fast local retrieval but lost on server restart — re-upload PDF to rebuild |
| Pinecone serverless | No infrastructure management, but cold starts add ~0.5s on first query |
| `openai/gpt-oss-20b` on Groq | No token usage metadata returned — cost tracking shows $0 even when tokens are used |
| RetrievalQA from LangChain Classic | Deprecated API; kept for stability — should migrate to LCEL in next iteration |
| Chunk size 600 / overlap 150 | Balanced context window; very large PDFs may need smaller chunks for precision |

---

## 🐛 Failure Narratives

**1. Model decommissioning (Groq)**
During development, both `llama-3.1-8b-instant` and `llama3-70b-8192` were decommissioned mid-project. This required two model swaps and highlighted the risk of hardcoding model names. Resolution: model name should be moved to `.env`.

**2. Pinecone dimension mismatch**
Switching from HuggingFace (768 dims) to FastEmbed (384 dims) caused silent upsert failures until the index was deleted and recreated. Resolution: added dimension check at startup with automatic index recreation.

**3. LangChain breaking changes**
`langchain.text_splitter`, `langchain.prompts`, `langchain.chains`, and `langchain.schema` all moved to new packages between versions. Required 4 separate import fixes. Resolution: pin LangChain versions in `requirements.txt`.

**4. BM25 index lost on restart**
BM25 index is built in memory and persisted to `bm25_index.pkl`. If the server restarts without the file, BM25 falls back to dense-only retrieval silently. Resolution: log a clear warning; future fix is to rebuild from uploaded docs on startup.

**5. Pinecone v3 upsert format change**
Original code used `zip(ids, embeddings, metadatas)` which was valid in v2 but silently dropped vectors in v3. Resolution: switched to explicit list of dicts `{"id": ..., "values": ..., "metadata": ...}`.

---

## ☁️ Deployment (Render)

Deploy as two separate Render web services:

**Backend:**
- Root directory: `server/`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port 10000`
- Add all `.env` variables as environment variables in Render dashboard

**Frontend:**
- Root directory: `client/`
- Build command: `pip install -r requirements.txt`
- Start command: `streamlit run app.py --server.port 10000 --server.address 0.0.0.0 --theme.base light`
- Set `API_BASE_URL` to your Render backend URL

---

## 🧪 Example Usage

1. Start both servers and open [http://localhost:8501](http://localhost:8501)
2. Upload `HR-Policy.pdf` via the sidebar
3. Ask questions:
   - *"What is the probation period for new employees?"*
   - *"What are the working hours and flexible start times?"*
   - *"How many days of earned leave are employees entitled to?"*
   - *"What happens during the exit interview process?"*
4. Review the answer, RAGAS scores, latency, and source citations

---

## 📌 Known Limitations

- Token usage shows `0` for `openai/gpt-oss-20b` on Groq — model does not return usage metadata
- BM25 index requires re-upload of PDFs after server restart
- RAGAS scores are heuristic (word overlap), not LLM-judged — treat as directional signals
- No authentication — all uploaded documents are accessible to anyone with the URL

---

## 👤 Author

**K MURALI KRISHNA**  


---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.