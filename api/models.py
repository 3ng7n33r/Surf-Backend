from django.db import models

time_choices = [
    ('06:00', '06:00'),
    ('09:00', '09:00'),
    ('12:00', '12:00'),
    ('15:00', '15:00'),
    ('18:00', '18:00'),
    ('21:00', '21:00'),
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
    hour = models.CharField(max_length=5)
    tide_choices = [
        ('low', 'low'),
        ('high', 'high')
    ]
    tide = models.CharField(max_length=5, choices=tide_choices)
    height = models.DecimalField(max_digits=5, decimal_places=2)  # in m

    def __str__(self):
        return str(self.beach) + " - " + str(self.date) + " - " + str(self.hour)


class Weather(models.Model):
    beach = models.ForeignKey(Beach, on_delete=models.CASCADE)
    date = models.DateField()
    hour = models.CharField(max_length=5, choices=time_choices)
    # in °C
    airTemperature = models.DecimalField(max_digits=4, decimal_places=2)
    cloudCover = models.DecimalField(max_digits=5, decimal_places=2)  # in %
    # in m/s
    windSpeed = models.DecimalField(max_digits=5, decimal_places=2)
    # in ° from 0 (from N) to 360
    windDirection = models.DecimalField(max_digits=7, decimal_places=4)

    def __str__(self):
        return str(self.beach) + " - " + str(self.date) + " - " + str(self.hour)


class Wave(models.Model):
    beach = models.ForeignKey(Beach, on_delete=models.CASCADE)
    date = models.DateField()
    hour = models.CharField(max_length=5, choices=time_choices)
    # in ° from 0 (from N) to 360
    waveDirection = models.DecimalField(max_digits=7, decimal_places=4)
    waveHeight = models.DecimalField(max_digits=5, decimal_places=2)  # in m
    wavePeriod = models.DecimalField(max_digits=5, decimal_places=2)  # in s
    # in °C
    waterTemperature = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return str(self.beach) + " - " + str(self.date) + " - " + str(self.hour)
