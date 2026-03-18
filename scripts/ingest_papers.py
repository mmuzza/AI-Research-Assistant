#  Downloads and indexes papers.

from data_pipeline.pdf_downloader import PDFDownloader
from data_pipeline.arxiv_client import ArxivClient
from data_pipeline.pdf_parser import PDFParser
from data_pipeline.chunking import TextChunker
from embeddings.embedding_model import EmbeddingModel
from vector_store.vector_db import VectorDB

from typing import List



class IngestPapers:

    def __init__(self, vector_db: VectorDB):

        self.arxiv_client = ArxivClient(max_results = 5)
        self.pdf_downloader = PDFDownloader()
        self.pdf_parser = PDFParser()
        self.chunking = TextChunker()
        self.embedding_model = EmbeddingModel()
        self.vector_db = vector_db


    
    def ingest(self, query : str):

        # 1. Get all papers
        papers = self.arxiv_client.search_papers(query)

        all_chunks = []
        all_metadata = []

        for paper in papers:

            try:

                # 2. Download PDF
                pdf_path = self.pdf_downloader.download_pdf(
                    paper["pdf_url"], paper["paper_id"]
                )

                # 3 parse text
                plain_text = self.pdf_parser.extract_text(pdf_path)

                # 4 chunk text
                chunks = self.chunking.chunk_text(plain_text)

                for chunk in chunks:
                    all_chunks.append(chunk)
                    # all_metadata.append({
                    #     "paper_id": paper["paper_id"],
                    #     "title": paper["title"],
                    #     "chunk_text": chunk
                    # })
                    all_metadata.append({
                        "paper_id": paper["paper_id"],
                        "title": paper["title"],
                        "authors": paper["authors"],
                        "published": paper["published"],
                        "chunk_text": chunk,
                        "pdf_url": paper["pdf_url"],
                        "summary": paper["summary"],
                    })
                
            except Exception as e:
                continue
            

        if not all_chunks:
            print("[INFO] No chunks to embed.")
            return


        # 5 embed chunks
        embeddings = self.embedding_model.embed_texts(all_chunks)

        # 6 store in vector db
        self.vector_db.add_embeddings(embeddings, all_metadata)

    def ingest_topic(self, query: str):
        """Ingest papers for a single topic"""
        self.ingest(query)

    def ingest_topics(self, topics: List[str]):
        """Pre-ingest multiple topics"""
        for topic in topics:
            self.ingest(topic)








if __name__ == "__main__":

    vector_db = VectorDB()
    ingestor = IngestPapers(vector_db)


    # ingestor.ingest("transformers")


    topics = [
        "transformers",
        "diffusion models",
        "reinforcement learning"
    ]

    ingestor.ingest_topics(topics)