from pathlib import Path
import pickle
from django.shortcuts import render, HttpResponse
import logging

from news_app.services.classifier import Classifier
from news_app.services.spider import Spider

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

    return render(request, 'home.html', {"news_item_list": classified_news_list})
