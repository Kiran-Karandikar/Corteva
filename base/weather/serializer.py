"""Serializers for the Weather API View."""
# Standard Library
import logging

# 3rd Party Libraries
from rest_framework import serializers

# Project Libraries
from core.models import WeatherDetails, WeatherStats


logger = logging.getLogger("corteva_api")


class WeatherDetailsSerializer(serializers.ModelSerializer):
    """Serializer for the retrieving details from `WeatherDetails` model.

    Notes:
        1. Retrieve all details from `WeatherDetails` model.
    """

    class Meta:
        model = WeatherDetails
        fields = "__all__"


class WeatherStatsDetailsSerializer(serializers.ModelSerializer):
    """Serializer for the retrieving details from `WeatherStats` model.

    Notes:
        1. Retrieve all details from `WeatherStats` model.
    """

    class Meta:
        model = WeatherStats
        fields = "__all__"
