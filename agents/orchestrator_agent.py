class OrchestratorAgent:
    def __init__(self, retrieval_agent, summarizer_agent, research_gap_agent=None, comparison_agent=None):
        self.retrieval_agent = retrieval_agent
        self.summarizer_agent = summarizer_agent
        self.research_gap_agent = research_gap_agent
        self.comparison_agent = comparison_agent

    def run(self, query: str):
        # 1. Retrieve papers ──
        retrieved_chunks = self.retrieval_agent.retrieve(query)


        retrieved_papers = []
        seen_papers = set()
        for chunk in retrieved_chunks:
            paper_id = chunk["paper_id"]
            if paper_id not in seen_papers:
                seen_papers.add(paper_id)
                retrieved_papers.append({
                    "paper_id": paper_id,
                    "title": chunk["title"],
                    "pdf_url": chunk["pdf_url"],
                    "authors": chunk.get("authors"),
                    "published": chunk.get("published").isoformat() if chunk.get("published") else None
                })

        # 2. Summarize papers
        summary = self.summarizer_agent.summarize(retrieved_chunks)
        paper_summaries = summary["paper_summaries"]
        global_summary = summary["global_summary"]

        print("Global summary:", global_summary)

        # 3. Research Gap Analysis
        research_gaps = None
        if self.research_gap_agent and paper_summaries:
            research_gaps = self.research_gap_agent.analyze(paper_summaries)
            print("Research Gaps:", research_gaps)

        # 4. Comparison / insights ──
        comparison_result = None
        if self.comparison_agent and paper_summaries:
            comparison_result = self.comparison_agent.compare(paper_summaries)
            print("Comparison Result:", comparison_result)

        # 5. Final return for frontend ──
        return {
            "retrieved_papers": retrieved_papers,
            "summary": global_summary,
            "paper_summaries": paper_summaries,
            "research_gaps": research_gaps,
            "comparison": comparison_result,
            "status": "done"
        }