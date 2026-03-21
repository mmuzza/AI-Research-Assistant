#  1. Finds relevant papers.

# scripts/retrieval_agent.py

from typing import List, Dict
from embeddings.embedding_model import EmbeddingModel
from vector_store.vector_db import VectorDB
from scripts.ingest_papers import IngestPapers
from sentence_transformers import CrossEncoder


class RetrievalAgent:
    """
    - Take a user query
    - Embed it
    - then search the VectorDB for relevant paper chunks
    - Return results for downstream agents (summarizer, experiment agent, etc.)
    """

    def __init__(self, vector_db: VectorDB, embedding_model: EmbeddingModel):
        self.vector_db = vector_db
        self.embedding_model = embedding_model
        self.ingestor = IngestPapers(vector_db, embedding_model)
        self.ingested_topics = set()
        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    

    def retrieve(self, query: str, k: int = 5) -> List[Dict]:


        # Dynamic ingesting
        if query.lower() not in self.ingested_topics:
            print(f"[INFO] Ingesting papers for query topic: '{query}'")
            self.ingestor.ingest(query)
            self.ingested_topics.add(query.lower())

        # 1. Embed the query
        query_embedding = self.embedding_model.embed_texts([query])[0]

        # 2. Search VectorDB
        search_results = self.vector_db.search(query_embedding, k=10)

        if not search_results:
            return []

        # 3. rerank with cross-encoder to make results better
        pairs = [(query, res["chunk"]["chunk_text"]) for res in search_results]
        scores = self.reranker.predict(pairs)
        for i, res in enumerate(search_results):
            res["rerank_score"] = scores[i]

        search_results = sorted(search_results, key=lambda x: x["rerank_score"], reverse=True)

        # 4. Keeping only top-k papers
        seen_papers = set()
        formatted_results = []

        for res in search_results:
            chunk_meta = res["chunk"]
            paper_id = chunk_meta.get("paper_id")
            if paper_id in seen_papers:
                continue
            seen_papers.add(paper_id)

            formatted_results.append({
                "chunk_text": chunk_meta.get("chunk_text"),
                "paper_id": paper_id,
                "title": chunk_meta.get("title"),
                "distance": res.get("distance"),  # optional, FAISS distance
                "authors": chunk_meta.get("authors"),
                "published": chunk_meta.get("published"),
                "pdf_url": chunk_meta.get("pdf_url"),
                "summary": chunk_meta.get("summary")
            })

            if len(formatted_results) >= k:
                break

        return formatted_results



# testing the file locally
if __name__ == "__main__":
    from embeddings.embedding_model import EmbeddingModel
    from agents.retrieval_agent import RetrievalAgent
    from scripts.ingest_papers import IngestPapers

    # Create one VectorDB instance
    vector_db = VectorDB()
    embedding_model = EmbeddingModel()

    # Pass the same DB into ingestor
    ingestor = IngestPapers(vector_db=vector_db, embedding_model=embedding_model)
    topics = ["transformers", "diffusion models", "reinforcement learning"]
    ingestor.ingest_topics(topics)

    # Now retrieval agent uses the same DB
    agent = RetrievalAgent(vector_db, embedding_model)

    query = "Recent advances in diffusion models"
    results = agent.retrieve(query, k=3)

    for i, r in enumerate(results, 1):

        print(f"\n{r['title']}")
        print(f"{r['published']}")
        print(f"{', '.join(r['authors'][:3])}")
        print(f"Score: {r['distance']:.4f}")
        print(f"Insight: {r['chunk_text'][:200]}...")
        print(f"{r['pdf_url']}")
        print(f"Summary: {r['summary']}")
