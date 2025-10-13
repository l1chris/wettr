from weather_cli.utils import to_fahrenheit


def test_to_fahrenheit():
    """Test conversion at water's freezing point"""
    assert to_fahrenheit(0) == 32.0


def test_to_fahrenheit_rounding():
    """Test that result is rounded to 1 decimal place"""
    # 15°C = 59.0°F exactly
    assert to_fahrenheit(15) == 59.0
    # 15.56°C = 60.008°F, should round to 60.0
    assert to_fahrenheit(15.56) == 60.0
