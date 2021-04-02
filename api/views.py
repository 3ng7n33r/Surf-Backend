from django.http import HttpResponse
from .serializers import TideSerializer, WeatherSerializer, WaveSerializer
import requests
import arrow
import pandas as pd
import json
''' from celery.schedules import crontab
from celery.task import periodic_task '''

from .models import Beach, Wave, Weather, Tide

''' @periodic_task(run_every=crontab(hour=7, minute=30, day_of_week="mon")) '''


def api_call(request):

    beaches = Beach.objects.all()

    for beach in beaches:
        print('start')

        waveweather(beach)
        tiderecorder(beach)

        print('end')

    return HttpResponse("Muy bueno")


def tiderecorder(beach):
    # load API key
    with open("storm_API.txt", "r") as f:
        apiKey = f.read()

    # Get first and last hour of today
    start = arrow.utcnow().replace(hour=0, minute=0, second=0)
    end = start.shift(days=+6)

    response = requests.get(
        'https://api.stormglass.io/v2/tide/extremes/point',
        params={
            'lat': beach.lat,
            'lng': beach.lng,
            'start': start.timestamp(),  # Convert to timestamp
            'end': end.timestamp(),  # Convert to UTC timestamp
        },
        headers={
            'Authorization': apiKey
        }
    )
    json_tides = response.json()['data']

    flattened_data = pd.json_normalize(json_tides)
    col_one_list = flattened_data['time'].tolist()
    col_one_list = [((arrow.get(hour)).shift(hours=+2)
                     ).format('YYYY-MM-DD HH:mm') for hour in col_one_list]
    flattened_data["time"] = col_one_list
    flattened_data.columns = flattened_data.columns.str.replace("type", "tide")
    flattened_data = flattened_data.round(2)

    flattened_data['date'], flattened_data['hour'] = flattened_data['time'].str.split(
        ' ', 1).str
    flattened_data.pop("time")
    flattened_data['beach'] = beach.id

    cleanjson = json.loads(flattened_data.to_json(orient="records"))

    for point in cleanjson:
        Tide_serializer = TideSerializer(data=point)
        if Tide_serializer.is_valid():
            embed = Tide_serializer.save()
        else:
            print(Tide_serializer.errors)

    return True


def waveweather(beach):
    # load API key
    with open("storm_API.txt", "r") as f:
        apiKey = f.read()

    # Get first and last hour of today
    start = arrow.utcnow().replace(hour=0, minute=0, second=0)
    end = start.shift(days=+6)

    response = requests.get(
        'https://api.stormglass.io/v2/weather/point',
        params={
            'lat': beach.lat,
            'lng': beach.lng,
            'params': ','.join(['waveHeight', 'airTemperature', 'cloudCover',
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

    data = response.json()['hours']

    flattened_data = pd.json_normalize(data)
    flatClean = pd.DataFrame()

    col_one_list = flattened_data['time'].tolist()

    col_one_list = [((arrow.get(hour)).shift(hours=+2)
                     ).format('YYYY-MM-DD HH:mm') for hour in col_one_list]
    flattened_data["time"] = col_one_list

    # Remove noaa from column header
    for i in flattened_data:
        flattened_data.rename(
            columns={i: i.split('.', 1)[0]}, inplace=True)

    # Delete all but the selected hours
    flattened_data['date'], flattened_data['hour'] = flattened_data['time'].str.split(
        ' ', 1).str
    flattened_data.pop("time")
    hour = ["06:00",
            "09:00",
            "12:00",
            "15:00",
            "18:00",
            "21:00",
            ]
    flatClean = flattened_data[flattened_data.hour.isin(hour)]
    flatClean['beach'] = beach.id

    cleanjson = json.loads(flatClean.to_json(orient="records"))

    for point in cleanjson:
        Wave_serializer = WaveSerializer(data=point)
        if Wave_serializer.is_valid():
            embed = Wave_serializer.save()
        else:
            print(Wave_serializer.errors)

    return True
