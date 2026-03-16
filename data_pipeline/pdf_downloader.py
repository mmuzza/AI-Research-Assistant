# We will download the pdf for creating embeddings later on

import requests
from pathlib import Path
from arxiv_client import ArxivClient

class PDFDownloader:

    def __init__(self, save_dir: str = "data/pdfs"):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def download_pdf(self, pdf_url : str, paper_id : str) -> str:
        # Create file path 
        file_path = self.save_dir / f"{paper_id}.pdf" 
        
        if file_path.exists(): 
            return str(file_path) 
            
        
        try: 
            response = requests.get(pdf_url, stream=True) 
            response.raise_for_status() 
            
            with open(file_path, "wb") as f: 
                for chunk in response.iter_content(chunk_size=8192): 
                    if chunk: 
                        f.write(chunk) 
                    
            return str(file_path) 
            
        except requests.RequestException as e: 
            print(f"Failed to download PDF: {pdf_url}") 
            print(e) 
            return ""



## Testing
if __name__ == "__main__":


    client = ArxivClient(max_results=4)
    downloader = PDFDownloader()

    papers = client.search_papers("transformers")

    for paper in papers:
        pdf_path = downloader.download_pdf(
            paper["pdf_url"],
            paper["paper_id"]
        )

        print("Saved to:", pdf_path)