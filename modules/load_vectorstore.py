import os
import time
import pickle
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rank_bm25 import BM25Okapi
from fastembed import TextEmbedding

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = "us-east-1"
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "enterprise-index")
BM25_INDEX_PATH = "./bm25_index.pkl"
FASTEMBED_MODEL = "BAAI/bge-small-en-v1.5"  # 384 dims, ~50MB

UPLOAD_DIR = "./uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
spec = ServerlessSpec(cloud="aws", region=PINECONE_ENV)
existing_indexes = [i["name"] for i in pc.list_indexes()]

# FastEmbed uses 384 dims — recreate index if wrong dimension
if PINECONE_INDEX_NAME in existing_indexes:
    index_info = pc.describe_index(PINECONE_INDEX_NAME)
    if index_info.dimension != 384:
        print("Recreating Pinecone index for FastEmbed (384 dims)...")
        pc.delete_index(PINECONE_INDEX_NAME)
        existing_indexes = []

if PINECONE_INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=384,
        metric="cosine",
        spec=spec
    )
    while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
        time.sleep(1)

index = pc.Index(PINECONE_INDEX_NAME)

# Load FastEmbed model once at startup
print("Loading FastEmbed model...")
embed_model = TextEmbedding(model_name=FASTEMBED_MODEL)
print("FastEmbed model loaded.")


def build_bm25_index(chunks):
    tokenized = [chunk.page_content.lower().split() for chunk in chunks]
    bm25 = BM25Okapi(tokenized)
    with open(BM25_INDEX_PATH, "wb") as f:
        pickle.dump({"bm25": bm25, "chunks": chunks}, f)
    print(f"BM25 index saved to {BM25_INDEX_PATH}")
    return bm25, chunks


def load_bm25_index():
    if os.path.exists(BM25_INDEX_PATH):
        with open(BM25_INDEX_PATH, "rb") as f:
            data = pickle.load(f)
        return data["bm25"], data["chunks"]
    return None, []


def load_vectorstore(uploaded_files):
    file_paths = []

    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR) / file.filename
        with open(save_path, "wb") as f:
            f.write(file.file.read())
        file_paths.append(str(save_path))

    all_chunks = []

    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=600, chunk_overlap=150
        )
        chunks = splitter.split_documents(documents)
        all_chunks.extend(chunks)

        texts = [chunk.page_content for chunk in chunks]
        metadatas = [
            {"text": chunk.page_content, "source": str(file_path)}
            for chunk in chunks
        ]
        ids = [f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]

        print(f"Embedding {len(texts)} chunks with FastEmbed...")
        embeddings = list(embed_model.embed(texts))

        vectors = [
            {"id": id_, "values": emb.tolist(), "metadata": meta}
            for id_, emb, meta in zip(ids, embeddings, metadatas)
        ]

        print("Uploading to Pinecone...")
        with tqdm(total=len(vectors), desc="Upserting to Pinecone") as progress:
            index.upsert(vectors=vectors)
            progress.update(len(vectors))

        print(f"Upload complete for {file_path}")

    print("Building BM25 index...")
    build_bm25_index(all_chunks)
    print("BM25 index built successfully.")