'''
RAG PIPELINE:
-------------

User query
↓
embed query
↓
search vector DB
↓
retrieve relevant chunks
↓
send to LLM
↓
generate answer
'''


class RAGPipeline:

    def __init__(self, vector_db, embedding_model, llm):
        self.vector_db = vector_db
        self.embedding_model = embedding_model
        self.llm = llm

    def query(self, question: str):
        
        # Creating the entire pipeline:
        # Step 1: embed query

        # Step 2: retrieve relevant chunks

        # Step 3: build prompt

        # Step 4: generate answer

        answer = ""

        return answer
