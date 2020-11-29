from unittest import mock
import datetime

import pytest
from freezegun import freeze_time

from functions.utils import get_sunrise_data, toggle_lamp


@pytest.fixture
def requests():
    with mock.patch("functions.utils.requests") as requests_mock:
        yield requests_mock


def test_get_sunrise_data():

    assert (
        get_sunrise_data(datetime.date(2021, 1, 1).isoformat())["sunrise"]
        == "6:12:39 AM"
    )


def test_night_after_midnight(requests):

    requests.get.return_value = mock.Mock(text="#state-->off")
    with freeze_time("2020-01-01 1:00"):
        toggle_lamp(
            sunrise=datetime.datetime(2020, 1, 1, 6),
            sunset=datetime.datetime(2020, 1, 1, 19),
            address="foo",
        )
        requests.get.assert_called_with("http://foo/on")
        requests.reset_mock()

        requests.get.return_value = mock.Mock(text="#state-->on")
        toggle_lamp(
            sunrise=datetime.datetime(2020, 1, 1, 6),
            sunset=datetime.datetime(2020, 1, 1, 19),
            address="foo",
        )
        assert mock.call("http://foo/on") not in requests.get.mock_calls


def test_during_day(requests):
    requests.get.return_value = mock.Mock(text="#state-->on")

    with freeze_time("2020-01-01 7:00"):
        toggle_lamp(
            sunrise=datetime.datetime(2020, 1, 1, 6),
            sunset=datetime.datetime(2020, 1, 1, 19),
            address="foo",
        )
        requests.get.assert_called_with("http://foo/off")
        requests.reset_mock()

        requests.get.return_value = mock.Mock(text="#state-->off")
        toggle_lamp(
            sunrise=datetime.datetime(2020, 1, 1, 6),
            sunset=datetime.datetime(2020, 1, 1, 19),
            address="foo",
        )
        assert mock.call("http://foo/off") not in requests.get.mock_calls


def test_after_sunset(requests):
    requests.get.return_value = mock.Mock(text="#state-->off")

    with freeze_time("2020-01-01 20:00"):
        toggle_lamp(
            sunrise=datetime.datetime(2020, 1, 1, 6),
            sunset=datetime.datetime(2020, 1, 1, 19),
            address="foo",
        )
        requests.get.assert_called_with("http://foo/on")
        requests.reset_mock()

        requests.get.return_value = mock.Mock(text="#state-->on")
        toggle_lamp(
            sunrise=datetime.datetime(2020, 1, 1, 6),
            sunset=datetime.datetime(2020, 1, 1, 19),
            address="foo",
        )
        assert mock.call("http://foo/on") not in requests.get.mock_calls
