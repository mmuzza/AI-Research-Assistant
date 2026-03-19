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

class RAGPipeline:

    def __init__(self, vector_db, embedding_model, llm):
        self.vector_db = vector_db
        self.embedding_model = embedding_model
        self.llm = llm

    def query(self, question: str, k: int = 5):

        query_embedding = self.embedding_model.embed_texts([question])[0]


        results = self.vector_db.search(query_embedding, k=k)

        if not results:
            return "No relevant papers found."

        context_text = "\n\n".join([r["chunk"]["chunk_text"] for r in results])
        prompt = f"Answer this question using the context below:\n{context_text}\n\nQuestion: {question}"

        answer = self.llm.generate(prompt)

        return answer



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