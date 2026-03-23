#  5. Proposes experiments.

class ExperimentAgent:
    def __init__(self, llm):
        self.llm = llm

    def generate(self, paper_summaries, research_gaps):
       
        summaries_text = "\n\n".join([
            f"Title: {p.get('title')}\nSummary: {p.get('summary')}"
            for p in paper_summaries
        ])

        gaps_text = ""
        if research_gaps:
            basic = research_gaps.get("basic_gaps", [])
            insights = research_gaps.get("insights", "")
            gaps_text = f"Basic Gaps:\n{basic}\n\nInsights:\n{insights}"

        prompt = f"""
You are an AI research scientist.

Given the following research summaries and identified gaps, propose 3-5 novel experiments or project ideas.

Each idea should include:
- Title
- Description
- Method (how to implement)
- Expected Outcome
- Difficulty (easy, medium, hard)

Research Summaries:
{summaries_text}

Research Gaps:
{gaps_text}

Return the result in JSON format like:
{{
  "ideas": [
    {{
      "title": "...",
      "description": "...",
      "method": "...",
      "expected_outcome": "...",
      "difficulty": "easy"
    }}
  ]
}}
"""

        response = self.llm.invoke(prompt)


        try:
            import json
            return json.loads(response.content)
        except:
            return {"ideas": [], "raw": response.content}