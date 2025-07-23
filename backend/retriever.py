
    
    # backend/retriever.py
from backend.embedder import Embedder

class Retriever:
    def __init__(self):
        self.embedder = Embedder()
        self.index, self.docs = self.embedder.load_index()

    def search(self, query, k=2):
        query_vector = self.embedder.embed_docs([query])
        D, I = self.index.search(query_vector, k)
        return [self.docs[i] for i in I[0]]

