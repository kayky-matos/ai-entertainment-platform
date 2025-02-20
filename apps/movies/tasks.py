from celery import shared_task
from datetime import datetime, timedelta
from django.db.models import Q
from django.core.cache import cache
from django.conf import settings

from .models import (
    Movie,
    Review,
    StreamingAvailability,
    MovieNews,
    UserMovieInteraction
)
from .services import (
    SentimentAnalysisService,
    RecommendationService,
    StreamingAvailabilityService
)


@shared_task
def update_movie_streaming_availability(movie_id: int = None):
    """
    Update streaming availability information for movies.
    If movie_id is provided, update only that movie;
    otherwise, update all movies with stale data.
    """
    streaming_service = StreamingAvailabilityService()

    if movie_id:
        try:
            movie = Movie.objects.get(id=movie_id)
            streaming_service.update_streaming_availability(movie)
        except Movie.DoesNotExist:
            return f"Movie with id {movie_id} not found"
    else:
        # Update movies with stale streaming data (older than 24 hours)
        stale_cutoff = datetime.now() - timedelta(hours=24)
        movies = Movie.objects.filter(
            Q(streaming_availability__isnull=True) |
            Q(streaming_availability__updated_at__lt=stale_cutoff)
        ).distinct()

        for movie in movies:
            streaming_service.update_streaming_availability(movie)

    return "Streaming availability update completed"


@shared_task
def analyze_review_sentiment(review_id: int):
    """
    Analyze the sentiment of a newly created or updated review.
    """
    try:
        review = Review.objects.get(id=review_id)
        sentiment_service = SentimentAnalysisService()

        # Analyze sentiment
        sentiment_score = sentiment_service.analyze_text(review.content)

        # Update review with sentiment score
        review.sentiment_score = sentiment_score
        review.save(update_fields=['sentiment_score'])

        # Update movie's average sentiment cache
        cache_key = f"movie_sentiment_{review.movie_id}"
        cache.delete(cache_key)

        return f"Sentiment analysis completed for review {review_id}"
    except Review.DoesNotExist:
        return f"Review with id {review_id} not found"


@shared_task
def batch_analyze_reviews(movie_id: int = None):
    """
    Perform sentiment analysis on multiple reviews.
    If movie_id is provided, analyze only that movie's reviews;
    otherwise, analyze all reviews without sentiment scores.
    """
    sentiment_service = SentimentAnalysisService()

    # Get reviews without sentiment scores
    reviews_query = Review.objects.filter(sentiment_score__isnull=True)
    if movie_id:
        reviews_query = reviews_query.filter(movie_id=movie_id)

    reviews = reviews_query[:100]  # Process in batches of 100

    if not reviews:
        return "No reviews to analyze"

    # Analyze sentiments in batch
    review_texts = [review.content for review in reviews]
    sentiment_scores = sentiment_service.batch_analyze(review_texts)

    # Update reviews with sentiment scores
    for review, score in zip(reviews, sentiment_scores):
        review.sentiment_score = score

    Review.objects.bulk_update(reviews, ['sentiment_score'])

    # Clear relevant caches
    if movie_id:
        cache.delete(f"movie_sentiment_{movie_id}")

    return f"Batch sentiment analysis completed for {len(reviews)} reviews"


@shared_task
def update_movie_recommendations():
    """
    Update cached recommendations for all movies.
    This is a computationally intensive task that should be run during off-peak hours.
    """
    recommendation_service = RecommendationService()
    movies = Movie.objects.all()

    for movie in movies:
        # Calculate similar movies
        similar_movies = recommendation_service.get_similar_movies(movie)

        # Cache the results
        cache_key = f"movie_recommendations_{movie.id}"
        cache.set(
            cache_key,
            [m.id for m in similar_movies],
            timeout=86400  # Cache for 24 hours
        )

    return f"Updated recommendations for {len(movies)} movies"


@shared_task
def update_user_recommendations(user_id: int):
    """
    Update personalized recommendations for a specific user.
    """
    recommendation_service = RecommendationService()

    # Get personalized recommendations
    recommendations = recommendation_service.get_personalized_recommendations(user_id)

    # Cache the results
    cache_key = f"user_recommendations_{user_id}"
    cache.set(
        cache_key,
        [m.id for m in recommendations],
        timeout=3600  # Cache for 1 hour
    )

    return f"Updated recommendations for user {user_id}"


@shared_task
def cleanup_old_interactions():
    """
    Remove old user interactions to prevent database bloat.
    Keeps the most recent interactions for each user-movie pair.
    """
    # Keep only the latest interaction of each type for each user-movie pair
    for interaction_type, _ in UserMovieInteraction.INTERACTION_TYPES:
        # Get the latest interaction for each user-movie pair
        latest_interactions = UserMovieInteraction.objects.filter(
            interaction_type=interaction_type
        ).values(
            'user_id',
            'movie_id'
        ).annotate(
            latest_id=models.Max('id')
        )

        # Delete all interactions except the latest ones
        UserMovieInteraction.objects.filter(
            interaction_type=interaction_type
        ).exclude(
            id__in=[item['latest_id'] for item in latest_interactions]
        ).delete()

    return "Cleaned up old user interactions"


@shared_task
def fetch_movie_news():
    """
    Fetch and update movie news from various sources.
    Implement web scraping or API calls to news sources.
    """
    # This is a placeholder for implementing news fetching logic
    # You would typically integrate with news APIs or implement web scraping here
    return "Movie news update completed"


@shared_task
def cleanup_stale_data():
    """
    Perform various cleanup tasks to maintain database health.
    """
    # Remove expired streaming availability entries
    StreamingAvailability.objects.filter(
        available_until__lt=datetime.now()
    ).delete()

    # Archive old news items
    archive_date = datetime.now() - timedelta(days=30)
    MovieNews.objects.filter(
        published_at__lt=archive_date
    ).update(
        archived=True
    )

    # Clear old cache entries
    cache.clear()

    return "Stale data cleanup completed"


@shared_task
def generate_movie_statistics():
    """
    Generate and cache various statistics for movies.
    """
    movies = Movie.objects.all()

    for movie in movies:
        stats = {
            'average_rating': movie.reviews.aggregate(avg_rating=models.Avg('rating'))['avg_rating'],
            'review_count': movie.reviews.count(),
            'view_count': movie.usermovieinteraction_set.filter(interaction_type='VIEW').count(),
            'favorite_count': movie.usermovieinteraction_set.filter(interaction_type='FAVORITE').count(),
            'available_platforms': movie.streaming_availability.count(),
        }

        # Cache the statistics
        cache_key = f"movie_stats_{movie.id}"
        cache.set(cache_key, stats, timeout=3600)  # Cache for 1 hour

    return "Movie statistics updated"