"""Django command to populate the `WeatherDetails` model on first boot."""
# Standard Library
import logging
import time

from datetime import timedelta

# Django Libraries
from django.core.management.base import BaseCommand

# 3rd Party Libraries
from tqdm import tqdm

# Project Libraries
from core.models import WeatherDetails
from weather.process_weather_data import prepare_weather_records


logger = logging.getLogger("corteva_api")
logger.setLevel("INFO")


class Command(BaseCommand):
    """Django command to populate the `WeatherDetails` model on first boot."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        logger.info("Populating WeatherDetails ......")
        start_time = time.monotonic()
        all_station_data = prepare_weather_records()
        objs = []
        for station in tqdm(
            all_station_data,
            total=len(all_station_data),
            desc="Ingesting data.",
        ):
            for record in station:
                file_name, r_date, max_t, min_t, precip = record
                file_name = file_name.strip(".txt").strip("USC")
                objs.append(
                    WeatherDetails(
                        weather_station=file_name,
                        record_date=r_date,
                        max_temp=max_t,
                        min_temp=min_t,
                        precip=precip,
                    )
                )

        WeatherDetails.objects.bulk_create(objs, batch_size=1000, ignore_conflicts=True)
        end_time = time.monotonic()
        logger.info("Success................")
        logger.info("time taken %s" % timedelta(seconds=end_time - start_time))
