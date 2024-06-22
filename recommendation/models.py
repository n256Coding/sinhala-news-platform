from django.db import models
from django.contrib.auth.models import User

class UserFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    feedback = models.JSONField()
