from django.contrib import admin

from .models import Beach, Wave, Weather, Tide


class BeachAdmin(admin.ModelAdmin):
    pass


admin.site.register(Beach, BeachAdmin)


class WaveAdmin(admin.ModelAdmin):
    pass


admin.site.register(Wave, WaveAdmin)


class WeatherAdmin(admin.ModelAdmin):
    pass


admin.site.register(Weather, WeatherAdmin)


class TideAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tide, TideAdmin)
