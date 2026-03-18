
from sentence_transformers import SentenceTransformer
from typing import List

from data_pipeline.pdf_parser import PDFParser
from data_pipeline.chunking import TextChunker

class EmbeddingModel:

    def __init__(self, model_name : str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, chunks : List[str]):

        embeddings = None
        embeddings = self.model.encode(chunks)

        return embeddings.astype("float32")



if __name__ == "__main__":

    parser = PDFParser()
    test_text = parser.extract_all_text("data/pdfs/2603.13098v1.pdf")

    chunk_class = TextChunker()
    chunks_of_text = chunk_class.chunk_text(test_text)
    
    embed = EmbeddingModel()
    embeds = embed.embed_texts(chunks_of_text)
    
    for emb in embeds[:2]:
        print(emb)
        print("------------------------------------")

