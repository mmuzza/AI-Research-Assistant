#  3. Compares different methods.

class ComparisonAgent:
    def __init__(self, llm):
        self.llm = llm

    def compare(self, paper_summaries):
        combined = "\n\n".join([
            f"{p['title']}:\n{p['summary']}"
            for p in paper_summaries
        ])

        prompt = f"""
        Compare the following research papers.

        Identify:
        - Key similarities
        - Key differences
        - Tradeoffs between approaches
        - Which paper is best for what use-case

        Papers:
        {combined}
        """

        response = self.llm.invoke(prompt)

        # return {
        #     "comparison": response.content
        # }
        return response.content


# Testing
if __name__ == "__main__":
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    agent = ComparisonAgent(llm)

    # Made up data...
    paper_summaries = [
        {
            "title": "Diffusion Models for Reasoning",
            "summary": "This paper explores using diffusion models to perform multi-step reasoning tasks."
        },
        {
            "title": "Chain-of-Thought Prompting",
            "summary": "This paper uses transformer-based models with chain-of-thought prompting to improve reasoning."
        }
    ]

    result = agent.compare(paper_summaries)

    print("\n=== Comparison results: ===\n")
    print(result["comparison"])