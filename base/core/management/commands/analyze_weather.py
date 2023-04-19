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
