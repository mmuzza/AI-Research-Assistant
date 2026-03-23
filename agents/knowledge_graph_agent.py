class KnowledgeGraphAgent:
    def __init__(self, llm):
        self.llm = llm

    def build_graph(self, paper_summaries):
        summaries_text = "\n\n".join([
            f"Title: {p.get('title')}\nSummary: {p.get('summary')}"
            for p in paper_summaries
        ])

        prompt = f"""
Extract a knowledge graph from the following research summaries.

Identify:
1. Key entities (models, methods, datasets, concepts)
2. Relationships between them

Return ONLY valid JSON in this format:

{{
  "nodes": [
    {{ "id": "entity_name", "type": "concept|model|method|dataset" }}
  ],
  "edges": [
    {{ "source": "entity1", "target": "entity2", "relation": "uses|improves|compares|based_on" }}
  ]
}}

Research Summaries:
{summaries_text}
"""

        response = self.llm.invoke(prompt)

        try:
            import json
            return json.loads(response.content)
        except:
            return {"nodes": [], "edges": [], "raw": response.content}