"""base_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/

Examples:
    Function views
        1. Add an import:  from my_app import views
        2. Add a URL to urlpatterns:  path('', views.home, name='home')
    Class-based views
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    Including another URLconf
        1. Import the include() function: from django.urls import include, path
        2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""
# Django Libraries
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views

# 3rd Party Libraries
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ----------------------------------------------------------------------------
# Swagger UI
# ----------------------------------------------------------------------------
urlpatterns += [
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path(
        "api/rdocs/",
        SpectacularRedocView.as_view(url_name="api-schema"),
        name="api-ReDocs",
    ),
]

# ----------------------------------------------------------------------------
# Debug Urls
# ----------------------------------------------------------------------------
if settings.DEBUG:
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        # 3rd Party Libraries
        import debug_toolbar

        urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# ----------------------------------------------------------------------------
# Custom API  url
# ----------------------------------------------------------------------------
urlpatterns += [
    path("api/weather/", include("weather.urls")),
]
