# Generated by Django 5.0.6 on 2024-06-22 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='news_id',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
    ]