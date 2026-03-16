#  Extracting text from the pdf so that we can leave out images and tables and be able to create embeddings.


from pypdf import PdfReader

class PDFParser:

    def __init__(self):
        pass

    
    def extract_all_text(self, pdf_path: str) -> str:
        
        pdf_text = ""

        reader = PdfReader(pdf_path)

        # for page in reader.pages:
        #     text = page.extract_text()
        #     if text:
        #         pdf_text += text + "\n"

        pdf_text = "\n".join((page.extract_text() or "").strip() for page in reader.pages)

        return pdf_text


if __name__ == "__main__":


    parser = PDFParser()

    test_text = parser.extract_all_text("data/pdfs/2603.13098v1.pdf")
    print(test_text[:500])


