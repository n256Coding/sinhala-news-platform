from news_app.dto.news import NewsItem
from recommendation.models import UserFeedback
from sinling import SinhalaTokenizer
import numpy as np
from gensim.models import FastText

sinhala_tokenizer = SinhalaTokenizer()
wv_model = FastText.load('temp/word2vec/fasttext.model')
vector_size = 100

# def get_content_based_recommendations(user_id, articles: list[NewsItem], num_recommendations=2):

#     user_feedback_record = UserFeedback.objects.filter(user__pk = user_id).first()


#     # Score each article based on the user's preferences
#     article_scores = []
#     for article in articles:
#         category = article.category
#         score = user_preferences.get(category, 0)
#         article_scores.append((score, article.content))
    
#     # Sort articles by score and get the top recommendations
#     article_scores.sort(reverse=True, key=lambda x: x[0])
#     recommended_articles = [article for score, article in article_scores[:num_recommendations]]
#     return recommended_articles

def to_sentence_embedding(sentence: str):
    # tokenized_sentence = sinhala_tokenizer.tokenize(sentence)
    # embeddings = [w2v_model.wv[word] if word in w2v_model.wv else np.zeros(vector_size) for word in tokenized_sentence]
    # sentence_vector = np.mean(embeddings, axis=0)

    # return sentence_vector

    return wv_model.wv.get_sentence_vector(sentence)
