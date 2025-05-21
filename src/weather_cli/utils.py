import requests


def get_location_from_ip():
    try:
        res = requests.get("https://ipwho.is", timeout=5)
        data = res.json()
        if data.get("success"):
            return {
                "city": data["city"],
                "country": data["country"],
                "lat": data["latitude"],
                "lon": data["longitude"],
            }
    except Exception:
        pass
    return None


def get_icon(code: int):
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


def get_weekday(number: int):
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


def to_fahrenheit(celsius: float):
    return round(celsius * 9 / 5 + 32, 1)
