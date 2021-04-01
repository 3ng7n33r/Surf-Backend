from django.db import models

time_choices = [
    ('6', '06:00'),
    ('9', '09:00'),
    ('12', '12:00'),
    ('15', '15:00'),
    ('18', '18:00'),
    ('21', '21:00'),
]


class Beach(models.Model):
    name = models.CharField(max_length=50)
    # ° from -90 to 90
    lat = models.DecimalField(max_digits=6, decimal_places=4)
    # ° from -180 to 180
    lng = models.DecimalField(max_digits=7, decimal_places=4)
    # ° from 0(facing N) to 360
    orientation = models.DecimalField(max_digits=7, decimal_places=4)

    def __str__(self):
        return self.name


class Tide(models.Model):
    beach = models.ForeignKey(Beach, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.CharField(max_length=5, choices=time_choices)
    tide_choices = [
        ('0', 'low'),
        ('1', 'high')
    ]
    tide = models.CharField(max_length=5, choices=tide_choices)
    tide_height = models.DecimalField(max_digits=5, decimal_places=2)  # in m

    def __str__(self):
        return str(self.beach) + " - " + str(self.date) + " - " + str(self.time) + ":00"


class Weather(models.Model):
    beach = models.ForeignKey(Beach, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.CharField(max_length=5, choices=time_choices)
    # in °C
    air_temperature = models.DecimalField(max_digits=4, decimal_places=2)
    cloud_cover = models.DecimalField(max_digits=5, decimal_places=2)  # in %
    # in m/s
    windSpeed = models.DecimalField(max_digits=5, decimal_places=2)
    # in ° from 0 (from N) to 360
    windDirection = models.DecimalField(max_digits=7, decimal_places=4)

    def __str__(self):
        return str(self.beach) + " - " + str(self.date) + " - " + str(self.time) + ":00"


class Wave(models.Model):
    beach = models.ForeignKey(Beach, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.CharField(max_length=5, choices=time_choices)
    # in ° from 0 (from N) to 360
    waveDirection = models.DecimalField(max_digits=7, decimal_places=4)
    waveHeight = models.DecimalField(max_digits=5, decimal_places=2)  # in m
    wavePeriod = models.DecimalField(max_digits=5, decimal_places=2)  # in s
    # in °C
    waterTemperature = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return str(self.beach) + " - " + str(self.time)
