from transformers import pipeline
from sinling import SinhalaTokenizer
from sinling import SinhalaStemmer

from news_app.dto.news import NewsItem

class Classifier:

    def __init__(self) -> None:
        self.classifier_local_location = 'temp/models/sinbert-500'
        self.classifier_pipe = pipeline("text-classification", self.classifier_local_location)

    def classify(self, news_list: list[NewsItem]):
        for news in news_list:
            news.content = self.preprocess(news.content)
            prediction = self.classifier_pipe(news.content[:500])
            news.category = prediction[0]['label']

        return news_list
        

    def preprocess(self, news_content: str):
        sinhala_tokenizer = SinhalaTokenizer()
        stemmer = SinhalaStemmer()
        
        tokens = sinhala_tokenizer.tokenize(news_content)
        stemmed = [stemmer.stem(token)[0] for token in tokens]
        
        return ' '.join(stemmed)
    