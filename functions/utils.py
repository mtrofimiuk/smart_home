import csv
import datetime
import re
from pathlib import Path

import requests
from loguru import logger

SUNRISE_DATA_YEAR = 2020

DATA_FILE = Path(__file__).parent.parent.joinpath(Path("data/2020.csv"))


def replace_year(day):
    return re.sub(r"^\d{4}", str(SUNRISE_DATA_YEAR), day)


def get_sunrise_data(day):
    day = replace_year(day)
    with DATA_FILE.open("r") as sunrise_data:
        reader = csv.reader(sunrise_data)
        header = next(reader)
        sunrise_data.seek(0)
        reader = csv.DictReader(sunrise_data, fieldnames=header)

        for sunrise_data_day in reader:
            if sunrise_data_day["day"] == day:
                return sunrise_data_day

    raise ValueError(f"Could not find sunrise data for {day}")


def turn_off(sunrise: datetime, address: str):
    now = datetime.datetime.utcnow()
    state = status(address)
    if now > sunrise and state == "on":
        logger.info("Turning lamp off")
        requests.get(f"http://{address}/off")


def turn_on(sunset: datetime, address: str):
    now = datetime.datetime.utcnow()
    state = status(address)
    if now > sunset and state == "off":
        logger.info("Turning lamp on")
        requests.get(f"http://{address}/on")


def toggle_lamp(sunrise: datetime, sunset: datetime, address: str):
    now = datetime.datetime.utcnow()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    state = status(address)

    if midnight <= now <= sunrise and state == "off":
        logger.info("Turning lamp on")
        requests.get(f"http://{address}/on")
    elif sunrise <= now <= sunset and state == "on":
        logger.info("Turning lamp off")
        requests.get(f"http://{address}/off")
    elif sunset <= now <= midnight + datetime.timedelta(days=1) and state == "off":
        logger.info("Turning lamp on")
        requests.get(f"http://{address}/on")


def status(address: str) -> str:
    response = requests.get(f"http://{address}/state")
    return re.findall(r"#state-->(\S+)", response.text)[0]
