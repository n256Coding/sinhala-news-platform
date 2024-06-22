from news_app.dto.news import NewsItem


def get_content_based_recommendations(user_id, user_likes: dict, articles: list[NewsItem], num_recommendations=2):
    # Get the user's preferences
    user_preferences = user_likes.get(user_id, {})
    
    # Score each article based on the user's preferences
    article_scores = []
    for article in articles:
        category = article.category
        score = user_preferences.get(category, 0)
        article_scores.append((score, article.content))
    
    # Sort articles by score and get the top recommendations
    article_scores.sort(reverse=True, key=lambda x: x[0])
    recommended_articles = [article for score, article in article_scores[:num_recommendations]]
    return recommended_articles
