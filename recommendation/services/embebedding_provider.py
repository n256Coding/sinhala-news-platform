from numpy import ndarray
from sentence_transformers import SentenceTransformer
from gensim.models import FastText
import gensim

model = SentenceTransformer('Ransaka/sinhala-roberta-sentence-transformer')
print('-- It is loaded again ---------------------------')

def get_transformer_embeddings(text_documents: list[str]):
    return model.encode(text_documents)

def get_transformer_embedding(text_document: str) -> ndarray:
    return model.encode(text_document)

def get_fasttext_embedding(text_document: list[str]):
    fasttext_model: gensim.models.fasttext.FastText = FastText.load('saved-models/fasttext.model')
    fasttext_model.wv.get_sentence_vector(text_document)
