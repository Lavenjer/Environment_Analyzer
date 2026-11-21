from django.db import models


class OpenMeteoEcosystemData(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField()

    #Atmosphere and Climate
    precipitation_sum = models.FloatField(null=True, blank=True)
    soil_moisture_7cm = models.FloatField(null=True, blank=True)
    soil_temperature_7cm = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']
        unique_together = ('latitude', 'longitude', 'timestamp')

    def __str__(self):
        return f"Open-Meteo ({self.latitude}, {self.longitude}) @ {self.timestamp}"

class WorldBankEnvironmentData(models.Model):
    country_iso3 = models.CharField(max_length=3, default="USA")
    year = models.IntegerField()

    co2_emissions = models.FloatField(null=True, blank=True)
    forest_cover_percent = models.FloatField(null=True, blank=True)
    protected_biodiversity_percent = models.FloatField(null=True, blank=True)
    water_stress = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['country_iso3', '-year']
        unique_together = ('country_iso3', 'year')

    def __str__(self):
        return f"{self.country_iso3} ({self.year})"
