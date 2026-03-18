#  2. Summarizes each paper.

class VectorDB:
    def __init__(self, embedding_dim=384, use_cosine: bool = True):
 
        self.embedding_dim = embedding_dim
        self.use_cosine = use_cosine

        self.index = faiss.IndexIDMap(faiss.IndexFlatL2(embedding_dim))
        self.metadata = []
        self.id_counter = 0 

# class VectorDB:
#     def __init__(self, embedding_dim=384, use_cosine: bool = True):
 
#         self.embedding_dim = embedding_dim
#         self.use_cosine = use_cosine

#         self.index = faiss.IndexIDMap(faiss.IndexFlatL2(embedding_dim))
#         self.metadata = []
#         self.id_counter = 0 
# class VectorDB:
#     def __init__(self, embedding_dim=384, use_cosine: bool = True):
 
#         self.embedding_dim = embedding_dim
#         self.use_cosine = use_cosine

#         self.index = faiss.IndexIDMap(faiss.IndexFlatL2(embedding_dim))
#         self.metadata = []
#         self.id_counter = 0 # class VectorDB:
#     def __init__(self, embedding_dim=384, use_cosine: bool = True):
 
#         self.embedding_dim = embedding_dim
#         self.use_cosine = use_cosine

#         self.index = faiss.IndexIDMap(faiss.IndexFlatL2(embedding_dim))
#         self.metadata = []
#         self.id_counter = 0 # class VectorDB:
#     def __init__(self, embedding_dim=384, use_cosine: bool = True):
 
#         self.embedding_dim = embedding_dim
#         self.use_cosine = use_cosine

#         self.index = faiss.IndexIDMap(faiss.IndexFlatL2(embedding_dim))
#         self.metadata = []
#         self.id_counter = 0 