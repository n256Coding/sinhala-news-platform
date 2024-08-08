# from datetime import datetime
import datetime
import random
import chromadb
from django.shortcuts import render
import logging
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

from news_app.models import News
from recommendation.models import UserFeedback
from recommendation.services.recommendation import to_sentence_embedding
from recommendation.services.vector_db_provider import get_chroma_db_collection
from sinhala_news_platform_backend.settings import MAXIMUM_NO_OF_RANDOM_SUGGESTED_ARTICLES

logger = logging.getLogger(__name__)


def home(request):
    
    # Todays news articles
    todays_news_items: list[News] = News.objects.filter(date__date=datetime.date.today()).all()
    chroma_collection = get_chroma_db_collection()

    current_user = request.user

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
            include=[]
        )
        print(resulted_article_details.get('ids')[0])

        resulted_articles = News.objects.filter(news_id__in=resulted_article_details.get('ids')[0]).all()

        print(resulted_articles)

    
    else:
        # The user seems to be new user or they have never liked/disliked any article before
        # Suggest some random articles
        logger.info('User has not liked any previous articles. Suggesting some random articles.')

        todays_news_items = [news_item for news_item in todays_news_items]

        resulted_articles = random.sample(todays_news_items, MAXIMUM_NO_OF_RANDOM_SUGGESTED_ARTICLES)

        logger.info(resulted_articles)





    # recommended_news_items = []
    # for index, similarity_data_row in categorywise_similarty_data.sort_values(by='liked_count_ratio', ascending=False).iterrows():
    #     category = similarity_data_row['category']
    #     similarity_data: pd.DataFrame = similarity_data_row['similarity_data']
    #     liked_count_ratio = similarity_data_row['liked_count_ratio']

    #     news_items = similarity_data.sort_values(by='similarity_score', ascending=False).iloc[:int(liked_count_ratio)]['news_item'].tolist()
    #     recommended_news_items += news_items
    
    render_context = {
        "news_item_list": resulted_articles,
        "extra_news_list": todays_news_items
    }

    return render(request, 'news_app/home.html', render_context)
