---
name: weather
description: Get current weather and forecasts using Open-Meteo API. MUST use the exec tool to run curl commands - never generate fake weather data.
homepage: https://open-meteo.com/en/docs
metadata: {"nanobot":{"emoji":"🌤️","requires":{"bins":["curl"]}}}
---

# Weather

Free weather service, no API key needed. Open-Meteo is accessible in China.

## IMPORTANT: Always Use exec Tool

When users ask about weather, you MUST:
1. Use the `exec` tool to run curl commands
2. Parse the actual JSON response from the API
3. Never generate fake weather data or make up information

## Open-Meteo (primary)

Free, no key, good for programmatic use. Returns JSON with weather data.

### Current Weather

```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=22.63&longitude=114.04&current_weather=true"
```

Returns JSON with:
- `temperature`: Current temperature (°C)
- `windspeed`: Wind speed (km/h)
- `weathercode`: Weather condition code
- `is_day`: Day/Night indicator

### Detailed Forecast

```bash
###curl -s "https://api.open-meteo.com/v1/forecast?latitude=22.63&longitude=114.04&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&hourly=temperature_2m,precipitation_probability"
curl -s "https://api.open-meteo.com/v1/forecast?latitude=22.63&longitude=114.04&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&hourly=temperature_2m"
```

### Weather Code Reference

Common weather codes:
- 0: Clear sky
- 1-3: Partly cloudy
- 45, 48: Fog
- 51-67: Drizzle/Rain
- 71-77: Snow
- 95-99: Thunderstorm

### Finding Coordinates

Use geocoding to find city coordinates:
```bash
curl -s "https://geocoding-api.open-meteo.com/v1/search?name=Beijing&count=1&language=zh&format=json"
```

Returns latitude and longitude for the city.

### Complete Example

```bash
# Get Beijing weather
curl -s "https://api.open-meteo.com/v1/forecast?latitude=39.90&longitude=116.40&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&timezone=auto"
```

## Example Usage Pattern

**Correct approach (use exec tool):**
```
User: What's the weather in Beijing?
AI: I'll check the current weather in Beijing for you.
[exec tool: curl -s "https://api.open-meteo.com/v1/forecast?latitude=39.90&longitude=116.40&current_weather=true"]
Based on the API response, Beijing currently shows: temperature 15°C, clear sky conditions.
```

**Incorrect approach (NEVER do this):**
```
User: What's the weather in Beijing?
AI: Beijing currently has a temperature of 15°C with clear skies and 45% humidity. ← WRONG! This is fake data.
```

Docs: https://open-meteo.com/en/docs
