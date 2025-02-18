from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="AI Entertainment Platform API",
        default_version='v1',
        description="API documentation for AI Entertainment Platform",
        contact=openapi.Contact(email="contact@aientertainment.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.movies.urls')),
    path('api/v1/', include('apps.users.urls')),
    path('api/v1/', include('apps.recommendations.urls')),
    path('api/v1/', include('apps.streaming.urls')),
    path('api/v1/', include('apps.moderation.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]