from rest_framework import serializers
from .models import Beach, Wave, Weather, Tide


class WaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wave
        fields = '__all__'


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = '__all__'


class TideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tide
        fields = '__all__'


class BeachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beach
        fields = '__all__'
