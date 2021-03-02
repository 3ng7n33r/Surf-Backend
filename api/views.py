from django.http import HttpResponse
import requests
import arrow
import simplejson


def index(request):
    with open("storm_API.txt", "r") as f:
        apiKey = f.read()

    # %% Fetch data from stormglass
    # Get first hour of today
    start = arrow.utcnow().replace(hour=0, minute=0, second=0)

    # Get last hour of today
    end = start.shift(days=+6)

    response = requests.get(
        'https://api.stormglass.io/v2/weather/point',
        params={
            'lat': 47.72,
            'lng': -3.49,
            'params': ','.join(['waveHeight', 'airTemperature',
                                'waterTemperature',
                                'waveDirection', 'waveHeight', 'wavePeriod',
                                'windSpeed', 'windDirection']),
            'start': start.timestamp(),  # Convert to timestamp
            'end': end.timestamp(),  # Convert to UTC timestamp
            'source': 'noaa'
        },
        headers={
            'Authorization': apiKey
        }
    )

    json_data = response.json()

    # %% Save response to JSON file

    # now write output to a file
    weatherDataFile = open("dataApi.json", "w")
    # magic happens here to make it pretty-printed
    weatherDataFile.write(simplejson.dumps(
        json_data, indent=4, sort_keys=True))
    weatherDataFile.close()

    # %% Fetch tide data

    response = requests.get(
        'https://api.stormglass.io/v2/tide/extremes/point',
        params={
            'lat': 47.72,
            'lng': -3.49,
            'start': start.to('UTC').timestamp(),  # Convert to UTC timestamp
            'end': end.to('UTC').timestamp(),  # Convert to UTC timestam
        },
        headers={
            'Authorization': apiKey
        }
    )
    return HttpResponse("Hello, world")
