import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

class Retriever:
    def __init__(self, model_name='all-MiniLM-L6-v2', index_path='teks_index.faiss'):
        self.model = SentenceTransformer(model_name)
        self.index_path = index_path
        self.index = None
        self.load_index()

    def load_index(self):
        try:
            self.index = faiss.read_index(self.index_path)
        except:
            print(f"Index not found at {self.index_path}. A new index will be created when adding data.")

    def encode_teks(self, teks_descriptions):
        return self.model.encode(teks_descriptions)

    def find_similar_questions(self, teks_description, k=5):
        query_vector = self.encode_teks([teks_description])
        if self.index is None:
            raise ValueError("Index is not initialized. Add data to the index first.")
        distances, indices = self.index.search(query_vector, k)
        return indices[0].tolist(), distances[0].tolist()

    def update_index(self, new_teks_descriptions, new_question_ids):
        new_vectors = self.encode_teks(new_teks_descriptions)
        if self.index is None:
            self.index = faiss.IndexFlatL2(new_vectors.shape[1])
        self.index.add(new_vectors)
        faiss.write_index(self.index, self.index_path)

        # In a real-world scenario, you would also need to maintain a mapping
        # between the FAISS indices and the question IDs in a separate data structure

    def add_to_index(self, teks_description, question_id):
        vector = self.encode_teks([teks_description])
        if self.index is None:
            self.index = faiss.IndexFlatL2(vector.shape[1])
        self.index.add(vector)
        faiss.write_index(self.index, self.index_path)

        # Again, in a real-world scenario, you would need to maintain a mapping
        # between the FAISS index and the question ID