# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import debug_toolbar

from urllib.parse import urljoin

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ DJANGO IMPORTS                                                                     │
# └────────────────────────────────────────────────────────────────────────────────────┘

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ ADMIN CUSTOMIZATION                                                                │
# └────────────────────────────────────────────────────────────────────────────────────┘

# Get project name
project_name = settings.PROJECT_NAME

# Get environment reminder
environment_reminder = settings.ENVIRONMENT.title()

# Define title from environment reminder
TITLE = f"{project_name} {environment_reminder}"

# Set title for Django Admin
admin.site.site_title = TITLE
admin.site.site_header = TITLE
admin.site.index_title = "Admin Panel"

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ URL PATTERNS                                                                       │
# └────────────────────────────────────────────────────────────────────────────────────┘

# URL Patterns List
urlpatterns = []

# Locale-specific URL Patterns
for api_version in settings.API_VERSIONS:

    # Construct API route, e.g. api/v1/
    api_route = urljoin(settings.API_ROUTE, api_version + "/")

    # Append to URL patterns
    urlpatterns += [
        path(api_route, include(("api.urls", "api"), namespace=api_version))
    ]

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ DJANGO ADMIN                                                                       │
# └────────────────────────────────────────────────────────────────────────────────────┘

# Admin URL Pattern
if settings.ENABLE_DJANGO_ADMIN:

    # Django Admin
    urlpatterns += [path("admin/", admin.site.urls)]

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ BROWSABLE API                                                                      │
# └────────────────────────────────────────────────────────────────────────────────────┘

# Browsable API URL Pattern
if settings.ENABLE_BROWSABLE_API:

    # Browsable API
    urlpatterns += [path("auth/", include("rest_framework.urls"))]

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ DJANGO DEBUG TOOLBAR                                                               │
# └────────────────────────────────────────────────────────────────────────────────────┘

# Django Debug Toolbar Pattern
if settings.ENABLE_DJANGO_DEBUG_TOOLBAR:

    # Django Debug Toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ LOCAL ENVIRONMENT                                                                  │
# └────────────────────────────────────────────────────────────────────────────────────┘

# Check if environment is local
if settings.ENVIRONMENT == settings.LOCAL:

    # Check if environment uses local storage
    if settings.USE_LOCAL_STORAGE:

        # Add local static and media URLs
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
