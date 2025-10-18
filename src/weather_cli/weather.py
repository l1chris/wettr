import logging
from typing import Dict, Optional

import requests

logger = logging.getLogger(__name__)


def get_coordinates(city: str) -> Optional[Dict[str, any]]:
    """
    Get coordinates and country for a given city name.

    Args:
        city: Name of the city to look up

    Returns:
        Dictionary with city, country, lat, lon if successful, None otherwise.
    """
    if not city:
        print("Error: No city name provided")
        return None

    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        data = response.json()

        if not data.get("results"):
            print(f"Error: City '{city}' not found")
            return None

        first_result = data["results"][0]

        # Validate that required fields exist
        required_fields = ["latitude", "longitude", "country"]
        if not all(field in first_result for field in required_fields):
            print("Error: Invalid response format from geocoding API")
            return None

        return {
            "city": city,
            "country": first_result["country"],
            "lat": first_result["latitude"],
            "lon": first_result["longitude"],
        }

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
    except (KeyError, IndexError, ValueError) as e:
        logger.error(f"Error: Could not parse geocoding response: {e}")
        return None


def get_current_weather(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current_weather=true"
        f"&hourly=temperature_2m,weather_code"
        f"&daily=temperature_2m_max,temperature_2m_min,weather_code"
        f"&forecast_days=4"
        f"&timezone=auto"
    )
    response = requests.get(url)
    return response.json()
