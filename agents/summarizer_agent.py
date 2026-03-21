from typing import List, Dict
from collections import defaultdict

class SummarizerAgent:
    def __init__(self, llm):
        self.llm = llm
    
    
    # Helper function to sort papers based on their id
    def group_by_paper(self, chunks: List[Dict]) -> Dict[str, List[Dict]]:
        paper_dict = defaultdict(list)
        for chunk in chunks:
            paper_dict[chunk["paper_id"]].append(chunk)
        return paper_dict

    # Helper function used by summarize_paper function
    def rank_chunks(self, chunks: List[Dict], top_k: int = 5) -> List[Dict]:
        # lower distance = more relevant
        sorted_chunks = sorted(chunks, key=lambda x: x["distance"])
        return sorted_chunks[:top_k]
    

    def summarize_paper(self, paper_chunks: List[Dict]) -> Dict:
        if not paper_chunks:
            return {}

        # Rank chunks
        top_chunks = self.rank_chunks(paper_chunks)

        # Combine chunk text
        combined_text = "\n\n".join([
            f"{c['title']} ({c['authors'][0]}): {c['chunk_text']}"
            for c in top_chunks
        ])

        prompt = f"""
        Summarize this research paper. Focus on:
        - Key contributions
        - Methods
        - Results

        Content:
        {combined_text}
        """

        # summary = self.llm.predict(prompt)
        response = self.llm.invoke(prompt)
        summary = response.content

        return {
            "paper_id": paper_chunks[0]["paper_id"],
            "title": paper_chunks[0]["title"],
            "authors": paper_chunks[0]["authors"],
            "published": paper_chunks[0]["published"],
            "pdf_url": paper_chunks[0]["pdf_url"],
            "summary": summary
        }

    
    def summarize_global(self, paper_summaries: List[Dict]) -> Dict:
        combined = "\n\n".join([
            f"{p['title']}: {p['summary']}"
            for p in paper_summaries
        ])

        prompt = f"""
        Given multiple research paper summaries, produce:
        1. A concise overall summary
        2. Key trends across papers
        3. Important differences if any

        Summaries:
        {combined}
        """

        # response = self.llm.predict(prompt)
        response = self.llm.invoke(prompt)
        summary = response.content

        return {
            # "global_summary": response
            "global_summary": summary
        }

    

    # Main pipeline
    def summarize(self, retrieved_chunks: List[Dict]) -> Dict:
        # Group
        paper_dict = self.group_by_paper(retrieved_chunks)

        # Summarize each paper
        paper_summaries = []
        for _, chunks in paper_dict.items():
            summary = self.summarize_paper(chunks)
            if summary:
                paper_summaries.append(summary)

        # Global summary
        global_summary = self.summarize_global(paper_summaries)

        return {
            "paper_summaries": paper_summaries,
            "global_summary": global_summary["global_summary"]
        }


if __name__ == "__main__":
    from agents.retrieval_agent import RetrievalAgent
    from vector_store.vector_db import VectorDB
    from embeddings.embedding_model import EmbeddingModel
    # from langchain.chat_models import ChatOpenAI
    from langchain_openai import ChatOpenAI

    vector_db = VectorDB()
    embedding_model = EmbeddingModel()
    retrieval_agent = RetrievalAgent(vector_db, embedding_model)

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    summarizer = SummarizerAgent(llm)

    query = "diffusion models reasoning"
    chunks = retrieval_agent.retrieve(query, k=10)

    result = summarizer.summarize(chunks)

    print("\n=== Global summary: ===")
    print(result["global_summary"])

    print("\n=== Paper summaries: ===")
    for p in result["paper_summaries"]:
        print(f"\n📄 {p['title']}")
        print(p["summary"][:300])