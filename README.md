# AI Research Assistant

A multi-agent system that takes a plain-language research question and does everything a researcher would spend hours doing — finding papers, reading them, findingg gaps, proposing experiments, and comparing approaches — all in one pipeline.

Built with FastAPI, React, and a handful of specialized AI agents talking to each other behind the scenes.

---

## What it actually does

You type something like _"diffusion models in medical imaging"_ and hit search. From that point the system takes over:

1. **Retrieval Agent** — queries arXiv, downloads the PDFs, parses and chunks the text, embeds everything using `intfloat/e5-large`, and stores it in a FAISS vector index. A cross-encoder then reranks the results so the most relevant chunks rise to the top.

2. **Summarizer Agent** — reads the top chunks from each paper and generates individual summaries, then synthesizes a single global summary across all of them — key trends, differences, the works.

3. **Research Gap Agent** — analyzes the summaries and identifies what hasn't been done yet. Which methods haven't been applied to which tasks? What do all these papers quietly avoid?

4. **Knowledge Graph Agent** — extracts entities (models, methods, datasets, concepts) and the relationships between them, then returns a graph you can actually interact with.

5. **Experiment Agent** — given the papers and the identified gaps, proposes 3–5 concrete experiment ideas with methods, expected outcomes, and a difficulty rating.

6. **Comparison Agent** — benchmarks the papers against each other: similarities, differences, tradeoffs, and which paper is best suited for which use case.

The frontend shows each agent activating in sequence as the pipeline runs, then collapses everything into a tabbed research report when it's done.

---

## Project structure

```
├── agents/
│   ├── retrieval_agent.py        # Embeds query, searches FAISS, reranks
│   ├── summarizer_agent.py       # Per-paper + global summarization
│   ├── research_gap_agent.py     # Gap detection and LLM analysis
│   ├── knowledge_graph_agent.py  # Entity/relationship extraction → JSON graph
│   ├── experiment_agent.py       # Novel experiment idea generation
│   └── comparison_agent.py       # Cross-paper benchmarking
│
├── data_pipeline/
│   ├── arxiv_client.py           # arXiv API wrapper
│   ├── pdf_downloader.py         # Downloads PDFs by paper ID
│   ├── pdf_parser.py             # Extracts and cleans raw text
│   └── chunking.py               # Sliding window text chunker
│
├── embeddings/
│   └── embedding_model.py        # SentenceTransformer wrapper (e5-large)
│
├── vector_store/
│   └── vector_db.py              # FAISS index with cosine similarity
│
├── scripts/
│   └── ingest_papers.py          # Orchestrates the full ingestion pipeline
│
├── main.py                       # FastAPI app — 5 split endpoints
│
└── frontend/
    └── src/
        ├── api/api.js             # One function per endpoint
        ├── components/
        │   ├── SearchBar.jsx
        │   ├── PaperCard.jsx
        │   ├── PipelinePanel.jsx  # Live agent progress visualization
        │   ├── ReportTabs.jsx     # 6-tab research report
        │   └── KnowledgeGraph.jsx # react-force-graph-2d visualization
        └── App.js                 # Pipeline orchestration and phase state
```

---

## Tech stack

| Layer               | Tools                                      |
| ------------------- | ------------------------------------------ |
| Backend             | Python, FastAPI                            |
| LLM                 | GPT-3.5-turbo via LangChain                |
| Embeddings          | `intfloat/e5-large` (SentenceTransformers) |
| Reranking           | `cross-encoder/ms-marco-MiniLM-L-6-v2`     |
| Vector Store        | FAISS                                      |
| Paper Source        | arXiv API                                  |
| Frontend            | React                                      |
| Graph Visualization | react-force-graph-2d                       |

---

## Getting started

### Backend

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your OpenAI API key
export OPENAI_API_KEY=your_key_here

# Start the API server
uvicorn main:app --reload
```

The API will be live at `http://127.0.0.1:8000`. You can explore the auto-generated docs at `/docs`.

### Frontend

```bash
cd frontend
npm install
npm start
```

The app runs at `http://localhost:3000`.

---

## API endpoints

The backend exposes five endpoints that the frontend calls in sequence, passing results forward through the chain:

```
POST /query/retrieve      { query }                           → papers + summaries
POST /query/gaps          { paper_summaries }                 → research gaps
POST /query/graph         { paper_summaries }                 → knowledge graph
POST /query/experiments   { paper_summaries, research_gaps }  → experiment ideas
POST /query/compare       { paper_summaries }                 → comparison analysis
```

Each endpoint is independent — you can also call them directly if you want to plug just one agent into something else.

---

## How the frontend pipeline works

When you submit a query, the UI enters a pipeline phase where each agent lights up one at a time. The first step also visualizes the data pipeline sub-steps (ArXiv fetch → PDF download → parse → chunk → embed → FAISS index) so you can see what's happening under the hood.

Once all five agents finish, the pipeline collapses into a compact status bar and a tabbed report slides in:

- **Papers** — the retrieved papers with authors, summaries, and PDF links
- **Summary** — the global synthesis plus per-paper accordion summaries
- **Gaps** — LLM-identified research gaps and unexplored directions
- **Graph** — an interactive force-directed knowledge graph (click nodes to zoom)
- **Experiments** — proposed research ideas with difficulty ratings
- **Comparison** — a structured breakdown of similarities, differences, and tradeoffs

---

## Notes

- On first query, the retrieval agent dynamically ingests papers for that topic. Subsequent queries on the same topic skip re-ingestion. The vector index lives in memory for the session, so it resets when the server restarts.
- The system fetches 5 papers per query by default. You can adjust `max_results` in `arxiv_client.py` and the top-k in `retrieval_agent.py`.
- The knowledge graph quality depends heavily on the LLM's ability to extract structured JSON. If it returns malformed output the graph tab will show empty — this is handled gracefully.

---

## Author

Built by **Muhammad Muzzammil**
