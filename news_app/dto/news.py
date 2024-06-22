from datetime import datetime


class NewsItem:
    def __init__(self) -> None:
        self.news_id: str
        self.heading: str
        self.content: str
        self.timestamp: datetime
        self.link_to_source: str
        self.category: str
