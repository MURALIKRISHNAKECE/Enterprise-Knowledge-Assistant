import os
from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from modules.llm import get_llm_chain
from modules.query_handlers import query_chain
from modules.load_vectorstore import load_bm25_index, embed_model
from modules.evaluation import run_ragas_evaluation
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from pinecone import Pinecone
from pydantic import Field
from typing import List, Optional
from logger import logger

router = APIRouter()


def reciprocal_rank_fusion(dense_docs, bm25_docs, k=60):
    scores = {}
    for rank, doc in enumerate(dense_docs):
        key = doc.page_content
        scores[key] = scores.get(key, 0) + 1 / (k + rank + 1)
    for rank, doc in enumerate(bm25_docs):
        key = doc.page_content
        scores[key] = scores.get(key, 0) + 1 / (k + rank + 1)
    all_docs = {doc.page_content: doc for doc in dense_docs + bm25_docs}
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [all_docs[key] for key, _ in ranked[:5]]


@router.post("/ask/")
async def ask_question(question: str = Form(...)):
    try:
        logger.info(f"User query: {question}")

        # ── Dense retrieval (Pinecone + FastEmbed) ──────────────
        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        index = pc.Index(os.environ["PINECONE_INDEX_NAME"])

        # Use cached FastEmbed model
        embedded_query = list(embed_model.query_embed(question))[0].tolist()
        res = index.query(vector=embedded_query, top_k=5, include_metadata=True)

        dense_docs = [
            Document(
                page_content=match["metadata"].get("text", ""),
                metadata=match["metadata"]
            )
            for match in res["matches"]
        ]

        # ── BM25 retrieval ──────────────────────────────────────
        bm25, chunks = load_bm25_index()
        if bm25 and chunks:
            tokenized_query = question.lower().split()
            bm25_scores = bm25.get_scores(tokenized_query)
            top_bm25_indices = sorted(
                range(len(bm25_scores)),
                key=lambda i: bm25_scores[i],
                reverse=True
            )[:5]
            bm25_docs = [chunks[i] for i in top_bm25_indices]
        else:
            bm25_docs = []
            logger.warning("BM25 index not found — using dense retrieval only")

        # ── Reciprocal Rank Fusion ──────────────────────────────
        fused_docs = reciprocal_rank_fusion(dense_docs, bm25_docs)
        logger.info(f"RRF: {len(dense_docs)} dense + {len(bm25_docs)} BM25 → {len(fused_docs)} fused")

        # ── Build retriever and chain ───────────────────────────
        class SimpleRetriever(BaseRetriever):
            tags: Optional[List[str]] = Field(default_factory=list)
            metadata: Optional[dict] = Field(default_factory=dict)

            def __init__(self, documents: List[Document]):
                super().__init__()
                self._docs = documents

            def _get_relevant_documents(self, query: str) -> List[Document]:
                return self._docs

        retriever = SimpleRetriever(fused_docs)
        chain = get_llm_chain(retriever)
        result = query_chain(chain, question)

        # ── RAGAS Evaluation ────────────────────────────────────
        contexts = [doc.page_content for doc in fused_docs]
        ragas_scores = run_ragas_evaluation(question, result["response"], contexts)
        result["ragas"] = ragas_scores

        logger.info("Query successful")
        return result

    except Exception as e:
        logger.exception("Error processing question")
        return JSONResponse(status_code=500, content={"error": str(e)})