from embeddings.embedding_model import EmbeddingModel
from vector_store.vector_db import VectorDB
from scripts.ingest_papers import IngestPapers

embedding_model = EmbeddingModel(model_name="intfloat/e5-large")
vector_db = VectorDB(embedding_dim=1024)
ingestor = IngestPapers(vector_db, embedding_model)

ingestor.ingest("diffusion models")
print("Vector DB size after ingest:", len(vector_db))

query_embedding = embedding_model.embed_texts(["diffusion models"])[0]
results = vector_db.search(query_embedding, k=5)
print("Search results:", results)
