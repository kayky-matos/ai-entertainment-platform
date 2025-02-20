import numpy as np
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import requests
from django.conf import settings
from django.core.cache import cache
from django.db.models import Q, Count, Avg
from transformers import pipeline
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from .models import Movie, Review, StreamingAvailability, UserMovieInteraction


class SentimentAnalysisService:
    """
    Service for analyzing sentiment in movie reviews using transformers.
    """

    def __init__(self):
        self.model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        self._sentiment_analyzer = None

    @property
    def sentiment_analyzer(self):
        if self._sentiment_analyzer is None:
            self._sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                device=-1  # CPU
            )
        return self._sentiment_analyzer

    def analyze_text(self, text: str) -> float:
        """
        Analyze the sentiment of a given text and return a score between 0 and 1.

        Args:
            text (str): The text to analyze

        Returns:
            float: Sentiment score (0 to 1, where 1 is most positive)
        """
        # Cache key for sentiment analysis
        cache_key = f"sentiment_{hash(text)}"
        cached_result = cache.get(cache_key)

        if cached_result is not None:
            return cached_result

        try:
            # Perform sentiment analysis
            result = self.sentiment_analyzer(text)[0]

            # Convert to score between 0 and 1
            score = result['score'] if result['label'] == 'POSITIVE' else 1 - result['score']

            # Cache the result for 24 hours
            cache.set(cache_key, score, 86400)

            return score
        except Exception as e:
            print(f"Error in sentiment analysis: {str(e)}")
            return 0.5  # Neutral sentiment as fallback

    def batch_analyze(self, texts: List[str]) -> List[float]:
        """
        Analyze sentiment for multiple texts in batch.

        Args:
            texts (List[str]): List of texts to analyze

        Returns:
            List[float]: List of sentiment scores
        """
        return [self.analyze_text(text) for text in texts]


class RecommendationService:
    """
    Service for generating movie recommendations using collaborative and content-based filtering.
    """

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english'
        )

    def _get_movie_features(self, movie: Movie) -> str:
        """
        Create a feature string for a movie combining various attributes.
        """
        features = [
            movie.title,
            movie.overview,
            ' '.join(g.name for g in movie.genres.all()),
            ' '.join(d.director.name for d in movie.directors.all()),
            ' '.join(c.person.name for c in movie.cast.all()[:5])
        ]
        return ' '.join(features)

    def _calculate_content_similarity(self, movie: Movie, n: int = 10) -> List[Movie]:
        """
        Calculate content-based similarity using TF-IDF and cosine similarity.
        """
        # Cache key for content-based recommendations
        cache_key = f"content_recommendations_{movie.id}"
        cached_results = cache.get(cache_key)

        if cached_results is not None:
            return Movie.objects.filter(id__in=cached_results)

        # Get all movies and their features
        movies = Movie.objects.all()
        movie_features = [self._get_movie_features(m) for m in movies]

        # Calculate TF-IDF matrix
        tfidf_matrix = self.vectorizer.fit_transform(movie_features)

        # Calculate similarity scores
        movie_idx = list(movies).index(movie)
        similarity_scores = cosine_similarity(
            tfidf_matrix[movie_idx:movie_idx + 1],
            tfidf_matrix
        )[0]

        # Get indices of most similar movies
        similar_indices = similarity_scores.argsort()[::-1][1:n + 1]
        similar_movie_ids = [movies[i].id for i in similar_indices]

        # Cache results for 24 hours
        cache.set(cache_key, similar_movie_ids, 86400)

        return Movie.objects.filter(id__in=similar_movie_ids)

    def _calculate_collaborative_similarity(self, movie: Movie, n: int = 10) -> List[Movie]:
        """
        Calculate collaborative filtering recommendations based on user interactions.
        """
        # Find users who interacted with this movie
        user_interactions = UserMovieInteraction.objects.filter(
            movie=movie,
            interaction_type__in=['VIEW', 'FAVORITE', 'RATE']
        ).values_list('user_id', flat=True)

        # Find other movies these users interacted with
        similar_movies = Movie.objects.filter(
            usermovieinteraction__user_id__in=user_interactions
        ).exclude(
            id=movie.id
        ).annotate(
            interaction_count=Count('usermovieinteraction')
        ).order_by('-interaction_count')[:n]

        return similar_movies

    def get_similar_movies(self, movie: Movie, n: int = 10) -> List[Movie]:
        """
        Get similar movies using a hybrid approach combining content-based and collaborative filtering.
        """
        # Get recommendations from both approaches
        content_based = set(self._calculate_content_similarity(movie, n))
        collaborative = set(self._calculate_collaborative_similarity(movie, n))

        # Combine results with preference to movies that appear in both sets
        combined = list(content_based & collaborative)  # Movies in both sets
        combined.extend(list(content_based - set(combined)))  # Add remaining content-based
        combined.extend(list(collaborative - set(combined)))  # Add remaining collaborative

        return combined[:n]

    def get_personalized_recommendations(self, user_id: int, n: int = 10) -> List[Movie]:
        """
        Get personalized movie recommendations for a user.
        """
        # Get user's recent interactions
        recent_interactions = UserMovieInteraction.objects.filter(
            user_id=user_id
        ).order_by('-created_at')[:5]

        recommendations = []
        for interaction in recent_interactions:
            similar_movies = self.get_similar_movies(interaction.movie, n=5)
            recommendations.extend(similar_movies)

        # Remove duplicates and movies the user has already interacted with
        seen_movies = UserMovieInteraction.objects.filter(
            user_id=user_id
        ).values_list('movie_id', flat=True)

        unique_recommendations = []
        seen_ids = set(seen_movies)

        for movie in recommendations:
            if movie.id not in seen_ids and movie not in unique_recommendations:
                unique_recommendations.append(movie)
                if len(unique_recommendations) >= n:
                    break

        return unique_recommendations


