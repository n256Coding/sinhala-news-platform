from django.db import models

# Create your models here.
class News(models.Model):
    news_id = models.CharField(max_length=50)
    date = models.DateField()
    heading = models.TextField()
    category = models.CharField(max_length=50)
    link_to_source = models.TextField()
