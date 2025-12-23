import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather-services")


@mcp.tool()
def get_weather(city: str) -> dict:
    """
    Get current weather for a city.
    
    Args:
        city: Name of city (e.g., "London", "New York", "Tokyo")
    """
    try:
        response = requests.get(
            f"https://wttr.in/{city}?format=j1",
            headers={"User-Agent": "SuperBox-MCP/1.0"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        current = data["current_condition"][0]
        return {
            "city": city,
            "temperature_celsius": int(current["temp_C"]),
            "temperature_fahrenheit": int(current["temp_F"]),
            "condition": current["weatherDesc"][0]["value"],
            "humidity_percent": int(current["humidity"]),
            "wind_kph": int(current['windspeedKmph'])
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_forecast(city: str, days: int = 3) -> dict:
    """
    Get weather forecast for a city.
    
    Args:
        city: Name of city
        days: Number of days (1-3)
    """
    try:
        days = min(max(days, 1), 3)
        response = requests.get(
            f"https://wttr.in/{city}?format=j1",
            headers={"User-Agent": "SuperBox-MCP/1.0"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        forecast = []
        for day in data["weather"][:days]:
            forecast.append({
                "date": day["date"],
                "max_temp_celsius": int(day["maxtempC"]),
                "min_temp_celsius": int(day["mintempC"]),
                "max_temp_fahrenheit": int(day["maxtempF"]),
                "min_temp_fahrenheit": int(day["mintempF"]),
                "condition": day["hourly"][4]["weatherDesc"][0]["value"]
            })
        
        return {
            "city": city,
            "forecast": forecast
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    mcp.run()
