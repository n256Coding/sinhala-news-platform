from pathlib import Path
import pickle
from django.shortcuts import render, HttpResponse
import logging
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

from news_app.services.classifier import Classifier
from news_app.services.spider import Spider
from recommendation.models import UserFeedback
from recommendation.services.recommendation import to_sentence_embedding

logger = logging.getLogger(__name__)


def home(request):
    spider = Spider()
    classifier = Classifier()
    
    cache_file_path_str = 'temp/news_cache.pkl'
    cache_file = Path(cache_file_path_str)
    if cache_file.is_file():
        # file exists, load the data from cache
        news_list = pickle.load(open(cache_file_path_str, 'rb'))
        logger.info('News data loaded from cache.')

    else:
        news_list = spider.crowl_todays()
        pickle.dump(news_list, open(cache_file_path_str, 'wb+'))
        logger.info('Caching the news data')

    classified_news_list = classifier.classify(news_list)

    current_user = request.user

    # Load previously liked news (from News)
    user_feedbacks = UserFeedback.objects.filter(user=current_user).all()
    user_feedbacks_df = UserFeedback.to_pandas(user_feedbacks)

    categorywise_user_feedbacks_df = user_feedbacks_df.groupby(by='category')[['user']].count()
    print(categorywise_user_feedbacks_df)

    df_field_categories = []
    df_field_liked_counts = []
    df_field_similarity_data = []
    for category, row in categorywise_user_feedbacks_df.iterrows():
        liked_count = row['user']
        # news_item = user_feedbacks_df[user_feedbacks_df['category'] == category]['news_item'].tolist()
        
        # Get sentence embeddings of previously liked news
        liked_sentence_embeddings = []
        for user_feedback in [item for item in user_feedbacks if item.news_item.category == category]:
            news_item = user_feedback.news_item
            heading = news_item.heading

            heading_embedding = to_sentence_embedding(heading)
            liked_sentence_embeddings.append(heading_embedding)

        # Get sentence embeddings of current news
        current_sentence_embeddings = []
        categorywise_classified_news_list = [item for item in classified_news_list if item.category == category]
        for current_news in categorywise_classified_news_list:
            heading = current_news.heading

            heading_embedding = to_sentence_embedding(heading)
            current_sentence_embeddings.append(heading_embedding)

        # Find most similar between previously liked news sentence embeddings and new news sentence embeddings
        similarity_scores = []
        for current_sentence_embedding in current_sentence_embeddings:

            liked_data_similarity = []
            for liked_sentence_embedding in liked_sentence_embeddings:
                similarity_score = cosine_similarity(liked_sentence_embedding.reshape(-1, 1), current_sentence_embedding.reshape(-1, 1))
                liked_data_similarity.append(similarity_score)
                # print(similarity_score)

            overall_similarity = np.mean(liked_data_similarity)
            similarity_scores.append(overall_similarity)

        df_field_categories.append(category)
        df_field_liked_counts.append(liked_count)
        df_field_similarity_data.append(pd.DataFrame({
            'similarity_score': similarity_scores,
            'news_item': categorywise_classified_news_list
        }))
    
    categorywise_similarty_data = pd.DataFrame({
        'category': df_field_categories,
        'liked_count': df_field_liked_counts,
        'similarity_data': df_field_similarity_data
    })

    categorywise_similarty_data['liked_count_ratio'] = (categorywise_similarty_data['liked_count'] / len(categorywise_similarty_data.index)) * len(classified_news_list)

    print(categorywise_similarty_data)
    # categorywise_similarty_data.sort_values(by='liked_count', ascending=False)

    # recommended_news_items = recommendation_result.sort_values(by='similarity_score', ascending=False).head(10)['news_item'].values
    # for recommended_news_item in recommended_news_items:
    #     print(recommended_news_item.heading)

    recommended_news_items = []
    for index, similarity_data_row in categorywise_similarty_data.sort_values(by='liked_count_ratio', ascending=False).iterrows():
        category = similarity_data_row['category']
        similarity_data: pd.DataFrame = similarity_data_row['similarity_data']
        liked_count_ratio = similarity_data_row['liked_count_ratio']

        news_items = similarity_data.sort_values(by='similarity_score', ascending=False).iloc[:int(liked_count_ratio)]['news_item'].tolist()
        recommended_news_items += news_items
    
    render_context = {
        "news_item_list": recommended_news_items,
        "extra_news_list": classified_news_list
    }

    return render(request, 'news_app/home.html', render_context)
