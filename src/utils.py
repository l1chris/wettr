def get_icon(code):
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


def get_weekday(number):
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
