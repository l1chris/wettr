from unittest.mock import Mock, patch

from weather_cli.utils import Geodata, get_coordinates_for_ip, to_fahrenheit


@patch("weather_cli.utils.requests.get")
def test_success_get_coordinates_for_ip(mock_get):
    """Test successful coordinate lookup"""
    mock_response = Mock()
    mock_response.text = (
        '{"success": true, "city": "Oldenburg", "country": "Germany", '
        '"latitude": 53.14, "longitude": 8.21}'
    )
    mock_get.return_value = mock_response

    result = get_coordinates_for_ip()

    assert isinstance(result, Geodata)
    assert result.city == "Oldenburg"
    assert result.country == "Germany"


def test_to_fahrenheit():
    """Test conversion at water's freezing point"""
    assert to_fahrenheit(0) == 32.0


def test_to_fahrenheit_rounding():
    """Test that result is rounded to 1 decimal place"""
    # 15°C = 59.0°F exactly
    assert to_fahrenheit(15) == 59.0
    # 15.56°C = 60.008°F, should round to 60.0
    assert to_fahrenheit(15.56) == 60.0
