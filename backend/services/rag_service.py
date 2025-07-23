import os
import fitz  # PyMuPDF
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from backend.utils.bedrock import query_bedrock

PDF_DIR = "data"
EMBED_DIR = "embeddings"
EMBED_FILE = os.path.join(EMBED_DIR, "faiss.index")
TEXT_FILE = os.path.join(EMBED_DIR, "chunks.txt")

model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text_from_pdfs():
    all_texts = []
    for filename in os.listdir(PDF_DIR):
        if filename.endswith(".pdf"):
            path = os.path.join(PDF_DIR, filename)
            doc = fitz.open(path)
            text = ""
            for page in doc:
                text += page.get_text()
            all_texts.append(text)
    return all_texts

def create_embeddings():
    os.makedirs(EMBED_DIR, exist_ok=True)
    texts = extract_text_from_pdfs()

    chunks = []
    for text in texts:
        for i in range(0, len(text), 500):
            chunks.append(text[i:i+500])

    with open(TEXT_FILE, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(chunk.strip().replace("\n", " ") + "\n")

    embeddings = model.encode(chunks)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    faiss.write_index(index, EMBED_FILE)

def answer_query(query):
    if not os.path.exists(EMBED_FILE):
        create_embeddings()

    query_embedding = model.encode([query]).astype("float32")

    index = faiss.read_index(EMBED_FILE)
    D, I = index.search(query_embedding, k=3)

    with open(TEXT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    top_chunks = [lines[i] for i in I[0]]
    context = "\n".join(top_chunks)

    prompt = f"Answer the question based on the context below:\n\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"
    return query_bedrock(prompt)
