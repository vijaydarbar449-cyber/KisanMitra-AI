import httpx

from services.ai_service import LANGUAGE_NAMES, _call_gemini

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
TIMEOUT = 15


class PlaceNotFound(Exception):
    pass


def search_places(query: str, count: int = 10) -> list:
    """નામ પરથી મળતાં સ્થળોની યાદી (ગામ/શહેર)."""
    r = httpx.get(
        GEO_URL,
        params={
            "name": query,
            "count": count,
            "language": "en",
            "format": "json",
            "countryCode": "IN",
        },
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    places = []
    for p in r.json().get("results") or []:
        places.append({
            "name": p.get("name"),
            "taluka": p.get("admin3"),
            "district": p.get("admin2"),
            "state": p.get("admin1"),
            "latitude": p["latitude"],
            "longitude": p["longitude"],
        })
    return places


def find_place(name: str) -> dict:
    """ગામ/શહેરનું નામ -> પહેલું મળતું સ્થળ."""
    places = search_places(name, count=1)
    if not places:
        raise PlaceNotFound(name)
    return places[0]


def get_forecast(lat: float, lon: float):
    """હાલનું હવામાન અને 5 દિવસની આગાહી."""
    r = httpx.get(
        FORECAST_URL,
        params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
            "daily": (
                "temperature_2m_max,temperature_2m_min,precipitation_sum,"
                "precipitation_probability_max,wind_speed_10m_max"
            ),
            "timezone": "auto",
            "forecast_days": 5,
        },
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    data = r.json()
    cur = data.get("current", {})
    daily = data.get("daily", {})

    current = {
        "temp_c": cur.get("temperature_2m"),
        "humidity_pct": cur.get("relative_humidity_2m"),
        "rain_mm": cur.get("precipitation"),
        "wind_kmh": cur.get("wind_speed_10m"),
    }

    days = []
    for i, day in enumerate(daily.get("time", [])):
        days.append({
            "date": day,
            "temp_min_c": daily["temperature_2m_min"][i],
            "temp_max_c": daily["temperature_2m_max"][i],
            "rain_mm": daily["precipitation_sum"][i],
            "rain_chance_pct": daily["precipitation_probability_max"][i],
            "wind_max_kmh": daily["wind_speed_10m_max"][i],
        })
    return current, days


def weather_advice(place: dict, current: dict, days: list, crop: str = "", language: str = "gu") -> str:
    """હવામાનના આંકડા જોઈને AI ખેતીની સલાહ આપે."""
    lang = LANGUAGE_NAMES.get(language, "ગુજરાતી")
    label = ", ".join(
        x for x in [place.get("name"), place.get("district"), place.get("state")] if x
    )

    lines = [
        f"- {d['date']}: તાપમાન {d['temp_min_c']}°C થી {d['temp_max_c']}°C, "
        f"વરસાદ {d['rain_mm']} mm (શક્યતા {d['rain_chance_pct']}%), "
        f"પવન મહત્તમ {d['wind_max_kmh']} km/h"
        for d in days
    ]

    prompt = (
        f"સ્થળ: {label}\n"
        f"પાક: {crop or 'જણાવ્યો નથી (સામાન્ય સલાહ આપો)'}\n"
        f"હાલનું હવામાન: તાપમાન {current['temp_c']}°C, ભેજ {current['humidity_pct']}%, "
        f"પવન {current['wind_kmh']} km/h\n"
        f"આગામી {len(days)} દિવસની આગાહી:\n" + "\n".join(lines) + "\n\n"
        "ઉપરના આંકડાના આધારે ખેડૂતને સરળ અને ટૂંકી સલાહ આપો: "
        "1) આ દિવસોની ટૂંકી સ્થિતિ, 2) પિયત ક્યારે કરવું કે ન કરવું, "
        "3) દવા/ખાતરનો છંટકાવ કયા દિવસે કરવો કે ટાળવો (વરસાદ અને પવન ધ્યાનમાં રાખીને), "
        "4) આ હવામાનમાં રોગ-જીવાતનું જોખમ, 5) બીજી જરૂરી કાળજી. "
        "ફક્ત આપેલા આંકડાનો ઉપયોગ કરો, નવા આંકડા ન બનાવો. "
        "આગાહી બદલાઈ શકે છે તે જણાવો. "
        f"જવાબ {lang} ભાષામાં આપો."
    )
    return _call_gemini(prompt)