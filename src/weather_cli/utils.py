import logging
from dataclasses import dataclass

import requests
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class IPWhoIsData(BaseModel):
    success: bool
    city: str
    country: str
    latitude: float
    longitude: float


@dataclass
class Geodata:
    city: str
    country: str
    lat: float
    lon: float


def get_coordinates_for_ip() -> Geodata | None:
    """
    Get coordinates and geo information for an IP address.

    Returns:
        Instance of Geodata if successful, None otherwise.
    """
    try:
        response = requests.get("https://ipwho.is", timeout=5)

        data = IPWhoIsData.model_validate_json(response.text)

        if data.success:
            return Geodata(data.city, data.country, data.latitude, data.longitude)
        else:
            # API returned success=false, log the reason if available
            logger.error(
                f"Location lookup failed: {data.get('message', 'Unknown error')}"
            )
            return None
    except requests.exceptions.Timeout:
        logger.error("Error: Request timed out while fetching location")
        return None
    except requests.exceptions.ConnectionError:
        logger.error("Error: Could not connect to location service")
        return None
    except requests.exceptions.HTTPError as e:
        logger.error(f"Error: HTTP error occurred: {e}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error: Request failed: {e}")
        return None
    except (KeyError, ValueError) as e:
        logger.error(f"Error: Invalid response format: {e}")
        return None


def get_icon(code: int) -> str:
    if code == 0:
        return "☀️"
    elif code in [1, 2]:
        return "🌤️"
    elif code == 3:
        return "☁️"
    elif 45 <= code <= 48:
        return "🌫️"
    elif 51 <= code <= 67:
        return "🌦️"
    elif 71 <= code <= 77:
        return "🌨️"
    elif 80 <= code <= 82:
        return "🌧️"
    elif code == 95:
        return "⛈️"
    elif 96 <= code <= 99:
        return "⛈️⚡"
    else:
        return "❓"


def get_weekday(number: int) -> str:
    if number == 0:
        return "Mon"
    elif number == 1:
        return "Tue"
    elif number == 2:
        return "Wed"
    elif number == 3:
        return "Thu"
    elif number == 4:
        return "Fri"
    elif number == 5:
        return "Sat"
    elif number == 6:
        return "Sun"


def get_ascii_title():
    return r"""
                      __   __
     _      __ ___   / /_ / /_ _____
    | | /| / // _ \ / __// __// ___/
    | |/ |/ //  __// /_ / /_ / /
    |__/|__/ \___/ \__/ \__//_/
"""


def to_fahrenheit(celsius: float) -> float:
    return round(celsius * 9 / 5 + 32, 1)
