from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .views import (
    MovieViewSet,
    PersonViewSet,
    GenreViewSet,
    ReviewViewSet,
    MovieNewsViewSet,
    ContentWarningViewSet,
    StreamingAvailabilityViewSet
)

# Create a router for main viewsets
router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'people', PersonViewSet, basename='person')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'content-warnings', ContentWarningViewSet, basename='content-warning')

# Create nested routers for movie-related resources
movies_router = routers.NestedDefaultRouter(router, r'movies', lookup='movie')
movies_router.register(r'reviews', ReviewViewSet, basename='movie-review')
movies_router.register(r'news', MovieNewsViewSet, basename='movie-news')
movies_router.register(
    r'streaming',
    StreamingAvailabilityViewSet,
    basename='movie-streaming'
)

# URL patterns including both main and nested routes
urlpatterns = [
    # Main router URLs
    path('', include(router.urls)),

    # Nested router URLs
    path('', include(movies_router.urls)),

    # Custom action URLs for movies
    path(
        'movies/<int:pk>/recommend/',
        MovieViewSet.as_view({'get': 'recommend'}),
        name='movie-recommend'
    ),
    path(
        'movies/<int:pk>/similar/',
        MovieViewSet.as_view({'get': 'similar'}),
        name='movie-similar'
    ),

    # Streaming availability routes
    path(
        'movies/<int:pk>/streaming/update/',
        MovieViewSet.as_view({'post': 'update_streaming'}),
        name='movie-update-streaming'
    ),

    # Review interaction routes
    path(
        'movies/<int:movie_pk>/reviews/<int:pk>/like/',
        ReviewViewSet.as_view({'post': 'like'}),
        name='review-like'
    ),
    path(
        'movies/<int:movie_pk>/reviews/<int:pk>/unlike/',
        ReviewViewSet.as_view({'post': 'unlike'}),
        name='review-unlike'
    ),

    # User interaction routes
    path(
        'movies/<int:pk>/interact/',
        MovieViewSet.as_view({'post': 'add_interaction'}),
        name='movie-interact'
    ),
    path(
        'movies/<int:pk>/remove-interaction/',
        MovieViewSet.as_view({'post': 'remove_interaction'}),
        name='movie-remove-interaction'
    ),

    # Person-related routes
    path(
        'people/<int:pk>/filmography/',
        PersonViewSet.as_view({'get': 'filmography'}),
        name='person-filmography'
    ),
    path(
        'people/<int:pk>/movies/',
        PersonViewSet.as_view({'get': 'movies'}),
        name='person-movies'
    ),

    # Genre-related routes
    path(
        'genres/<int:pk>/movies/',
        GenreViewSet.as_view({'get': 'movies'}),
        name='genre-movies'
    ),

    # Search routes
    path(
        'search/movies/',
        MovieViewSet.as_view({'get': 'search'}),
        name='movie-search'
    ),
    path(
        'search/people/',
        PersonViewSet.as_view({'get': 'search'}),
        name='person-search'
    ),

    # Analytics routes
    path(
        'movies/<int:pk>/analytics/',
        MovieViewSet.as_view({'get': 'analytics'}),
        name='movie-analytics'
    ),
    path(
        'genres/analytics/',
        GenreViewSet.as_view({'get': 'analytics'}),
        name='genre-analytics'
    ),

    # Content warning routes
    path(
        'movies/<int:pk>/warnings/',
        MovieViewSet.as_view({'get': 'warnings'}),
        name='movie-warnings'
    ),
    path(
        'movies/<int:pk>/add-warning/',
        MovieViewSet.as_view({'post': 'add_warning'}),
        name='movie-add-warning'
    ),

    # News routes
    path(
        'movies/<int:pk>/latest-news/',
        MovieViewSet.as_view({'get': 'latest_news'}),
        name='movie-latest-news'
    ),

    # Recommendation routes
    path(
        'movies/trending/',
        MovieViewSet.as_view({'get': 'trending'}),
        name='movies-trending'
    ),
    path(
        'movies/upcoming/',
        MovieViewSet.as_view({'get': 'upcoming'}),
        name='movies-upcoming'
    ),
    path(
        'movies/popular/',
        MovieViewSet.as_view({'get': 'popular'}),
        name='movies-popular'
    ),
    path(
        'movies/top-rated/',
        MovieViewSet.as_view({'get': 'top_rated'}),
        name='movies-top-rated'
    ),

    # User personalization routes
    path(
        'movies/recommended/',
        MovieViewSet.as_view({'get': 'recommended'}),
        name='movies-recommended'
    ),
    path(
        'movies/watchlist/',
        MovieViewSet.as_view({'get': 'watchlist'}),
        name='movies-watchlist'
    ),
    path(
        'movies/favorites/',
        MovieViewSet.as_view({'get': 'favorites'}),
        name='movies-favorites'
    ),

    # Export routes
    path(
        'movies/<int:pk>/export/',
        MovieViewSet.as_view({'get': 'export'}),
        name='movie-export'
    ),
    path(
        'people/<int:pk>/export/',
        PersonViewSet.as_view({'get': 'export'}),
        name='person-export'
    ),
]

# API documentation patterns
api_documentation_patterns = [
    path('schema/', include('rest_framework.urls')),
]

urlpatterns += api_documentation_patterns