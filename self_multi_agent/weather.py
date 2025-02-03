
from dotenv import load_dotenv
from langchain_core.tools import tool
from typing_extensions import TypedDict
from typing import Literal, Annotated
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

import logging
logger = logging.getLogger(__name__)


# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
weather_params = {
    "latitude": 0.0,
	"longitude": 0.0,
	"hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature", "showers", "visibility", "wind_speed_10m"],
	"temperature_unit": "fahrenheit",
	"wind_speed_unit": "ms"
}

class WeatherData(TypedDict):
    time: Annotated[list,pd.Timestamp]
    temperature: Annotated[list,float]
    relative_humidity: Annotated[list,float]
    showers: Annotated[list,float]
    dew: Annotated[list,float]
    apparent_temperature: Annotated[list,float]
    visibility: Annotated[list,float]

@tool
def get_weather(lat: float, lon: float) -> WeatherData:
    """Tool that returns the real-time weather updates for a given latitude and longitude"""
    logger.info(f"Getting weather for {lat} - {lon}")
    weather_params["latitude"] = lat
    weather_params["longitude"] = lon
    responses = openmeteo.weather_api(url, params=weather_params)[0]

    hourly = responses.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(3).ValuesAsNumpy()
    hourly_showers = hourly.Variables(4).ValuesAsNumpy()
    hourly_visibility = hourly.Variables(5).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(6).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
    ).strftime("%Y-%m-%d %H:%M:%S")}
    
    weatherInfo: WeatherData = {
        "time": hourly_data["date"][5:23],
        "temperature": hourly_temperature_2m[5:23],
        "relative_humidity": hourly_relative_humidity_2m[5:23],
        "dew": hourly_dew_point_2m[5:23],
        "apparent_temperature": hourly_apparent_temperature[5:23],
        "showers": hourly_showers[5:23],
        "wind_speed": hourly_wind_speed_10m[5:23],
        "visibility": hourly_visibility[5:23]
    }

    return weatherInfo


if __name__ == "__main__":
    load_dotenv()
    print(get_weather(37.7749, -122.4194))