import datetime
from logging import Logger
import random

import chromadb
import pandas as pd
from news_app.dto.news import NewsItem
from news_app.models import News
from recommendation.models import UserFeedback
from sinling import SinhalaTokenizer
import numpy as np
from gensim.models import FastText

from recommendation.services.vector_db_provider import get_chroma_db_collection
from sinhala_news_platform_backend.settings import MAXIMUM_NO_OF_SUGGESTED_ARTICLES

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

def get_recommended_articles(todays_news_items, logger: Logger, current_user):

    chroma_collection = get_chroma_db_collection()

    # Load previously liked news (from News)
    user_feedbacks = UserFeedback.objects.filter(user=current_user).all()

    # News articles that the user has liked before
    liked_news_items: list[News] = [user_feedback.news_item for user_feedback in user_feedbacks]

    if liked_news_items:

        # There are some pre liked items available, proceed with them
        print('Like history found. Recommendation processing...')

        liked_articles_details: chromadb.GetResult = chroma_collection.get(
            ids=[liked_new_item.news_id for liked_new_item in liked_news_items],
            include=['embeddings']
        )
        
        liked_embddings: list = liked_articles_details.get('embeddings')

        resulted_article_details: chromadb.QueryResult = chroma_collection.query(
            query_embeddings=liked_embddings,
            n_results=5,
            where={'timestamp': {'$gte': datetime.datetime.combine(datetime.datetime.today(), datetime.time.min).timestamp()}},
            include=['distances']
        )
        ids = []
        distances = []
        for resulted_article_detail_ids in resulted_article_details.get('ids'):
            ids.extend(resulted_article_detail_ids)
        for resulted_article_detail_distances in resulted_article_details.get('distances'):
            distances.extend(resulted_article_detail_distances)

        article_details_df = pd.DataFrame({
            'id': ids,
            'distances': distances
        })
        article_details_df = article_details_df.sort_values(by='distances', ascending=False).head(MAXIMUM_NO_OF_SUGGESTED_ARTICLES)
        
        resulted_articles = News.objects.filter(news_id__in=article_details_df['id'].values).all()
    
    else:
        # The user seems to be new user or they have never liked/disliked any article before
        # Suggest some random articles
        logger.info('User has not liked any previous articles. Suggesting some random articles.')

        todays_news_items = [news_item for news_item in todays_news_items]

        resulted_articles = random.sample(todays_news_items, MAXIMUM_NO_OF_SUGGESTED_ARTICLES)

        logger.info(resulted_articles)

    return resulted_articles
