from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Person(models.Model):
    """Model for actors, directors, and other crew members"""
    name = models.CharField(max_length=255)
    biography = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=255, blank=True)
    image_url = models.URLField(blank=True)
    imdb_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['imdb_id']),
        ]

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Model for movie/series genres"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ContentWarning(models.Model):
    """Model for content warnings and age ratings"""
    WARNING_TYPES = [
        ('VIOLENCE', 'Violence'),
        ('LANGUAGE', 'Strong Language'),
        ('SEXUAL', 'Sexual Content'),
        ('DRUGS', 'Drug Use'),
        ('PHOTOSENSITIVE', 'Photosensitive Content'),
        ('DISTURBING', 'Disturbing Content'),
    ]

    warning_type = models.CharField(max_length=20, choices=WARNING_TYPES)
    description = models.TextField()
    severity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return f"{self.get_warning_type_display()} (Severity: {self.severity})"


class Movie(models.Model):
    """Model for movies"""
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255, blank=True)
    imdb_id = models.CharField(max_length=20, unique=True)
    overview = models.TextField()
    release_date = models.DateField()
    runtime = models.IntegerField(help_text="Runtime in minutes")
    poster_url = models.URLField(blank=True)
    backdrop_url = models.URLField(blank=True)
    trailer_url = models.URLField(blank=True)

    # Relationships
    genres = models.ManyToManyField(Genre, related_name='movies')
    directors = models.ManyToManyField(
        Person,
        related_name='directed_movies',
        through='MovieDirector'
    )
    cast = models.ManyToManyField(
        Person,
        related_name='acted_movies',
        through='MovieCast'
    )
    content_warnings = models.ManyToManyField(
        ContentWarning,
        related_name='movies'
    )

    # Ratings and scores
    age_rating = models.CharField(max_length=10)  # e.g., PG-13, R, etc.
    imdb_rating = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    rotten_tomatoes_score = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    # Additional information
    budget = models.BigIntegerField(null=True, blank=True)
    revenue = models.BigIntegerField(null=True, blank=True)
    original_language = models.CharField(max_length=10)
    production_companies = models.TextField(blank=True)
    filming_locations = models.TextField(blank=True)

    # Book adaptation info
    based_on_book = models.BooleanField(default=False)
    book_title = models.CharField(max_length=255, blank=True)
    book_author = models.CharField(max_length=255, blank=True)

    # Interesting facts and trivia
    fun_facts = models.TextField(blank=True)
    trivia = models.TextField(blank=True)
    awards = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['imdb_id']),
            models.Index(fields=['release_date']),
        ]

    def __str__(self):
        return self.title


class MovieDirector(models.Model):
    """Through model for movie directors"""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    director = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, default='Director')

    class Meta:
        unique_together = ('movie', 'director')


class MovieCast(models.Model):
    """Through model for movie cast members"""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=255)
    order = models.IntegerField()

    class Meta:
        unique_together = ('movie', 'person', 'character_name')
        ordering = ['order']


class Review(models.Model):
    """Model for user reviews"""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    content = models.TextField()
    sentiment_score = models.FloatField(null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('movie', 'user')
        indexes = [
            models.Index(fields=['movie', 'created_at']),
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f"Review for {self.movie.title} by {self.user.username}"


class UserMovieInteraction(models.Model):
    """Model for tracking user interactions with movies"""
    INTERACTION_TYPES = [
        ('VIEW', 'Viewed'),
        ('WISHLIST', 'Added to Wishlist'),
        ('FAVORITE', 'Favorited'),
        ('RATE', 'Rated'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie', 'interaction_type')
        indexes = [
            models.Index(fields=['user', 'interaction_type']),
            models.Index(fields=['movie', 'interaction_type']),
        ]


class MovieNews(models.Model):
    """Model for movie-related news and updates"""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='news')
    title = models.CharField(max_length=255)
    content = models.TextField()
    source_url = models.URLField()
    source_name = models.CharField(max_length=100)
    image_url = models.URLField(blank=True)
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['movie', 'published_at']),
            models.Index(fields=['published_at']),
        ]

    def __str__(self):
        return self.title


class StreamingAvailability(models.Model):
    """Model for tracking where movies are available to stream"""
    STREAMING_SERVICES = [
        ('NETFLIX', 'Netflix'),
        ('AMAZON', 'Amazon Prime'),
        ('DISNEY', 'Disney+'),
        ('HULU', 'Hulu'),
        ('HBO', 'HBO Max'),
        ('APPLE', 'Apple TV+'),
        ('PEACOCK', 'Peacock'),
        ('PARAMOUNT', 'Paramount+'),
    ]

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='streaming_availability')
    service = models.CharField(max_length=20, choices=STREAMING_SERVICES)
    region = models.CharField(max_length=10)  # ISO country code
    url = models.URLField()
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    available_from = models.DateTimeField()
    available_until = models.DateTimeField(null=True, blank=True)
    quality = models.CharField(max_length=20, blank=True)  # HD, 4K, etc.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('movie', 'service', 'region')
        indexes = [
            models.Index(fields=['movie', 'service']),
            models.Index(fields=['service', 'region']),
        ]

    def __str__(self):
        return f"{self.movie.title} on {self.get_service_display()} ({self.region})"