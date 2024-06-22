from django.contrib.auth.models import User

class FeedbackRequest:

    def __init__(self) -> None:
        self.category: str
        self.feedback_type: str
