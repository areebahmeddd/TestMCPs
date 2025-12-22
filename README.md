# Simple Location MCP Server

A minimal Model Context Protocol (MCP) server that returns your location (latitude and longitude).

## Tools

1. **get_my_location** - Get your current location via IP geolocation
2. **get_location** - Get coordinates for any place by name

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Running Locally

```bash
python main.py
```

### Testing with SuperBox CLI

```bash
# Test mode (without registration)
superbox test --url https://github.com/YOUR_USERNAME/test-mcp --client vscode

# Or push to registry (with security scanning)
superbox push --name location-mcp
```

## Examples

**"What is my location?"**
```
Your location: Mumbai, Maharashtra, India
Latitude: 19.0760
Longitude: 72.8777
Timezone: Asia/Kolkata
```

**"What is the location of Eiffel Tower?"**
```
Location: Tour Eiffel, 5, Avenue Anatole France, Paris, France
Latitude: 48.8582
Longitude: 2.2945
```

## License

MIT
