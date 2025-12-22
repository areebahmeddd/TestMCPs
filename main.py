"""
Simple Location MCP Server
Returns location coordinates (latitude and longitude)
"""

import requests
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("location-mcp")


@mcp.tool()
def get_my_location() -> str:
    """
    Get your current location based on your IP address.
    
    Returns:
        Your latitude, longitude, and location details
    """
    try:
        # Use IP geolocation (free, no API key needed)
        response = requests.get("http://ip-api.com/json/", timeout=5)
        data = response.json()
        
        if data.get("status") == "success":
            return (
                f"Your location: {data.get('city')}, {data.get('regionName')}, {data.get('country')}\n"
                f"Latitude: {data.get('lat')}\n"
                f"Longitude: {data.get('lon')}\n"
                f"Timezone: {data.get('timezone')}"
            )
        else:
            return "Could not determine your location"
    except Exception as e:
        return f"Error getting location: {str(e)}"


@mcp.tool()
def get_location(place_name: str) -> str:
    """
    Get coordinates for any location by name.
    
    Args:
        place_name: Name of the place (e.g., "Paris", "Eiffel Tower", "New York")
    
    Returns:
        Latitude and longitude of the place
    """
    try:
        # Use Nominatim (OpenStreetMap) for geocoding
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": place_name,
            "format": "json",
            "limit": 1
        }
        headers = {
            "User-Agent": "SuperBox-Location-MCP/1.0"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=5)
        data = response.json()
        
        if data and len(data) > 0:
            result = data[0]
            return (
                f"Location: {result.get('display_name')}\n"
                f"Latitude: {result.get('lat')}\n"
                f"Longitude: {result.get('lon')}"
            )
        else:
            return f"Could not find location: {place_name}"
    except Exception as e:
        return f"Error: {str(e)}"


# Run the server
if __name__ == "__main__":
    mcp.run()
