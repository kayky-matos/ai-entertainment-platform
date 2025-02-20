from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from ..models import (
    Movie,
    Person,
    Genre,
    Review,
    UserMovieInteraction,
    StreamingAvailability
)
from ..services import (
    SentimentAnalysisService,
    RecommendationService,
    StreamingAvailabilityService
)

User = get_user_model()


class SentimentAnalysisServiceTests(TestCase):
    def setUp(self):
        self.service = SentimentAnalysisService()
        self.positive_text = "This movie was absolutely amazing! Loved every minute."
        self.negative_text = "Terrible movie, complete waste of time."
        self.neutral_text = "The movie was okay, had some good and bad moments."

    @patch('transformers.pipeline')
    def test_analyze_positive_sentiment(self, mock_pipeline):
        """Test analyzing positive sentiment"""
        mock_analyzer = MagicMock()
        mock_analyzer.return_value = [{'label': 'POSITIVE', 'score': 0.95}]
        mock_pipeline.return_value = mock_analyzer

        score = self.service.analyze_text(self.positive_text)
        self.assertGreater(score, 0.8)
        mock_analyzer.assert_called_once_with(self.positive_text)

    @patch('transformers.pipeline')
    def test_analyze_negative_sentiment(self, mock_pipeline):
        """Test analyzing negative sentiment"""
        mock_analyzer = MagicMock()
        mock_analyzer.return_value = [{'label': 'NEGATIVE', 'score': 0.85}]
        mock_pipeline.return_value = mock_analyzer

        score = self.service.analyze_text(self.negative_text)
        self.assertLess(score, 0.3)
        mock_analyzer.assert_called_once_with(self.negative_text)

    @patch('transformers.pipeline')
    def test_batch_analyze_sentiment(self, mock_pipeline):
        """Test batch sentiment analysis"""
        mock_analyzer = MagicMock()
        mock_analyzer.side_effect = [
            [{'label': 'POSITIVE', 'score': 0.9}],
            [{'label': 'NEGATIVE', 'score': 0.8}],
            [{'label': 'POSITIVE', 'score': 0.6}]
        ]
        mock_pipeline.return_value = mock_analyzer

        texts = [self.positive_text, self.negative_text, self.neutral_text]
        scores = self.service.batch_analyze(texts)

        self.assertEqual(len(scores), 3)
        self.assertGreater(scores[0], scores[1])  # Positive > Negative
        mock_analyzer.assert_called()

    def test_sentiment_caching(self):
        """Test that sentiment analysis results are cached"""
        with patch('django.core.cache.cache.get') as mock_cache_get:
            with patch('django.core.cache.cache.set') as mock_cache_set:
                mock_cache_get.return_value = None

                self.service.analyze_text(self.positive_text)
                mock_cache_get.assert_called_once()
                mock_cache_set.assert_called_once()


class RecommendationServiceTests(TestCase):
    def setUp(self):
        self.service = RecommendationService()

        # Create test data
        self.genre1 = Genre.objects.create(name="Action")
        self.genre2 = Genre.objects.create(name="Drama")

        self.director = Person.objects.create(
            name="John Director",
            biography="Test director"
        )

        self.actor = Person.objects.create(
            name="Jane Actor",
            biography="Test actor"
        )

        # Create test movies
        self.movie1 = Movie.objects.create(
            title="Test Movie 1",
            overview="Action packed movie",
            release_date="2023-01-01",
            runtime=120,
            age_rating="PG-13"
        )
        self.movie1.genres.add(self.genre1)

        self.movie2 = Movie.objects.create(
            title="Test Movie 2",
            overview="Drama movie",
            release_date="2023-02-01",
            runtime=110,
            age_rating="PG-13"
        )
        self.movie2.genres.add(self.genre2)

        # Create test user and interactions
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    def test_get_movie_features(self):
        """Test extracting movie features"""
        features = self.service._get_movie_features(self.movie1)
        self.assertIn(self.movie1.title, features)
        self.assertIn(self.movie1.overview, features)
        self.assertIn(self.genre1.name, features)

    def test_calculate_content_similarity(self):
        """Test content-based similarity calculation"""
        similar_movies = self.service._calculate_content_similarity(self.movie1)
        self.assertIsInstance(similar_movies, list)
        self.assertLess(len(similar_movies), 2)  # Should only have movie2

    def test_calculate_collaborative_similarity(self):
        """Test collaborative filtering similarity"""
        # Create some user interactions
        UserMovieInteraction.objects.create(
            user=self.user,
            movie=self.movie1,
            interaction_type="VIEW"
        )
        UserMovieInteraction.objects.create(
            user=self.user,
            movie=self.movie2,
            interaction_type="FAVORITE"
        )

        similar_movies = self.service._calculate_collaborative_similarity(self.movie1)
        self.assertIn(self.movie2, similar_movies)

    def test_get_personalized_recommendations(self):
        """Test getting personalized recommendations"""
        # Create user interactions
        UserMovieInteraction.objects.create(
            user=self.user,
            movie=self.movie1,
            interaction_type="VIEW"
        )

        recommendations = self.service.get_personalized_recommendations(self.user.id)
        self.assertIsInstance(recommendations, list)
        self.assertLess(len(recommendations), 2)

    def test_recommendation_caching(self):
        """Test that recommendations are cached"""
        with patch('django.core.cache.cache.get') as mock_cache_get:
            with patch('django.core.cache.cache.set') as mock_cache_set:
                mock_cache_get.return_value = None

                self.service.get_similar_movies(self.movie1)
                mock_cache_get.assert_called_once()
                mock_cache_set.assert_called_once()


