from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.utils import timezone
from datetime import datetime, timedelta

from ..models import (
    Movie,
    Person,
    Genre,
    Review,
    UserMovieInteraction,
    MovieNews,
    StreamingAvailability,
    ContentWarning
)

User = get_user_model()

class MovieViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.genre = Genre.objects.create(name='Action')
        self.movie = Movie.objects.create(
            title='Test Movie',
            imdb_id='tt1234567',
            overview='Test overview',
            release_date='2023-01-01',
            runtime=120,
            age_rating='PG-13'
        )
        self.movie.genres.add(self.genre)

    def test_list_movies(self):
        """Test retrieving a list of movies"""
        url = reverse('movie-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_movie(self):
        """Test retrieving a specific movie"""
        url = reverse('movie-detail', kwargs={'pk': self.movie.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Movie')

    def test_filter_movies_by_genre(self):
        """Test filtering movies by genre"""
        url = reverse('movie-list')
        response = self.client.get(url, {'genre': 'Action'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_search_movies(self):
        """Test searching movies"""
        url = reverse('movie-list')
        response = self.client.get(url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_add_movie_interaction(self):
        """Test adding a movie interaction"""
        url = reverse('movie-add-interaction', kwargs={'pk': self.movie.pk})
        data = {'interaction_type': 'VIEW'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            UserMovieInteraction.objects.filter(
                user=self.user,
                movie=self.movie,
                interaction_type='VIEW'
            ).exists()
        )

    def test_get_similar_movies(self):
        """Test getting similar movies"""
        url = reverse('movie-similar', kwargs={'pk': self.movie.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_movie_analytics(self):
        """Test getting movie analytics"""
        url = reverse('movie-analytics', kwargs={'pk': self.movie.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('view_count', response.data)
        self.assertIn('average_rating', response.data)

class ReviewViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.movie = Movie.objects.create(
            title='Test Movie',
            imdb_id='tt1234567',
            overview='Test overview',
            release_date='2023-01-01',
            runtime=120,
            age_rating='PG-13'
        )

    def test_create_review(self):
        """Test creating a movie review"""
        url = reverse('movie-review-list', kwargs={'movie_pk': self.movie.pk})
        data = {
            'rating': 8,
            'content': 'Great movie!'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)

    def test_like_review(self):
        """Test liking a review"""
        review = Review.objects.create(
            movie=self.movie,
            user=self.user,
            rating=8,
            content='Great movie!'
        )
        url = reverse('review-like', kwargs={
            'movie_pk': self.movie.pk,
            'pk': review.pk
        })
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(review.likes.count(), 1)

    def test_update_review(self):
        """Test updating a review"""
        review = Review.objects.create(
            movie=self.movie,
            user=self.user,
            rating=8,
            content='Original review'
        )
        url = reverse('movie-review-detail', kwargs={
            'movie_pk': self.movie.pk,
            'pk': review.pk
        })
        data = {
            'rating': 9,
            'content': 'Updated review'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        review.refresh_from_db()
        self.assertEqual(review.rating, 9)
        self.assertEqual(review.content, 'Updated review')

class PersonViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.person = Person.objects.create(
            name='John Doe',
            biography='Test biography',
            birth_date='1970-01-01'
        )

    def test_list_people(self):
        """Test retrieving a list of people"""
        url = reverse('person-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_person(self):
        """Test retrieving a specific person"""
        url = reverse('person-detail', kwargs={'pk': self.person.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Doe')

    def test_get_person_filmography(self):
        """Test getting person's filmography"""
        url = reverse('person-filmography', kwargs={'pk': self.person.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('as_actor', response.data)
        self.assertIn('as_director', response.data)

class StreamingAvailabilityViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.movie = Movie.objects.create(
            title='Test Movie',
            imdb_id='tt1234567',
            overview='Test overview',
            release_date='2023-01-01',
            runtime=120,
            age_rating='PG-13'
        )
        self.streaming = StreamingAvailability.objects.create(
            movie=self.movie,
            service='NETFLIX',
            region='US',
            url='https://netflix.com/movie',
            available_from=timezone.now()
        )

    def test_list_streaming_availability(self):
        """Test retrieving streaming availability"""
        url = reverse('movie-streaming-list', kwargs={'movie_pk': self.movie.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['service'], 'NETFLIX')

    def test_filter_by_service(self):
        """Test filtering streaming availability by service"""
        url = reverse('movie-streaming-list', kwargs={'movie_pk': self.movie.pk})
        response = self.client.get(url, {'service': 'NETFLIX'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

class MovieNewsViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.movie = Movie.objects.create(
            title='Test Movie',
            imdb_id='tt1234567',
            overview='Test overview',
            release_date='2023-01-01',
            runtime=120,
            age_rating='PG-13'
        )
        self.news = MovieNews.objects.create(
            movie=self.movie,
            title='Test News',
            content='Test content',
            source_url='https://example.com',
            source_name='Test Source',
            published_at=timezone.now()
        )

    def test_list_movie_news(self):
        """Test retrieving movie news"""
        url = reverse('movie-news-list', kwargs={'movie_pk': self.movie.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test News')

    def test_filter_news_by_date(self):
        """Test filtering news by date"""
        url = reverse('movie-news-list', kwargs={'movie_pk': self.movie.pk})
        today = datetime.now().date().isoformat()
        response = self.client.get(url, {'date': today})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

class ContentWarningViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.movie = Movie.objects.create(
            title='Test Movie',
            imdb_id='tt1234567',
            overview='Test overview',
            release_date='2023-01-01',
            runtime=120,
            age_rating='PG-13'
        )
        self.warning = ContentWarning.objects.create(
            warning_type='VIOLENCE',
            description='Test warning',
            severity=3
        )
        self.movie.content_warnings.add(self.warning)

    def test_list_content_warnings(self):
        """Test retrieving content warnings"""
        url = reverse('content-warning-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_by_warning_type(self):
        """Test filtering content warnings by type"""
        url = reverse('content-warning-list')
        response = self.client.get(url, {'warning_type': 'VIOLENCE'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

class GenreViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.genre = Genre.objects.create(
            name='Action',
            description='Action movies'
        )
        self.movie = Movie.objects.create(
            title='Test Movie',
            imdb_id='tt1234567',
            overview='Test overview',
            release_date='2023-01-01',
            runtime=120,
            age_rating='PG-13'
        )
        self.movie.genres.add(self.genre)

    def test_list_genres(self):
        """Test retrieving genres"""
        url = reverse('genre-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Action')

    def test_get_genre_movies(self):
        """Test getting movies in a genre"""
        url = reverse('genre-movies', kwargs={'pk': self.genre.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Movie')