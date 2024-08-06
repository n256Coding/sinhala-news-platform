from transformers import pipeline
from sinling import SinhalaTokenizer
from sinling import SinhalaStemmer

from news_app.dto.news import NewsItem
from news_app.models import News

class Classifier:

    def __init__(self) -> None:
        self.classifier_local_location = 'temp/models/sinbert-500'
        self.classifier_pipe = pipeline("text-classification", self.classifier_local_location)
        self.content_max_length = 500

    def classify_and_save(self, news_list: list[NewsItem]) -> list[NewsItem]:
        for news in news_list:
            
            saved_object = News.objects.filter(news_id=news.news_id).first()
            if not saved_object:
                news.content = self.preprocess(news.content)
                prediction = self.classifier_pipe(news.content[:self.content_max_length])
                news.category = prediction[0]['label']

                # Save to database
                news_store = News()
                news_store.news_id = news.news_id
                news_store.heading = news.heading
                news_store.category = news.category
                news_store.link_to_source = news.link_to_source
                news_store.date = news.timestamp

                news_store.save()

            else:
                news.category = saved_object.category

        return news_list
    
    def classify(self, news_list: list[NewsItem]) -> list[NewsItem]:
        preprocessed_news_content_list = [self.preprocess(news_item.content[:self.content_max_length]) for news_item in news_list]
        predictions = self.classifier_pipe(preprocessed_news_content_list)

        for i, prediction in enumerate(predictions):
            news_list[i].category = prediction['label']

        return news_list
        

    def preprocess(self, news_content: str):
        sinhala_tokenizer = SinhalaTokenizer()
        stemmer = SinhalaStemmer()
        
        tokens = sinhala_tokenizer.tokenize(news_content)
        stemmed = [stemmer.stem(token)[0] for token in tokens]
        
        return ' '.join(stemmed)
    