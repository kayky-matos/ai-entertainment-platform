from rest_framework import serializers
from .models import (
    Person,
    Genre,
    ContentWarning,
    Movie,
    MovieDirector,
    MovieCast,
    Review,
    UserMovieInteraction,
    MovieNews,
    StreamingAvailability
)


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ContentWarningSerializer(serializers.ModelSerializer):
    warning_type_display = serializers.CharField(source='get_warning_type_display', read_only=True)

    class Meta:
        model = ContentWarning
        fields = ['id', 'warning_type', 'warning_type_display', 'description', 'severity']


class MovieCastSerializer(serializers.ModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = MovieCast
        fields = ['id', 'person', 'character_name', 'order']


class MovieDirectorSerializer(serializers.ModelSerializer):
    director = PersonSerializer()

    class Meta:
        model = MovieDirector
        fields = ['id', 'director', 'role']


class StreamingAvailabilitySerializer(serializers.ModelSerializer):
    service_display = serializers.CharField(source='get_service_display', read_only=True)

    class Meta:
        model = StreamingAvailability
        fields = [
            'id', 'service', 'service_display', 'region', 'url', 'price',
            'available_from', 'available_until', 'quality', 'updated_at'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    likes_count = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'rating', 'content', 'sentiment_score',
            'likes_count', 'user_has_liked', 'created_at', 'updated_at'
        ]
        read_only_fields = ['sentiment_score', 'likes_count', 'user_has_liked']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_user_has_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False


class MovieNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieNews
        fields = [
            'id', 'title', 'content', 'source_url', 'source_name',
            'image_url', 'published_at', 'created_at'
        ]


class MovieListSerializer(serializers.ModelSerializer):
    """Serializer for movie list view with minimal information"""
    genres = GenreSerializer(many=True, read_only=True)
    content_warnings = ContentWarningSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'release_date', 'poster_url', 'genres',
            'imdb_rating', 'content_warnings', 'age_rating'
        ]


class MovieDetailSerializer(serializers.ModelSerializer):
    """Serializer for movie detail view with complete information"""
    genres = GenreSerializer(many=True, read_only=True)
    directors = serializers.SerializerMethodField()
    cast = serializers.SerializerMethodField()
    content_warnings = ContentWarningSerializer(many=True, read_only=True)
    streaming_availability = StreamingAvailabilitySerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    news = MovieNewsSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    user_interaction = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'original_title', 'imdb_id', 'overview',
            'release_date', 'runtime', 'poster_url', 'backdrop_url',
            'trailer_url', 'genres', 'directors', 'cast', 'content_warnings',
            'age_rating', 'imdb_rating', 'rotten_tomatoes_score',
            'budget', 'revenue', 'original_language', 'production_companies',
            'filming_locations', 'based_on_book', 'book_title', 'book_author',
            'fun_facts', 'trivia', 'awards', 'streaming_availability',
            'reviews', 'news', 'average_rating', 'user_interaction',
            'created_at', 'updated_at'
        ]

    def get_directors(self, obj):
        directors = MovieDirector.objects.filter(movie=obj)
        return MovieDirectorSerializer(directors, many=True).data

    def get_cast(self, obj):
        cast = MovieCast.objects.filter(movie=obj).order_by('order')
        return MovieCastSerializer(cast, many=True).data

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return None
        return sum(review.rating for review in reviews) / reviews.count()

    def get_user_interaction(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return None

        interactions = UserMovieInteraction.objects.filter(
            user=request.user,
            movie=obj
        )

        return {
            'viewed': interactions.filter(interaction_type='VIEW').exists(),
            'wishlisted': interactions.filter(interaction_type='WISHLIST').exists(),
            'favorited': interactions.filter(interaction_type='FAVORITE').exists(),
            'rated': interactions.filter(interaction_type='RATE').exists(),
        }


class UserMovieInteractionSerializer(serializers.ModelSerializer):
    movie = MovieListSerializer(read_only=True)
    interaction_type_display = serializers.CharField(
        source='get_interaction_type_display',
        read_only=True
    )

    class Meta:
        model = UserMovieInteraction
        fields = [
            'id', 'movie', 'interaction_type',
            'interaction_type_display', 'created_at'
        ]
        read_only_fields = ['interaction_type_display']

    def validate(self, data):
        """
        Check that the interaction type is valid and unique for the user-movie pair
        """
        user = self.context['request'].user
        movie = self.context['movie']
        interaction_type = data['interaction_type']

        # Check if interaction already exists
        if UserMovieInteraction.objects.filter(
                user=user,
                movie=movie,
                interaction_type=interaction_type
        ).exists():
            raise serializers.ValidationError(
                f"This {interaction_type.lower()} interaction already exists."
            )

        return data


class ReviewCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating reviews"""

    class Meta:
        model = Review
        fields = ['rating', 'content']

    def validate_rating(self, value):
        """
        Check that the rating is between 1 and 10
        """
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                "Rating must be between 1 and 10."
            )
        return value

    def create(self, validated_data):
        """
        Create a new review with the current user and movie
        """
        user = self.context['request'].user
        movie = self.context['movie']

        # Check if user already reviewed this movie
        if Review.objects.filter(user=user, movie=movie).exists():
            raise serializers.ValidationError(
                "You have already reviewed this movie."
            )

        return Review.objects.create(
            user=user,
            movie=movie,
            **validated_data
        )