from django.db import models


class OpenMeteoEcosystemData(models.Model):
    #Location and time
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField()

    #Soil and precipitation data
    precipitation_sum = models.FloatField(null=True, blank=True)
    soil_moisture_7cm = models.FloatField(null=True, blank=True)
    soil_temperature_7cm = models.FloatField(null=True, blank=True)

    class Meta:
        #Organize data by timestamp and filter using the location and time
        ordering = ['-timestamp']
        unique_together = ('latitude', 'longitude', 'timestamp') 

    def __str__(self):
        return f"Open-Meteo ({self.latitude}, {self.longitude}) @ {self.timestamp}"

class WorldBankEnvironmentData(models.Model):
    #Locations and time
    country_iso3 = models.CharField(max_length=3, default="USA")
    year = models.IntegerField()
    
    #Biodiversity, forest cover, CO2 emissions, and water stress values
    co2_emissions = models.FloatField(null=True, blank=True)
    forest_cover_percent = models.FloatField(null=True, blank=True)
    protected_biodiversity_percent = models.FloatField(null=True, blank=True)
    water_stress = models.FloatField(null=True, blank=True)

    class Meta:
        #Organize data by the country and year while only accepting data from that given country (This could use some tweaking)
        ordering = ['country_iso3', '-year']
        unique_together = ('country_iso3', 'year')

    def __str__(self):
        return f"{self.country_iso3} ({self.year})"
