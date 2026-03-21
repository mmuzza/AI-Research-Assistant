from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.retrieval_agent import RetrievalAgent
from embeddings.embedding_model import EmbeddingModel
from vector_store.vector_db import VectorDB
from fastapi.middleware.cors import CORSMiddleware

from agents.orchestrator_agent import OrchestratorAgent
from agents.summarizer_agent import SummarizerAgent
from langchain_openai import ChatOpenAI

from agents.research_gap_agent import ResearchGapAgent
from agents.comparison_agent import ComparisonAgent

# FastAPI app
app = FastAPI(title="AI Research Assistant API")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body model
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

# Initialize backend components
vector_db = VectorDB(embedding_dim=1024)  # match your embedding dim
embedding_model = EmbeddingModel(model_name="intfloat/e5-large")
retrieval_agent = RetrievalAgent(vector_db, embedding_model)




#####################################################################
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
summarizer_agent = SummarizerAgent(llm)
research_gap_agent = ResearchGapAgent(llm)
comparison_agent = ComparisonAgent(llm)
orchestrator = OrchestratorAgent(retrieval_agent,
                                summarizer_agent,
                                research_gap_agent=research_gap_agent,
                                comparison_agent=comparison_agent)

# POST endpoint
@app.post("/query")
def query_endpoint(request: dict):
    query = request.get("query")

    # if not query:
    #     return {"summary": "", "papers": []}

    if not query:
        return {
            "retrieved_papers": [],
            "paper_summaries": [],
            "summary": ""
        }

    result = orchestrator.run(query)
    return result