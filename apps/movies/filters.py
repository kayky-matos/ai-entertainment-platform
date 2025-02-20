from django.db.models import Q, Avg, Count
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Movie,
    Person,
    Genre,
    ContentWarning,
    Review,
    UserMovieInteraction,
    MovieNews,
    StreamingAvailability
)
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    PersonSerializer,
    GenreSerializer,
    ContentWarningSerializer,
    ReviewSerializer,
    ReviewCreateUpdateSerializer,
    UserMovieInteractionSerializer,
    MovieNewsSerializer,
    StreamingAvailabilitySerializer
)
from .filters import MovieFilter
from .permissions import IsOwnerOrReadOnly
from .services import (
    SentimentAnalysisService,
    RecommendationService,
    StreamingAvailabilityService
)


class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet for movies with various actions and filtering capabilities.
    """
    queryset = Movie.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MovieFilter
    search_fields = ['title', 'original_title', 'overview']
    ordering_fields = ['release_date', 'imdb_rating', 'rotten_tomatoes_score']
    ordering = ['-release_date']

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        return MovieDetailSerializer

    def get_queryset(self):
        queryset = Movie.objects.prefetch_related(
            'genres',
            'content_warnings',
            'directors',
            'cast',
            'streaming_availability',
            'reviews',
            'news'
        )

        # Filter by genre
        genre = self.request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(genres__name__iexact=genre)

        # Filter by release year
        year = self.request.query_params.get('year')
        if year:
            queryset = queryset.filter(release_date__year=year)

        # Filter by content rating
        rating = self.request.query_params.get('rating')
        if rating:
            queryset = queryset.filter(age_rating=rating)

        # Filter by streaming service
        service = self.request.query_params.get('service')
        if service:
            queryset = queryset.filter(
                streaming_availability__service=service,
                streaming_availability__available_until__gte=timezone.now()
            )

        return queryset

    @action(detail=True, methods=['post'])
    def add_interaction(self, request, pk=None):
        """Add a user interaction (view, wishlist, favorite, rate)"""
        movie = self.get_object()
        serializer = UserMovieInteractionSerializer(
            data=request.data,
            context={'request': request, 'movie': movie}
        )

        if serializer.is_valid():
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_interaction(self, request, pk=None):
        """Remove a user interaction"""
        movie = self.get_object()
        interaction_type = request.data.get('interaction_type')

        interaction = get_object_or_404(
            UserMovieInteraction,
            user=request.user,
            movie=movie,
            interaction_type=interaction_type
        )
        interaction.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True)
    def similar(self, request, pk=None):
        """Get similar movies based on various factors"""
        movie = self.get_object()
        recommendation_service = RecommendationService()
        similar_movies = recommendation_service.get_similar_movies(movie)

        serializer = MovieListSerializer(similar_movies, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def streaming_availability(self, request, pk=None):
        """Get up-to-date streaming availability information"""
        movie = self.get_object()
        service = StreamingAvailabilityService()
        availability = service.get_movie_availability(movie)

        serializer = StreamingAvailabilitySerializer(availability, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        """Create a review for the movie"""
        movie = self.get_object()
        serializer = ReviewCreateUpdateSerializer(
            data=request.data,
            context={'request': request, 'movie': movie}
        )

        if serializer.is_valid():
            review = serializer.save()

            # Perform sentiment analysis on the review
            sentiment_service = SentimentAnalysisService()
            sentiment_score = sentiment_service.analyze_text(review.content)
            review.sentiment_score = sentiment_score
            review.save()

            return Response(
                ReviewSerializer(review).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for actors, directors, and other crew members.
    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'biography']

    @action(detail=True)
    def filmography(self, request, pk=None):
        """Get person's complete filmography"""
        person = self.get_object()
        acted_movies = person.acted_movies.all()
        directed_movies = person.directed_movies.all()

        return Response({
            'as_actor': MovieListSerializer(acted_movies, many=True).data,
            'as_director': MovieListSerializer(directed_movies, many=True).data
        })


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for movie genres.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    @action(detail=True)
    def movies(self, request, pk=None):
        """Get all movies in a specific genre"""
        genre = self.get_object()
        movies = genre.movies.all()

        # Use the filter backend for additional filtering
        filtered_movies = MovieFilter(
            request.GET,
            queryset=movies
        ).qs

        serializer = MovieListSerializer(filtered_movies, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for movie reviews with like/unlike functionality.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(
            movie_id=self.kwargs['movie_pk']
        ).select_related('user').prefetch_related('likes')

    @action(detail=True, methods=['post'])
    def like(self, request, movie_pk=None, pk=None):
        """Like or unlike a review"""
        review = self.get_object()
        user = request.user

        if review.likes.filter(id=user.id).exists():
            review.likes.remove(user)
            return Response({'status': 'unliked'})
        else:
            review.likes.add(user)
            return Response({'status': 'liked'})


class MovieNewsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for movie-related news.
    """
    serializer_class = MovieNewsSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['published_at']
    ordering = ['-published_at']

    def get_queryset(self):
        if 'movie_pk' in self.kwargs:
            return MovieNews.objects.filter(movie_id=self.kwargs['movie_pk'])
        return MovieNews.objects.all()


class ContentWarningViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for content warnings.
    """
    queryset = ContentWarning.objects.all()
    serializer_class = ContentWarningSerializer


class StreamingAvailabilityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for streaming availability information.
    """
    serializer_class = StreamingAvailabilitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['service', 'region']

    def get_queryset(self):
        return StreamingAvailability.objects.filter(
            movie_id=self.kwargs['movie_pk']
        )