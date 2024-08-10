from numpy import ndarray
from sentence_transformers import SentenceTransformer
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import os

print(f'Working dir: {os.getcwd()}')

sentence_bert_model = SentenceTransformer('Ransaka/sinhala-roberta-sentence-transformer')
with open('temp/models/xgboost/tfidf_vectorizer.pkl', 'rb') as f:
    tfidf_vectorizer: TfidfVectorizer = pickle.load(f)

print('-- It is loaded again ---------------------------')


def get_embeddings(text_documents: list[str]):
    return sentence_bert_model.encode(text_documents)

def get_embedding(text_document: str) -> ndarray:
    return sentence_bert_model.encode(text_document)

def get_tfidf_embeddings(text_documents: list[str]):
    return tfidf_vectorizer.transform(text_documents)
