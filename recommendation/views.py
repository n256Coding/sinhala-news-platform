from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view

from recommendation.models import UserFeedback

@api_view(['POST'])
def get_user_feedback(request: Request):
    print(dir(request))

    user = request.user

    print(request.data)
    category = request.data.get('category')
    feedback_type = request.data.get('feedback_type')

    feedback_record = UserFeedback.objects.filter(user=user).first()
    if not feedback_record:
        feedback_record = UserFeedback()
        feedback_record.user = user
        feedback_record.feedback = {category: 1 if feedback_type == 'positive' else -1}
    
    else:
        feedback_json = feedback_record.feedback
        if feedback_json.get(category):
            feedback_json[category] = feedback_json[category] + (1 if feedback_type == 'positive' else -1)
        else:
            feedback_json[category] = (1 if feedback_type == 'positive' else -1)

        feedback_record.feedback = feedback_json
    
    feedback_record.save()

    return Response()
