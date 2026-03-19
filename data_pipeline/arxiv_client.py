# This file helps fetches papers from arxiv.


import arxiv
from typing import List, Dict


class ArxivClient:

    def __init__(self, max_results : int = 10):
        self.max_results = max_results
        self.client = arxiv.Client()

    
    def search_papers(self, query : str, max_results=None) -> List[Dict]:

        max_results = max_results or self.max_results
        papers = []

        search = arxiv.Search(
            query=query,
            max_results= max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        for result in self.client.results(search):

            paper = {
                "paper_id": result.get_short_id(),
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "summary": result.summary,
                "published": result.published,
                "pdf_url": result.pdf_url,
                "entry_id": result.entry_id
            }

            papers.append(paper)


        return papers



## testing
if __name__ == "__main__":

    client = ArxivClient(max_results=3)

    papers = client.search_papers("transformers")

    for paper in papers:
        print(paper["title"])
        print(paper["authors"])
        print(paper["pdf_url"])
        print("-" * 40)