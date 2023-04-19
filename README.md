# Corteva Code Challenge: Solutions

<!-- toc -->

## Table of contents

-   [Problem 1](#problem-1)
-   [Problem 2](#problem-2)
-   [Problem 3](#problem-3)
-   [Problem 4](#problem-4)
-   [Problem 5: Deployment](#problem-5-deployment)

<!-- tocstop -->

## Problem 1

To implement the solution, Django's ORM was used. The database schema is shown
below and can be found in `/base/core/models.py`.

```python
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
```

## Problem 2

The Django management command `ingest_weather_data` was used for data ingestion.
The command can be executed by running `python manage.py ingest_weather_data`.
The total ingestion time is: `10 mins`

> The constraints defined in the database model ensure that duplicate data is
not inserted.

## Problem 3

The Django management command `analyze_weather` was used for data analysis.
The command can be executed by running `python manage.py analyze_weather`.
The total ingestion time is: `~3 mins`

```python
"""Django command to populate the `WeatherStats` model on first boot."""
# Standard Library
import logging
import time

from datetime import timedelta

# Django Libraries
from django.core.management.base import BaseCommand
from django.db.models import Avg, Max, Min, Sum

# Project Libraries
from core.models import WeatherDetails, WeatherStats


logger = logging.getLogger("corteva_api")
logger.setLevel("INFO")


class Command(BaseCommand):
    """Django command to populate the `WeatherStats` model on first boot."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        if WeatherDetails.objects.count():
            logger.info("Populating WeatherStats ......")
            start_time = time.monotonic()

            start_year = WeatherDetails.objects.aggregate(Min("record_date"))[
                "record_date__min"
            ].year
            end_year = WeatherDetails.objects.aggregate(Max("record_date"))[
                "record_date__max"
            ].year

            objs = []

            for station in (
                _.get("weather_station")
                for _ in WeatherDetails.objects.distinct("weather_station").values(
                    "weather_station"
                )
            ):
                for year in range(start_year, end_year + 1):
                    avg_max_temp = (
                        WeatherDetails.objects.filter(
                            weather_station=station, record_date__year=year
                        )
                        .exclude(max_temp=-9999)
                        .aggregate(Avg("max_temp"))
                        .get("max_temp__avg")
                    )
                    avg_min_temp = (
                        WeatherDetails.objects.filter(
                            weather_station=station, record_date__year=year
                        )
                        .exclude(min_temp=-9999)
                        .aggregate(Avg("min_temp"))
                        .get("min_temp__avg")
                    )
                    total_precip = (
                        WeatherDetails.objects.filter(
                            weather_station=station, record_date__year=year
                        )
                        .exclude(precip=-9999)
                        .aggregate(Sum("precip"))
                        .get("precip__sum")
                    )
                    objs.append(
                        WeatherStats(
                            weather_station=station,
                            max_temp_avg=avg_max_temp,
                            min_temp_avg=avg_min_temp,
                            total_precip=total_precip,
                            year=year,
                        )
                    )
            WeatherStats.objects.all().delete()
            WeatherStats.objects.bulk_create(objs, batch_size=1000)

            end_time = time.monotonic()
            logger.info("Success................")
            logger.info("time taken %s" % timedelta(seconds=end_time - start_time))
        else:
            logger.critical(
                "Weather Data doesn't exists!, Failed Analyzing weather data."
            )

```

> The constraints defined in the database model ensure that duplicate data is
not inserted.


## Problem 4

To implement the solution, the Django REST framework was used. Follow the steps
below to get started:

```shell
docker build .
docker compose build
docker compose up
```

* To view the Swagger API documentation, navigate to `localhost:8000/api/docs` or `
  localhost:8000/api/rdocs/`.
* To access the weather data, go to `localhost:8000/api/weather`.
* For data analysis, visit `localhost:8000/api/weather/stats`.


Please note that the `.envs` directory contains environment variables that
should not be committed to GitHub. For brevity reasons, they are included in
this repository.

## Problem 5: Deployment

Although I do not have experience deploying to AWS, I can provide some insights
based on my experience deploying to Azure. To achieve this, I intend to utilize
the following services:

* Azure Database for PostgreSQL flexible server as the database
* Azure App Services to host the web application
* Azure Data Factory for data ingestion and analysis generation.
