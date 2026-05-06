import faiss
import numpy as np
import os
import hashlib
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

def get_embedding(text: str) -> list:
    words = text.lower().split()
    vector = np.zeros(768, dtype="float32")
    for word in words:
        hash_val = int(hashlib.md5(word.encode()).hexdigest(), 16)
        idx = hash_val % 768
        vector[idx] += 1.0
    norm = np.linalg.norm(vector)
    if norm > 0:
        vector = vector / norm
    return vector.tolist()

def chunk_text(text: str, chunk_size: int = 500) -> list:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - 50):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

class VectorStore:
    def __init__(self):
        self.index = None
        self.chunks = []

    def build_index(self, text: str):
        self.chunks = chunk_text(text)
        embeddings = [get_embedding(chunk) for chunk in self.chunks]
        dim = len(embeddings[0])
        self.index = faiss.IndexFlatL2(dim)
        vectors = np.array(embeddings, dtype="float32")
        self.index.add(vectors)

    def search(self, query: str, top_k: int = 3) -> list:
        if not self.index:
            return []
        query_vec = np.array([get_embedding(query)], dtype="float32")
        distances, indices = self.index.search(query_vec, top_k)
        results = []
        for idx in indices[0]:
            if idx < len(self.chunks):
                results.append(self.chunks[idx])
        return results

vector_stores = {}