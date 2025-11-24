"""
URL configuration for demperm-social backend.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static

# drf_yasg imports can trigger DRF settings to import third-party auth classes
# which may import Django models before apps are ready. To avoid AppRegistry
# errors at import time, import drf_yasg lazily when the docs endpoint is hit.
def _get_schema_view():
    """Lazily create and return a drf_yasg schema view.

    This defers importing drf_yasg until a request reaches the docs endpoints,
    avoiding import-time issues with Django app registry.
    """
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    # Ensure serializers defined in local apps have unique ref_name values
    # so drf_yasg does not raise collisions when multiple serializers
    # share the same class name across different modules.
    try:
        import importlib
        import inspect
        from pathlib import Path
        from rest_framework import serializers as drf_serializers

        APPS_DIR = Path(__file__).resolve().parent.parent / 'apps'
        if APPS_DIR.exists():
            for child in APPS_DIR.iterdir():
                if not child.is_dir():
                    continue
                mod_name = f"apps.{child.name}.serializers"
                try:
                    mod = importlib.import_module(mod_name)
                except Exception:
                    # ignore modules that don't exist or fail to import
                    continue

                for attr_name, attr in vars(mod).items():
                    try:
                        if inspect.isclass(attr) and issubclass(attr, drf_serializers.Serializer):
                            # If serializer has no Meta.ref_name, set a unique one
                            meta = getattr(attr, 'Meta', None)
                            if not (meta and getattr(meta, 'ref_name', None)):
                                # create or update Meta on the serializer class
                                Meta = type('Meta', (), {'ref_name': f"{attr.__module__}.{attr.__name__}"})
                                setattr(attr, 'Meta', Meta)
                    except Exception:
                        # guard against weird classes
                        continue
    except Exception:
        # Non-fatal: if this process fails, let drf_yasg handle naming as before
        pass

    return get_schema_view(
        openapi.Info(
            title="Demperm Social API",
            default_version='v1',
            description="API REST pour réseau social politique local",
            terms_of_service="https://www.example.com/terms/",
            contact=openapi.Contact(email="contact@example.com"),
            license=openapi.License(name="MIT License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

def _swagger_view(request, *args, **kwargs):
    """View wrapper for Swagger UI that instantiates schema view lazily."""
    # DEBUG WRAPPER: capture traceback and return plain text for easier debugging
    return _get_schema_view().with_ui('swagger', cache_timeout=0)(request, *args, **kwargs)

def _redoc_view(request, *args, **kwargs):
    """View wrapper for ReDoc UI that instantiates schema view lazily."""
    # DEBUG WRAPPER: capture traceback and return plain text for easier debugging
    return _get_schema_view().with_ui('redoc', cache_timeout=0)(request, *args, **kwargs)

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    
    # API v1
    path('api/v1/auth/', include('apps.custom_auth.urls')),
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/domains/', include('apps.domains.urls')),
    path('api/v1/forums/', include('apps.forums.urls')),
    path('api/v1/subforums/', include('apps.subforums.urls')),
    path('api/v1/subscriptions/', include('apps.subscriptions.urls')),
    path('api/v1/posts/', include('apps.posts.urls')),
    path('api/v1/comments/', include('apps.comments.urls')),
    path('api/v1/likes/', include('apps.likes.urls')),
    path('api/v1/followers/', include('apps.followers.urls')),
    path('api/v1/following/', include('apps.followers.urls')),  # Alias
    path('api/v1/tags/', include('apps.tags.urls')),
    path('api/v1/messages/', include('apps.custom_messages.urls')),
    path('api/v1/reports/', include('apps.reports.urls')),
    path('api/v1/admin/', include('apps.admin_panel.urls')),
    
    # API Documentation
    path('api/v1/docs/', _swagger_view, name='schema-swagger-ui'),
    path('api/v1/redoc/', _redoc_view, name='schema-redoc'),
]

# In development environments we may run with DEBUG=True inside Docker and
# use Gunicorn; to make static assets available (admin, drf-yasg assets,
# etc.) append the static() helper when DEBUG is enabled. In production a
# proper static file server (nginx, S3, CDN) or WhiteNoise should be used.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

