# Django Libraries
from django.db import models


class WeatherStation(models.Model):
    """
    Model class to store station details.
    """

    weather_station = models.CharField(max_length=40, help_text="Station ID.")

    class Meta:
        abstract = True


class WeatherDetails(WeatherStation):
    record_date = models.DateField(
        help_text="Record date.", verbose_name="Record date."
    )
    max_temp = models.FloatField(
        help_text="Max temp (in 0.1°C).",
    )
    min_temp = models.FloatField(
        help_text="Min temp (in 0.1°C).",
    )
    precip = models.FloatField(
        help_text="Precipitation (in 0.1mm).",
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        null=False,
        verbose_name="Created on.",
    )
    last_updated = models.DateTimeField(
        auto_now=True, verbose_name="Last updated.", null=False
    )

    class Meta:
        ordering = ["weather_station"]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "weather_station",
                    "record_date",
                    "max_temp",
                    "min_temp",
                    "precip",
                ],
                name="Valid record by station, record and weather details.",
            )
        ]


class WeatherStats(WeatherStation):
    year = models.IntegerField(help_text="Stats done this year.")
    max_temp_avg = models.FloatField(
        null=True,
        help_text="Avg max temp (in °C).",
    )
    min_temp_avg = models.FloatField(
        null=True,
        help_text="Avg min temp (in °C).",
    )
    total_precip = models.FloatField(
        null=True,
        help_text="Total precip (in cm).",
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
        null=False,
        verbose_name="Created on.",
    )
    last_updated = models.DateTimeField(
        auto_now=True, verbose_name="Last updated.", null=False
    )

    class Meta:
        ordering = ["weather_station", "year"]
        constraints = [
            models.UniqueConstraint(
                fields=["weather_station", "year"],
                name="Valid Stats by station, record and weather details.",
            )
        ]