class StreamingAvailabilityServiceTests(TestCase):
    def setUp(self):
        self.service = StreamingAvailabilityService()
        self.movie = Movie.objects.create(
            title="Test Movie",
            imdb_id="tt1234567",
            overview="Test movie",
            release_date="2023-01-01",
            runtime=120,
            age_rating="PG-13"
        )

    @patch('requests.get')
    def test_fetch_justwatch_data(self, mock_get):
        """Test fetching data from JustWatch API"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'offers': [{
                'provider_id': 'NETFLIX',
                'country': 'US',
                'urls': {'standard_web': 'https://netflix.com'},
                'retail_price': None,
                'presentation_type': 'HD'
            }]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        data = self.service._fetch_justwatch_data(self.movie)
        self.assertIsNotNone(data)
        self.assertIn('offers', data)
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_fetch_reelgood_data(self, mock_get):
        """Test fetching data from Reelgood API"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'sources': [{
                'source': 'NETFLIX',
                'region': 'US',
                'web_url': 'https://netflix.com',
                'quality': 'HD'
            }]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        data = self.service._fetch_reelgood_data(self.movie)
        self.assertIsNotNone(data)
        self.assertIn('sources', data)
        mock_get.assert_called_once()

    @patch.object(StreamingAvailabilityService, '_fetch_justwatch_data')
    @patch.object(StreamingAvailabilityService, '_fetch_reelgood_data')
    def test_update_streaming_availability(self, mock_reelgood, mock_justwatch):
        """Test updating streaming availability"""
        mock_justwatch.return_value = {
            'offers': [{
                'provider_id': 'NETFLIX',
                'country': 'US',
                'urls': {'standard_web': 'https://netflix.com'},
                'retail_price': None,
                'presentation_type': 'HD'
            }]
        }
        mock_reelgood.return_value = None

        availabilities = self.service.update_streaming_availability(self.movie)
        self.assertEqual(len(availabilities), 1)
        self.assertEqual(availabilities[0].service, 'NETFLIX')

    def test_get_movie_availability(self):
        """Test getting current streaming availability"""
        # Create test streaming availability
        StreamingAvailability.objects.create(
            movie=self.movie,
            service='NETFLIX',
            region='US',
            url='https://netflix.com',
            available_from=timezone.now()
        )

        availabilities = self.service.get_movie_availability(self.movie)
        self.assertEqual(len(availabilities), 1)
        self.assertEqual(availabilities[0].service, 'NETFLIX')

    def test_availability_update_threshold(self):
        """Test that availability is updated when data is stale"""
        old_date = timezone.now() - timedelta(days=2)
        StreamingAvailability.objects.create(
            movie=self.movie,
            service='NETFLIX',
            region='US',
            url='https://netflix.com',
            available_from=old_date,
            updated_at=old_date
        )

        with patch.object(StreamingAvailabilityService, 'update_streaming_availability') as mock_update:
            mock_update.return_value = []
            self.service.get_movie_availability(self.movie)
            mock_update.assert_called_once_with(self.movie)