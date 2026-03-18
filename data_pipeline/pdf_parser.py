#  Extracting text from the pdf so that we can leave out images and tables and be able to create embeddings.


from pypdf import PdfReader
import re

class PDFParser:

    def __init__(self):
        pass

    @staticmethod
    def clean_text(pdf_text: str) -> str:
        """
        Cleans raw PDF text for chunking and embeddings:
        """

        text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", pdf_text)

        text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

        text = re.sub(r"\s+", " ", text)

        text = text.strip()

        return text
    
    def extract_text(self, pdf_path: str) -> str:
        
        pdf_text = ""

        reader = PdfReader(pdf_path)

        # for page in reader.pages:
        #     text = page.extract_text()
        #     if text:
        #         pdf_text += text + "\n"

        pdf_text = "\n".join((page.extract_text() or "").strip() for page in reader.pages)

        return self.clean_text(pdf_text)
        # return pdf_text


if __name__ == "__main__":


    parser = PDFParser()

    test_text = parser.extract_text("data/pdfs/2603.13098v1.pdf")
    print(test_text[:500])
    print(test_text[:500])