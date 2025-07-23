# backend/embedder.py
import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index_path = "embeddings/index.faiss"
        self.mapping_path = "embeddings/mapping.pkl"

    def embed_docs(self, docs):
        vectors = self.model.encode(docs)
        return vectors

    def save_index(self, vectors, docs):
        os.makedirs("embeddings", exist_ok=True)
        index = faiss.IndexFlatL2(vectors.shape[1])
        index.add(np.array(vectors))
        faiss.write_index(index, self.index_path)

        with open(self.mapping_path, "wb") as f:
            pickle.dump(docs, f)

    def load_index(self):
        index = faiss.read_index(self.index_path)
        with open(self.mapping_path, "rb") as f:
            docs = pickle.load(f)
        return index, docs
