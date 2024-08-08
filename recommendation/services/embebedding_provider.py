from numpy import ndarray
from sentence_transformers import SentenceTransformer


model = SentenceTransformer('Ransaka/sinhala-roberta-sentence-transformer')
print('-- It is loaded again ---------------------------')

def get_embeddings(text_documents: list[str]):
    return model.encode(text_documents)

def get_embedding(text_document: str) -> ndarray:
    return model.encode(text_document)
