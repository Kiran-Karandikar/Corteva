"""Views for the `api/weather` API endpoint."""
# Standard Library
import logging

# 3rd Party Libraries
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.settings import api_settings
from rest_framework.viewsets import ReadOnlyModelViewSet

# Project Libraries
from core.models import WeatherDetails, WeatherStats
from weather.serializer import WeatherDetailsSerializer, WeatherStatsDetailsSerializer


logger = logging.getLogger("corteva_api")


class WeatherDetailsView(ReadOnlyModelViewSet):
    """Get the `WeatherDetails` details.

    1. GET `api/weather/`: List all `WeatherDetails` stored in local database.

    See Also:
        1. https://docs.djangoproject.com/en/4.0/ref/contrib/auth/#fields
        2. https://www.django-rest-framework.org/api-guide/filtering/#filtering
    """

    permission_classes = [AllowAny]
    lookup_fields = ("weather_station", "record_date")
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    queryset = WeatherDetails.objects.all()
    http_method_names = ["get"]
    serializer_class = WeatherDetailsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("weather_station", "record_date")


class WeatherStatsDetailsView(ReadOnlyModelViewSet):
    """Get the `WeatherStats` details.

    1. GET `api/weather/stats`: List all `WeatherStats` stored in local database.

    See Also:
        1. https://docs.djangoproject.com/en/4.0/ref/contrib/auth/#fields
        2. https://www.django-rest-framework.org/api-guide/filtering/#filtering
    """

    permission_classes = [AllowAny]
    lookup_fields = ("weather_station", "record_date")
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    queryset = WeatherStats.objects.all()
    http_method_names = ["get"]
    serializer_class = WeatherStatsDetailsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("weather_station", "record_date")
