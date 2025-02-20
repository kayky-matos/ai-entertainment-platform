from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg, Count

from .models import (
    Movie,
    Person,
    Genre,
    ContentWarning,
    MovieDirector,
    MovieCast,
    Review,
    UserMovieInteraction,
    MovieNews,
    StreamingAvailability
)
from .tasks import (
    update_movie_streaming_availability,
    analyze_review_sentiment,
    update_movie_recommendations
)

class MovieDirectorInline(admin.TabularInline):
    model = MovieDirector
    extra = 1
    autocomplete_fields = ['director']

class MovieCastInline(admin.TabularInline):
    model = MovieCast
    extra = 1
    autocomplete_fields = ['person']
    ordering = ['order']

class StreamingAvailabilityInline(admin.TabularInline):
    model = StreamingAvailability
    extra = 1
    readonly_fields = ['updated_at']

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ['user', 'rating', 'sentiment_score', 'created_at']
    can_delete = False
    max_num = 0
    show_change_link = True

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'release_date',
        'age_rating',
        'imdb_rating',
        'rotten_tomatoes_score',
        'average_user_rating',
        'streaming_platforms',
        'view_on_site'
    ]
    list_filter = [
        'release_date',
        'age_rating',
        'genres',
        'based_on_book',
        'streaming_availability__service'
    ]
    search_fields = ['title', 'original_title', 'overview']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['genres', 'content_warnings']
    inlines = [
        MovieDirectorInline,
        MovieCastInline,
        StreamingAvailabilityInline,
        ReviewInline
    ]
    fieldsets = (
        (None, {
            'fields': (
                'title', 'original_title', 'imdb_id', 'overview',
                'release_date', 'runtime', 'age_rating'
            )
        }),
        ('Media', {
            'fields': ('poster_url', 'backdrop_url', 'trailer_url'),
            'classes': ('collapse',)
        }),
        ('Ratings', {
            'fields': ('imdb_rating', 'rotten_tomatoes_score'),
        }),
        ('Additional Information', {
            'fields': (
                'budget', 'revenue', 'original_language',
                'production_companies', 'filming_locations'
            ),
            'classes': ('collapse',)
        }),
        ('Book Adaptation', {
            'fields': ('based_on_book', 'book_title', 'book_author'),
            'classes': ('collapse',)
        }),
        ('Fun Facts & Trivia', {
            'fields': ('fun_facts', 'trivia', 'awards'),
            'classes': ('collapse',)
        }),
        ('Categories', {
            'fields': ('genres', 'content_warnings'),
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = [
        'update_streaming_availability',
        'update_recommendations',
        'export_movie_data'
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            avg_rating=Avg('reviews__rating'),
            platforms_count=Count('streaming_availability', distinct=True)
        )

    def average_user_rating(self, obj):
        return round(obj.avg_rating, 2) if obj.avg_rating else 'No ratings'
    average_user_rating.short_description = 'User Rating'

    def streaming_platforms(self, obj):
        return obj.platforms_count
    streaming_platforms.short_description = 'Streaming Platforms'

    def view_on_site(self, obj):
        url = reverse('movie-detail', kwargs={'pk': obj.pk})
        return format_html('<a href="{}" target="_blank">View</a>', url)

    def update_streaming_availability(self, request, queryset):
        for movie in queryset:
            update_movie_streaming_availability.delay(movie.id)
        self.message_user(request, f"Updating streaming availability for {queryset.count()} movies.")
    update_streaming_availability.short_description = "Update streaming availability"

    def update_recommendations(self, request, queryset):
        for movie in queryset:
            update_movie_recommendations.delay(movie.id)
        self.message_user(request, f"Updating recommendations for {queryset.count()} movies.")
    update_recommendations.short_description = "Update recommendations"

    class Media:
        css = {
            'all': ('admin/css/movie_admin.css',)
        }
        js = ('admin/js/movie_admin.js',)

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'birth_date',
        'movies_directed',
        'movies_acted',
        'view_on_site'
    ]
    list_filter = ['birth_date']
    search_fields = ['name', 'biography']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('name', 'biography', 'image_url')
        }),
        ('Personal Information', {
            'fields': ('birth_date', 'death_date', 'place_of_birth')
        }),
        ('External IDs', {
            'fields': ('imdb_id',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            directed_count=Count('directed_movies', distinct=True),
            acted_count=Count('acted_movies', distinct=True)
        )

    def movies_directed(self, obj):
        return obj.directed_count
    movies_directed.short_description = 'Movies Directed'

    def movies_acted(self, obj):
        return obj.acted_count
    movies_acted.short_description = 'Movies Acted In'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'movie',
        'user',
        'rating',
        'sentiment_score',
        'likes_count',
        'created_at'
    ]
    list_filter = ['rating', 'created_at']
    search_fields = ['movie__title', 'user__username', 'content']
    readonly_fields = ['sentiment_score', 'created_at', 'updated_at']
    actions = ['analyze_sentiment']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            likes_count=Count('likes')
        )

    def likes_count(self, obj):
        return obj.likes_count
    likes_count.short_description = 'Likes'

    def analyze_sentiment(self, request, queryset):
        for review in queryset:
            analyze_review_sentiment.delay(review.id)
        self.message_user(request, f"Analyzing sentiment for {queryset.count()} reviews.")
    analyze_sentiment.short_description = "Analyze sentiment"

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'movie_count']
    search_fields = ['name', 'description']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            movie_count=Count('movies')
        )

    def movie_count(self, obj):
        return obj.movie_count
    movie_count.short_description = 'Number of Movies'

@admin.register(ContentWarning)
class ContentWarningAdmin(admin.ModelAdmin):
    list_display = [
        'warning_type',
        'severity',
        'movie_count'
    ]
    list_filter = ['warning_type', 'severity']
    search_fields = ['description']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            movie_count=Count('movies')
        )

    def movie_count(self, obj):
        return obj.movie_count
    movie_count.short_description = 'Number of Movies'

@admin.register(MovieNews)
class MovieNewsAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'movie',
        'source_name',
        'published_at'
    ]
    list_filter = ['source_name', 'published_at']
    search_fields = ['title', 'content', 'movie__title']
    readonly_fields = ['created_at']

@admin.register(StreamingAvailability)
class StreamingAvailabilityAdmin(admin.ModelAdmin):
    list_display = [
        'movie',
        'service',
        'region',
        'price',
        'available_from',
        'available_until'
    ]
    list_filter = ['service', 'region', 'available_from']
    search_fields = ['movie__title']
    readonly_fields = ['updated_at']

@admin.register(UserMovieInteraction)
class UserMovieInteractionAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'movie',
        'interaction_type',
        'created_at'
    ]
    list_filter = ['interaction_type', 'created_at']
    search_fields = ['user__username', 'movie__title']
    readonly_fields = ['created_at']

# Register the through models with minimal admin interfaces
admin.site.register(MovieDirector)
admin.site.register(MovieCast)