class StreamingAvailabilityService:
    """
    Service for managing and updating streaming availability information.
    """

    def __init__(self):
        self.justwatch_api_key = settings.JUSTWATCH_API_KEY
        self.reelgood_api_key = settings.REELGOOD_API_KEY
        self.base_url = "https://api.justwatch.com/content/titles/movie"

    def _fetch_justwatch_data(self, movie: Movie) -> Optional[Dict]:
        """
        Fetch streaming data from JustWatch API.
        """
        try:
            response = requests.get(
                f"{self.base_url}/{movie.imdb_id}/locale/en_US",
                headers={"Authorization": f"Bearer {self.justwatch_api_key}"}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching JustWatch data: {str(e)}")
            return None

    def _fetch_reelgood_data(self, movie: Movie) -> Optional[Dict]:
        """
        Fetch streaming data from Reelgood API.
        """
        try:
            response = requests.get(
                f"https://api.reelgood.com/v1/movie/{movie.imdb_id}/availability",
                headers={"Authorization": f"Bearer {self.reelgood_api_key}"}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching Reelgood data: {str(e)}")
            return None

    def update_streaming_availability(self, movie: Movie) -> List[StreamingAvailability]:
        """
        Update streaming availability information for a movie.
        """
        # Fetch data from both APIs
        justwatch_data = self._fetch_justwatch_data(movie)
        reelgood_data = self._fetch_reelgood_data(movie)

        # Combine and normalize the data
        streaming_info = []

        if justwatch_data:
            for offer in justwatch_data.get('offers', []):
                streaming_info.append({
                    'service': offer['provider_id'],
                    'region': offer['country'],
                    'url': offer['urls']['standard_web'],
                    'price': offer.get('retail_price'),
                    'quality': offer.get('presentation_type'),
                    'available_from': offer.get('valid_from'),
                    'available_until': offer.get('valid_until')
                })

        if reelgood_data:
            for source in reelgood_data.get('sources', []):
                # Only add if not already present from JustWatch
                if not any(s['service'] == source['source'] and
                           s['region'] == source['region'] for s in streaming_info):
                    streaming_info.append({
                        'service': source['source'],
                        'region': source['region'],
                        'url': source['web_url'],
                        'price': source.get('price'),
                        'quality': source.get('quality'),
                        'available_from': source.get('available_from'),
                        'available_until': source.get('available_until')
                    })

        # Update database
        current_time = datetime.now()
        updated_availabilities = []

        for info in streaming_info:
            availability, created = StreamingAvailability.objects.update_or_create(
                movie=movie,
                service=info['service'],
                region=info['region'],
                defaults={
                    'url': info['url'],
                    'price': info['price'],
                    'quality': info['quality'],
                    'available_from': info.get('available_from', current_time),
                    'available_until': info.get('available_until')
                }
            )
            updated_availabilities.append(availability)

        # Remove outdated entries
        StreamingAvailability.objects.filter(
            movie=movie
        ).exclude(
            id__in=[a.id for a in updated_availabilities]
        ).delete()

        return updated_availabilities

    def get_movie_availability(self, movie: Movie) -> List[StreamingAvailability]:
        """
        Get current streaming availability for a movie.
        """
        # Check if we need to update the data
        last_updated = StreamingAvailability.objects.filter(
            movie=movie
        ).order_by('-updated_at').first()

        if not last_updated or \
                datetime.now() - last_updated.updated_at > timedelta(hours=24):
            # Update if data is more than 24 hours old
            return self.update_streaming_availability(movie)

        return StreamingAvailability.objects.filter(
            movie=movie,
            available_until__isnull=True
        ).order_by('service', 'region')