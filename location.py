import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("location-services")


@mcp.tool()
def get_location() -> dict:
    """Get your current location based on your IP address."""
    try:
        response = requests.get("http://ip-api.com/json/", timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == "success":
            return {
                "city": data.get("city"),
                "region": data.get("regionName"),
                "country": data.get("country"),
                "country_code": data.get("countryCode"),
                "latitude": data.get("lat"),
                "longitude": data.get("lon"),
                "timezone": data.get("timezone")
            }
        return {"error": "Could not determine location"}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def search_place(place_name: str) -> dict:
    """
    Convert place name to coordinates.
    
    Args:
        place_name: Name of location (e.g., "Paris", "Times Square", "Tokyo Tower")
    """
    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": place_name, "format": "json", "limit": 1},
            headers={"User-Agent": "SuperBox-MCP/1.0"},
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        
        if data:
            loc = data[0]
            return {
                "place_name": place_name,
                "display_name": loc["display_name"],
                "latitude": float(loc["lat"]),
                "longitude": float(loc["lon"]),
                "type": loc.get("type")
            }
        return {"error": f"Location not found: {place_name}"}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def reverse_geocode(latitude: float, longitude: float) -> dict:
    """
    Convert coordinates to place name.
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
    """
    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": latitude, "lon": longitude, "format": "json"},
            headers={"User-Agent": "SuperBox-MCP/1.0"},
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        
        if "display_name" in data:
            return {
                "latitude": latitude,
                "longitude": longitude,
                "display_name": data["display_name"],
                "address": data.get("address", {})
            }
        return {"error": "Location not found"}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    mcp.run()
