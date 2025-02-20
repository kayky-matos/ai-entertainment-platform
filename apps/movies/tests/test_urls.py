from django.test import TestCase
from django.urls import reverse, resolve
from ..views import (
    MovieViewSet,
    PersonViewSet,
    GenreViewSet,
    ReviewViewSet,
    MovieNewsViewSet,
    ContentWarningViewSet,
    StreamingAvailabilityViewSet
)

class UrlsTests(TestCase):
    def test_movie_list_url(self):
        """Test movie list URL"""
        url = reverse('movie-list')
        self.assertEqual(resolve(url).func.cls, MovieViewSet)

    def test_movie_detail_url(self):
        """Test movie detail URL"""
        url = reverse('movie-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, MovieViewSet)

    def test_person_list_url(self):
        """Test person list URL"""
        url = reverse('person-list')
        self.assertEqual(resolve(url).func.cls, PersonViewSet)

    def test_person_detail_url(self):
        """Test person detail URL"""
        url = reverse('person-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, PersonViewSet)

    def test_genre_list_url(self):
        """Test genre list URL"""
        url = reverse('genre-list')
        self.assertEqual(resolve(url).func.cls, GenreViewSet)

    def test_genre_detail_url(self):
        """Test genre detail URL"""
        url = reverse('genre-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, GenreViewSet)

    def test_review_list_url(self):
        """Test review list URL"""
        url = reverse('movie-review-list', kwargs={'movie_pk': 1})
        self.assertEqual(resolve(url).func.cls, ReviewViewSet)

    def test_review_detail_url(self):
        """Test review detail URL"""
        url = reverse('movie-review-detail', kwargs={'movie_pk': 1, 'pk': 1})
        self.assertEqual(resolve(url).func.cls, ReviewViewSet)

    def test_movie_news_list_url(self):
        """Test movie news list URL"""
        url = reverse('movie-news-list', kwargs={'movie_pk': 1})
        self.assertEqual(resolve(url).func.cls, MovieNewsViewSet)

    def test_streaming_availability_list_url(self):
        """Test streaming availability list URL"""
        url = reverse('movie-streaming-list', kwargs={'movie_pk': 1})
        self.assertEqual(resolve(url).func.cls, StreamingAvailabilityViewSet)

    def test_content_warning_list_url(self):
        """Test content warning list URL"""
        url = reverse('content-warning-list')
        self.assertEqual(resolve(url).func.cls, ContentWarningViewSet)

    def test_movie_similar_url(self):
        """Test movie similar URL"""
        url = reverse('movie-similar', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, MovieViewSet)

    def test_movie_recommend_url(self):
        """Test movie recommend URL"""
        url = reverse('movie-recommend', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, MovieViewSet)

    def test_movie_analytics_url(self):
        """Test movie analytics URL"""
        url = reverse('movie-analytics', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, MovieViewSet)

    def test_person_filmography_url(self):
        """Test person filmography URL"""
        url = reverse('person-filmography', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, PersonViewSet)

    def test_person_movies_url(self):
        """Test person movies URL"""
        url = reverse('person-movies', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, PersonViewSet)

    def test_genre_movies_url(self):
        """Test genre movies URL"""
        url = reverse('genre-movies', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, GenreViewSet)

    def test_movie_search_url(self):
        """Test movie search URL"""
        url = reverse('movie-search')
        self.assertEqual(resolve(url).func.cls, MovieViewSet)

    def test_person_search_url(self):
        """Test person search URL"""
        url = reverse('person-search')
        self.assertEqual(resolve(url).func.cls, PersonViewSet)

    def test_genre_analytics_url(self):
        """Test genre analytics URL"""
        url = reverse('genre-analytics')
        self.assertEqual(resolve(url).func.cls, GenreViewSet)

    def test_movie_warnings_url(self):
        """Test movie warnings URL"""
        url = reverse('movie-warnings', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, MovieViewSet)

    def test_movie_add_warning_url(self):
        """Test movie add warning URL"""
        url = reverse('movie-add-warning', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, MovieViewSet)

    def test_movie_latest_news_url(self):
        """Test movie latest news URL"""
        url = reverse('movie-latest-news', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, MovieViewSet)

    def test_movies_trending_url(self):
        """Test trending movies URL"""
        url = reverse('movies-trending')
        self.assertEqual(resolve(url).func.cls, MovieViewSet)

    def test_movies_upcoming_url(self):
        """Test upcoming movies URL"""
        url = reverse('movies-upcoming')
        self.assertEqual(resolve(url).func.cls, MovieViewSet)

    def test_movies_popular_url(self):
        """Test popular movies URL"""
        url = reverse('movies-popular')
        self.assertEqual(resolve(url).func.cls, MovieViewSet)

    def test_movies_top_rated_url(self):
        """Test top rated movies URL"""
        url = reverse('movies-top-rated')
        self.assertEqual(resolve(url).func.cls, MovieViewSet)

    def test_movies_recommended_url(self):
        """Test recommended movies URL"""
        url = reverse('movies-recommended')
        self.assertEqual(resolve(url).func.cls, MovieViewSet)

    def test_movies_watchlist_url(self):
        """Test watchlist URL"""
        url = reverse('movies-watchlist')
        self.assertEqual(resolve(url).func.cls, MovieViewSet)

    def test_movies_favorites_url(self):
        """Test favorites URL"""
        url = reverse('movies-favorites')
        self.assertEqual(resolve(url).func.cls, MovieViewSet)

    def test_movie_export_url(self):
        """Test movie export URL"""
        url = reverse('movie-export', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, MovieViewSet)

    def test_person_export_url(self):
        """Test person export URL"""
        url = reverse('person-export', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, PersonViewSet)

    def test_review_like_url(self):
        """Test review like URL"""
        url = reverse('review-like', kwargs={'movie_pk': 1, 'pk': 1})
        self.assertEqual(resolve(url).func.cls, ReviewViewSet)

    def test_review_unlike_url(self):
        """Test review unlike URL"""
        url = reverse('review-unlike', kwargs={'movie_pk': 1, 'pk': 1})
        self.assertEqual(resolve(url).func.cls, ReviewViewSet)

    def test_movie_interact_url(self):
        """Test movie interaction URL"""
        url = reverse('movie-interact', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, MovieViewSet)

    def test_movie_remove_interaction_url(self):
        """Test remove movie interaction URL"""
        url = reverse('movie-remove-interaction', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, MovieViewSet)

    def test_url_names_unique(self):
        """Test that all URL names are unique"""
        url_names = [
            'movie-list', 'movie-detail', 'person-list', 'person-detail',
            'genre-list', 'genre-detail', 'movie-review-list', 'movie-review-detail',
            'movie-news-list', 'movie-streaming-list', 'content-warning-list',
            'movie-similar', 'movie-recommend', 'movie-analytics', 'person-filmography',
            'person-movies', 'genre-movies', 'movie-search', 'person-search',
            'genre-analytics', 'movie-warnings', 'movie-add-warning',
            'movie-latest-news', 'movies-trending', 'movies-upcoming',
            'movies-popular', 'movies-top-rated', 'movies-recommended',
            'movies-watchlist', 'movies-favorites', 'movie-export',
            'person-export', 'review-like', 'review-unlike', 'movie-interact',
            'movie-remove-interaction'
        ]
        self.assertEqual(len(url_names), len(set(url_names)), "URL names must be unique")