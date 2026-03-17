# import tiktoken
from typing import List
# from pdf_parser import PDFParser

class TextChunker:
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_text(self, pdf_text : str) -> List[str]:
        
        words = pdf_text.split() # helping split in words instead of letters
        step = self.chunk_size - self.overlap

        chunks = []
        for i in range(0, len(words), step):
            chunk_words = words[i:i+self.chunk_size]

            if(len(chunk_words) < self.chunk_size):
                break

            if not chunk_words:
                break

            chunks.append(" ".join(chunk_words))
        
        return chunks


# Testing it works
if __name__ == "__main__":

    parser = PDFParser()
    test_text = parser.extract_all_text("data/pdfs/2603.13098v1.pdf")

    chunk_class = TextChunker()

    chunks_of_text = chunk_class.chunk_text(test_text)
    for chunk in chunks_of_text[:2]:
        print(chunk)
        print("------------------------------------")


    
    