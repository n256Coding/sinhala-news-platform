import datetime
import random
import chromadb
from django.shortcuts import render
import logging
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from news_app.dto.news import NewsItem
from news_app.models import News
from news_app.services.classifier import Classifier
from recommendation.models import UserFeedback
from recommendation.services.vector_db_provider import get_chroma_db_collection
from sinhala_news_platform_backend.settings import MAXIMUM_NO_OF_SUGGESTED_ARTICLES

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

    
    render_context = {
        "news_item_list": resulted_articles,
        "extra_news_list": todays_news_items
    }

    return render(request, 'news_app/home.html', render_context)

@api_view(['POST'])
def classify_article(request: Request):

    print(request.data)

    news_document = request.data.get('news_document')
    model_type = request.data.get('model_type')

    classifer = Classifier()
    if model_type == 'light':
        predicted_label = classifer.xgb_classify(news_document)

    else: # 'heavy'
        news_item = NewsItem()
        news_item.content = news_document
        predicted_items = classifer.bert_classify([news_item])

        predicted_label = predicted_items[0].category

    return Response({
        'category': predicted_label
    })
