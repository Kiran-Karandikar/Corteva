"""Url Patterns for api endpoint `api/weather/`.
"""
# Django Libraries
from django.urls import path

# Project Libraries
from weather.views import WeatherDetailsView, WeatherStatsDetailsView


app_name = "weather"

urlpatterns = [
    path("", WeatherDetailsView.as_view(actions={"get": "list"}), name="index"),
    path(
        "stats/",
        WeatherStatsDetailsView.as_view(actions={"get": "list"}),
        name="weather_stats",
    ),
]
