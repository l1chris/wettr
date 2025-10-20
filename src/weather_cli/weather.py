import logging
from typing import List

import requests
from pydantic import BaseModel, Field, ValidationError

from weather_cli.utils import Geodata

logger = logging.getLogger(__name__)


class CoordinateData(BaseModel):
    country: str
    latitude: float
    longitude: float


class CurrentData(BaseModel):
    temperature: float
    windspeed: float
    weathercode: int


class HourlyData(BaseModel):
    time: List[str]
    temperature_2m: List[float] = Field(..., alias="temperature_2m")
    weather_code: List[int]


class DailyData(BaseModel):
    time: List[str]
    temperature_2m_max: List[float] = Field(..., alias="temperature_2m_max")
    temperature_2m_min: List[float] = Field(..., alias="temperature_2m_min")
    weather_code: List[int]


class WeatherData(BaseModel):
    timezone: str
    current_weather: CurrentData
    hourly: HourlyData
    daily: DailyData


def get_coordinates_for_city(city: str) -> Geodata | None:
    """
    Get coordinates and country for a given city name.

    Args:
        city: Name of the city to look up

    Returns:
        Instance of Geodata if successful, None otherwise.
    """
    if not city:
        print("Error: No city name provided")
        return None

    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        data = response.json()

        if not data.get("results"):
            print(f"Error: City '{city}' not found")
            return None

        first_result = data["results"][0]
        first_result = CoordinateData.model_validate(first_result)

        return Geodata(
            city, first_result.country, first_result.latitude, first_result.longitude
        )

    except requests.exceptions.Timeout:
        logger.error("Error: Request timed out while looking up city")
        return None
    except requests.exceptions.ConnectionError:
        logger.error("Error: Could not connect to geocoding service")
        return None
    except requests.exceptions.HTTPError as e:
        logger.error(f"Error: HTTP error occurred: {e}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error: Request failed: {e}")
        return None
    except ValidationError as e:
        logger.error(f"Error: Response validation failed: {e}")
        return None


def get_current_weather(lat: float, lon: float) -> WeatherData | None:
    """
    Get weather information for a latitude and longitude.

    Args:
        lat: Latitude value
        lon: Longitude value

    Returns:
        WeatherData, None otherwise.
    """
    if not lat or not lon:
        logger.error("Error: No latitude or longitude provided")
        return None

    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current_weather=true"
            f"&hourly=temperature_2m,weather_code"
            f"&daily=temperature_2m_max,temperature_2m_min,weather_code"
            f"&forecast_days=4"
            f"&timezone=auto"
        )
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        data = WeatherData.model_validate_json(response.text)

        return data

    except requests.exceptions.Timeout:
        logger.error("Error: Request timed out while looking up city")
        return None
    except requests.exceptions.ConnectionError:
        logger.error("Error: Could not connect to open meteo")
        return None
    except requests.exceptions.HTTPError as e:
        logger.error(f"Error: HTTP error occurred: {e}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error: Request failed: {e}")
        return None
    except ValidationError as e:
        logger.error(f"Error: Response validation failed: {e}")
        return None
