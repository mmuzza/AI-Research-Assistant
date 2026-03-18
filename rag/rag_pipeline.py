# '''
# RAG PIPELINE:
# -------------

# User query
# ↓
# embed query
# ↓
# search vector DB
# ↓
# retrieve relevant chunks
# ↓
# send to LLM
# ↓
# generate answer
# '''

# class RAGPipeline:

#     def __init__(self, vector_db, embedding_model, llm):
#         self.vector_db = vector_db
#         self.embedding_model = embedding_model
#         self.llm = llm

#     def query(self, question: str, k: int = 5):

#         query_embedding = self.embedding_model.embed_texts([question])[0]


#         results = self.vector_db.search(query_embedding, k=k)

#         if not results:
#             return "No relevant papers found."

#         context_text = "\n\n".join([r["chunk"]["chunk_text"] for r in results])
#         prompt = f"Answer this question using the context below:\n{context_text}\n\nQuestion: {question}"

#         answer = self.llm.generate(prompt)

#         return answer



from typing import List, Dict
from embeddings.embedding_model import EmbeddingModel
from vector_score.vector_db import VectorDB
from scripts.ingest_papers import IngestPapers


class RetrievalAgent:
    def __init__(
        self,
        vector_db: VectorDB,
        embedding_model: EmbeddingModel,
        ingestor: IngestPapers = None, 
        min_results: int = 3
    ):
        self.vector_db = vector_db
        self.embedding_model = embedding_model
        self.ingestor = ingestor
        self.min_results = min_results

    def retrieve(self, query: str, k: int = 5) -> Dict:
        """
        1. Embed query
        2. Search vector DB
        3. If not enough results -> dynamically ingest
        4. Return structured JSON
        """

        # 1. Embed query
        query_embedding = self.embedding_model.embed_texts([query])[0]

        # 2. Search
        results = self.vector_db.search(query_embedding, k)

        # 3. Dynamic ingestion
        if len(results) < self.min_results and self.ingestor:
            print("[INFO] Not enough results, performing dynamic ingestion...")
            self.ingestor.ingest_topics(query)
            results = self.vector_db.search(query_embedding, k)

        # 4. Gathering result and returning Json for front end
        formatted_results = []
        seen_papers = set()

        for res in results:
            meta = res["metadata"]

            formatted_results.append({
                "paper_id": meta.get("paper_id"),
                "title": meta.get("title"),
                "chunk_text": meta.get("chunk_text"),
                "distance": res["distance"],
                # Optional richer info (if you add during ingestion)
                "authors": meta.get("authors"),
                "published": str(meta.get("published")),
                "pdf_url": meta.get("pdf_url")
            })

            seen_papers.add(meta.get("paper_id"))

        return {
            "query": query,
            "num_results": len(formatted_results),
            "unique_papers": len(seen_papers),
            "results": formatted_results
        }


# ------------------ TEST RUN ------------------

if __name__ == "__main__":
    from vector_score.vector_db import VectorDB
    from embeddings.embedding_model import EmbeddingModel
    from scripts.ingest_papers import IngestPapers

    # Shared DB
    vector_db = VectorDB()
    embedding_model = EmbeddingModel()

    # Ingestor (for dynamic ingestion)
    ingestor = IngestPapers(vector_db)

    # OPTIONAL: pre-ingest some topics
    topics = ["transformers", "diffusion models"]
    ingestor.ingest_topics(topics)

    # Create agent
    agent = RetrievalAgent(
        vector_db=vector_db,
        embedding_model=embedding_model,
        ingestor=ingestor
    )

    # Query
    query = "Recent advances in diffusion models"
    output = agent.retrieve(query, k=5)

    import json
    print(json.dumps(output, indent=2))