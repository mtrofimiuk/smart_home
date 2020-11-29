import datetime

from dateutil.parser import parse

from functions.utils import get_sunrise_data, toggle_lamp

LAMP_ADDRESS = "192.168.3.247"

if __name__ == "__main__":
    now = datetime.datetime.utcnow()
    sunrise_data = get_sunrise_data(now.date().isoformat())
    sunset = parse(sunrise_data["civil_twilight_end"])
    sunrise = parse(sunrise_data["civil_twilight_begin"])
    toggle_lamp(sunrise, sunset, LAMP_ADDRESS)
