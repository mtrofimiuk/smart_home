import csv
import datetime
from typing import Iterable

import requests

SUNRISE_API = "https://api.sunrise-sunset.org/json"
LOCATION = (52.190767, 21.158035)
YEAR = 2020


def all_days(year: int) -> Iterable[str]:
    day = datetime.date(day=1, month=1, year=year)
    while True:
        yield day.isoformat()
        day += datetime.timedelta(days=1)
        if day.year > year:
            break


all_days_sunrise_data = []

for day in all_days(YEAR):
    sunrise_data = requests.get(
        SUNRISE_API, params={"lat": LOCATION[0], "lng": LOCATION[1], "date": day}
    ).json()
    print(f"{day} {sunrise_data['status']}")
    results = sunrise_data["results"]
    results["day"] = day
    all_days_sunrise_data.append(results)

with open(f"data/{YEAR}.csv", "w") as csvfile:
    field_names = all_days_sunrise_data[0].keys()
    writer = csv.DictWriter(csvfile, field_names)
    writer.writeheader()
    writer.writerows(all_days_sunrise_data)
