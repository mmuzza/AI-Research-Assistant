import faiss
import numpy as np

class VectorDB:
    def __init__(self, embedding_dim=384, use_cosine: bool = True):
 
        self.embedding_dim = embedding_dim
        self.use_cosine = use_cosine

        self.index = faiss.IndexIDMap(faiss.IndexFlatL2(embedding_dim))
        self.metadata = []
        self.id_counter = 0 


    def add_embeddings(self, embeddings, metadata_list):

        embeddings = np.array(embeddings).astype("float32")

        if self.use_cosine:
            faiss.normalize_L2(embeddings)

        num_embeddings = embeddings.shape[0]
        ids = np.arange(self.id_counter, self.id_counter + num_embeddings)
        self.index.add_with_ids(embeddings, ids)
        self.metadata.extend(metadata_list)
        self.id_counter += num_embeddings


    def search(self, query_embedding, k: int = 5):

        query = np.array([query_embedding]).astype("float32")
        if self.use_cosine:
            faiss.normalize_L2(query)

        distances, indices = self.index.search(query, k)

        results = []
        for rank, idx in enumerate(indices[0]):
            if idx == -1: 
                continue
            results.append({
                "chunk": self.metadata[idx],
                "distance": float(distances[0][rank])
            })
        return results

    def __len__(self):
        return self.index.ntotal


if __name__ == "__main__":

    db = VectorDB(embedding_dim=384)

    embeddings = [
        [0.1]*384,
        [0.2]*384
    ]
    metadata = [
        {"paper_title": "Paper 1", "chunk_text": "Chunk 1 text"},
        {"paper_title": "Paper 2", "chunk_text": "Chunk 2 text"}
    ]

    db.add_embeddings(embeddings, metadata)

    # Query example
    query_embedding = [0.15]*384
    results = db.search(query_embedding, k=3)

    import json
    print(json.dumps(results, indent=3))