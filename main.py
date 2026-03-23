# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from langchain_openai import ChatOpenAI

# from embeddings.embedding_model import EmbeddingModel
# from vector_store.vector_db import VectorDB
# from fastapi.middleware.cors import CORSMiddleware


# from agents.orchestrator_agent import OrchestratorAgent

# from agents.retrieval_agent import RetrievalAgent
# from agents.summarizer_agent import SummarizerAgent
# from agents.research_gap_agent import ResearchGapAgent
# from agents.comparison_agent import ComparisonAgent
# from agents.experiment_agent import ExperimentAgent

# from agents.knowledge_graph_agent import KnowledgeGraphAgent

# # FastAPI app
# app = FastAPI(title="AI Research Assistant API")

# # Allow frontend requests
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # React dev server
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Request body model
# class QueryRequest(BaseModel):
#     query: str
#     top_k: int = 5

# # Initialize backend components
# vector_db = VectorDB(embedding_dim=1024)  # match your embedding dim
# embedding_model = EmbeddingModel(model_name="intfloat/e5-large")
# retrieval_agent = RetrievalAgent(vector_db, embedding_model)




# #####################################################################
# llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
# summarizer_agent = SummarizerAgent(llm)
# research_gap_agent = ResearchGapAgent(llm)
# comparison_agent = ComparisonAgent(llm)
# experiment_agent = ExperimentAgent(llm)
# knowledge_graph_agent = KnowledgeGraphAgent(llm)

# orchestrator = OrchestratorAgent(retrieval_agent,
#                                 summarizer_agent,
#                                 research_gap_agent=research_gap_agent,
#                                 comparison_agent=comparison_agent,
#                                 experiment_agent=experiment_agent,
#                                 knowledge_graph_agent=knowledge_graph_agent)

# # POST endpoint
# @app.post("/query")
# def query_endpoint(request: dict):
#     query = request.get("query")

#     # if not query:
#     #     return {"summary": "", "papers": []}

#     if not query:
#         return {
#             "retrieved_papers": [],
#             "paper_summaries": [],
#             "summary": ""
#         }

#     result = orchestrator.run(query)
#     return result
























from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_openai import ChatOpenAI
from embeddings.embedding_model import EmbeddingModel
from vector_store.vector_db import VectorDB
from agents.retrieval_agent import RetrievalAgent
from agents.summarizer_agent import SummarizerAgent
from agents.research_gap_agent import ResearchGapAgent
from agents.comparison_agent import ComparisonAgent
from agents.experiment_agent import ExperimentAgent
from agents.knowledge_graph_agent import KnowledgeGraphAgent

app = FastAPI(title="AI Research Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Initialize components ─────────────────────────────
vector_db = VectorDB(embedding_dim=1024)
embedding_model = EmbeddingModel(model_name="intfloat/e5-large")
retrieval_agent = RetrievalAgent(vector_db, embedding_model)

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
summarizer_agent = SummarizerAgent(llm)
research_gap_agent = ResearchGapAgent(llm)
comparison_agent = ComparisonAgent(llm)
experiment_agent = ExperimentAgent(llm)
knowledge_graph_agent = KnowledgeGraphAgent(llm)


# ── Helper: make paper_summaries JSON-safe ────────────
def sanitize_summaries(summaries: list) -> list:
    clean = []
    for p in summaries:
        entry = dict(p)
        if hasattr(entry.get("published"), "isoformat"):
            entry["published"] = entry["published"].isoformat()
        clean.append(entry)
    return clean


# ── 1. Retrieve + Summarize ───────────────────────────
@app.post("/query/retrieve")
def retrieve_endpoint(request: dict):
    query = request.get("query", "").strip()
    if not query:
        return {"retrieved_papers": [], "paper_summaries": [], "global_summary": ""}

    # Retrieve chunks
    retrieved_chunks = retrieval_agent.retrieve(query)

    # Build deduplicated paper list
    seen, retrieved_papers = set(), []
    for chunk in retrieved_chunks:
        pid = chunk["paper_id"]
        if pid not in seen:
            seen.add(pid)
            retrieved_papers.append({
                "paper_id": pid,
                "title": chunk["title"],
                "pdf_url": chunk["pdf_url"],
                "authors": chunk.get("authors"),
                "published": chunk["published"].isoformat()
                    if hasattr(chunk.get("published"), "isoformat")
                    else chunk.get("published"),
            })

    # Summarize
    summary = summarizer_agent.summarize(retrieved_chunks)
    paper_summaries = sanitize_summaries(summary["paper_summaries"])
    global_summary = summary["global_summary"]

    return {
        "retrieved_papers": retrieved_papers,
        "paper_summaries": paper_summaries,
        "global_summary": global_summary,
    }


# ── 2. Research Gaps ──────────────────────────────────
@app.post("/query/gaps")
def gaps_endpoint(request: dict):
    paper_summaries = request.get("paper_summaries", [])
    if not paper_summaries:
        return {"basic_gaps": [], "insights": ""}

    result = research_gap_agent.analyze(paper_summaries)
    return result


# ── 3. Knowledge Graph ────────────────────────────────
@app.post("/query/graph")
def graph_endpoint(request: dict):
    paper_summaries = request.get("paper_summaries", [])
    if not paper_summaries:
        return {"nodes": [], "edges": []}

    result = knowledge_graph_agent.build_graph(paper_summaries)
    return result


# ── 4. Experiment Ideas ───────────────────────────────
@app.post("/query/experiments")
def experiments_endpoint(request: dict):
    paper_summaries = request.get("paper_summaries", [])
    research_gaps = request.get("research_gaps", None)
    if not paper_summaries:
        return {"ideas": []}

    result = experiment_agent.generate(paper_summaries, research_gaps)
    return result


# ── 5. Comparison ─────────────────────────────────────
@app.post("/query/compare")
def compare_endpoint(request: dict):
    paper_summaries = request.get("paper_summaries", [])
    if not paper_summaries:
        return {"comparison": ""}

    result = comparison_agent.compare(paper_summaries)
    # comparison_agent returns a raw string
    return {"comparison": result}