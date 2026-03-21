from collections import defaultdict

class ResearchGapAgent:

    def __init__(self, llm):
        self.llm = llm

    def extract_signals(self, paper_summaries):
        structured = []

        for p in paper_summaries:
            text = (p.get("summary") or "").lower()

            structured.append({
                "title": p["title"],
                "method": self.detect_method(text),
                "task": self.detect_task(text),
                "keywords": self.extract_keywords(text)
            })

        return structured

    def detect_method(self, text):
        if "diffusion" in text:
            return "diffusion"
        if "transformer" in text:
            return "transformer"
        if "reinforcement" in text:
            return "reinforcement learning"
        return "other"

    def detect_task(self, text):
        if "reasoning" in text:
            return "reasoning"
        if "vision" in text:
            return "vision"
        if "language" in text:
            return "nlp"
        return "other"

    def extract_keywords(self, text):
        return list(set(text.split()))[:10]


    def group_papers(self, structured):
        groups = defaultdict(list)

        for p in structured:
            key = f"{p['method']} | {p['task']}"
            groups[key].append(p)

        return groups


    def detect_basic_gaps(self, groups):
        gaps = []

        methods = set()
        tasks = set()

        for key in groups:
            method, task = key.split(" | ")
            methods.add(method)
            tasks.add(task)

        for m in methods:
            for t in tasks:
                combo = f"{m} | {t}"
                if combo not in groups:
                    gaps.append(f"No papers found for {m} applied to {t}")

        return gaps


    def build_prompt(self, groups, basic_gaps):
        return f"""
        You are a research scientist.

        Research clusters:
        {groups}

        Detected gaps:
        {basic_gaps}

        Analyze:
        - deeper research gaps
        - limitations
        - new research ideas
        """

    def analyze(self, paper_summaries):
        structured = self.extract_signals(paper_summaries)
        groups = self.group_papers(structured)
        basic_gaps = self.detect_basic_gaps(groups)

        prompt = self.build_prompt(groups, basic_gaps)
        response = self.llm.invoke(prompt)

        return {
            "basic_gaps": basic_gaps,
            "insights": response.content
        }


if __name__ == "__main__":
    from langchain_openai import ChatOpenAI


    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    agent = ResearchGapAgent(llm)

    paper_summaries = [
        {
            "title": "Diffusion Models for Reasoning",
            "summary": "This paper explores diffusion models applied to reasoning tasks..."
        },
        {
            "title": "Transformers in Vision",
            "summary": "We use transformer architectures for vision tasks..."
        }
    ]

    result = agent.analyze(paper_summaries)

    print("\n Research Gap: =====\n")
    print(result)