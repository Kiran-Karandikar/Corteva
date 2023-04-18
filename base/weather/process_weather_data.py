"""Script to process data received from the wrike api."""
# Standard Library
import logging
import os

from datetime import datetime
from multiprocessing import Pool, cpu_count


logger = logging.getLogger("corteva_api")


def read_files():
    """Fetch Locally stored weather files."""
    return [
        os.path.join(location, file)
        for location in filter(
            lambda x: os.path.exists(x),
            map(lambda x: os.path.join(x, "wx_data"), (".", "../")),
        )
        for file in os.listdir(location)
    ]


def process_weather_record(file_path):
    """Read and parse individual weather record file.

    Args:
        file_path (:string): Actual file path of weather record.

    Returns:
        :list: List of tuple for each line of weather record.
    """
    records_list = []
    if os.path.exists(file_path):
        file_name = file_path.split("/")[-1]
        with open(file_path) as fp:
            logger.info(f"Processing file: {file_path}")
            for line in fp.readlines():
                year, max_t, min_t, p = line.split("\t")
                records_list.append(
                    (
                        file_name,
                        datetime.strptime(year, "%Y%m%d").date(),
                        float(max_t) / 10,
                        float(min_t) / 10,
                        float(p) / 10,
                    )
                )
            logger.info(f"Finished processing {file_path}")
    return records_list


def prepare_weather_records():
    """Read and process weather records from each station in parallel.

    Returns:
        :list: List of Lists of tuple for all weather records from each station.
    """
    total_process = cpu_count()
    logger.info(f"Using total: {total_process} of process")
    with Pool(total_process) as p:
        all_records_list = [
            record for record in p.map(process_weather_record, read_files())
        ]
    return all_records_list
