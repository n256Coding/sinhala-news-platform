from rest_framework import serializers
from .dto.feedback_request import FeedbackRequest

class FeedbackRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackRequest
        fields = ('category', 'feedback_type')
