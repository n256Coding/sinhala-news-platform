# Generated by Django 5.0.6 on 2024-08-08 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0003_alter_news_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='abstract',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
