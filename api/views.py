from django.http import HttpResponse
from .serializers import TideSerializer, WeatherSerializer, WaveSerializer
import requests
import arrow
import pandas as pd
import json
from decimal import Decimal
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
            'start': start.to('UTC').timestamp,  # Convert to UTC timestamp
            'end': end.to('UTC').timestamp,  # Convert to UTC timestam
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

    flattened_data['date'], flattened_data['hour'] = flattened_data['time'].str.split(
        ' ', 1).str
    flattened_data.pop("time")

    cleanjson = json.loads(flattened_data.to_json(orient="records"))

    for point in cleanjson:
        Tide_serializer = TideSerializer(data=point)
        if Tide_serializer.is_valid():
            embed = Tide_serializer.save()
            print('Muy bueno')
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
            print('Muy bueno')
        else:
            print(Wave_serializer.errors)

    for point in cleanjson:
        Weather_serializer = WeatherSerializer(data=point)
        if Weather_serializer.is_valid():
            embed = Weather_serializer.save()
            print('Muy bueno')
        else:
            print(Weather_serializer.errors)

    return True


"""
        for datapoint in cleanjson:
            wavedata = Wave(
                beach=beach,
                date=datapoint['date'],
                time=datapoint['hour'],
                wave_direction=datapoint['waveDirection'],
                wave_height=datapoint['waveHeight'],
                wave_period=datapoint['wavePeriod'],
                water_temperature=datapoint['waterTemperature']
            )
            wavedata.save()

    return HttpResponse("Hello, world") """

# %% tide data


'''     with open("dataTideApi.json", "r") as json_file:
        tides = json.load(json_file)
        
    testdata = tides["data"]
    flattened_data = pd.json_normalize(testdata)
    col_one_list = flattened_data['time'].tolist()
    col_one_list = [((arrow.get(hour)).shift(hours=+2)).format('YYYY-MM-DD HH:mm') for hour in col_one_list]
    flattened_data["time"] = col_one_list

    flattened_data['date'], flattened_data['hour'] = flattened_data['time'].str.split(' ', 1).str
    flattened_data.pop("time")

    cleanjson = json.loads(flattened_data.to_json(orient="records"))

    # now write output to a file
    cleandata = open("tides.json", "w")
    # magic happens here to make it pretty-printed
    cleandata.write(simplejson.dumps(cleanjson, indent=4, sort_keys=True))
    cleandata.close() '''

'''     # %% Fetch tide data

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
    ) '''
