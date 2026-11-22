import requests
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from analyzer.models import OpenMeteoEcosystemData, WorldBankEnvironmentData


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--lat", type=float, required=True)
        parser.add_argument("--lon", type=float, required=True)
        parser.add_argument("--country", type=str, default="US")

    def handle(self, *args, **options):
        lat = round(options["lat"], 2)
        lon = round(options["lon"], 2)
        country = options["country"].upper()

        self.fetch_open_meteo_forecast(lat, lon)

        # Only fetch USA World Bank data once (it is national and annual)
        if not WorldBankEnvironmentData.objects.filter(country_iso3="USA").exists():
            self.fetch_world_bank(country="USA", date_range="2015:2024")

        self.stdout.write(self.style.SUCCESS(f"Data ready for ({lat}, {lon}) [country]"))

    def fetch_open_meteo_forecast(self, lat, lon):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "forecast_days": 7,
            "daily": ["precipitation_sum"],
            "hourly": ["soil_moisture_3_to_9cm", "soil_temperature_6cm"],
            "timezone": "auto",
        }
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        daily = data.get("daily", {})
        hourly = data.get("hourly", {})

        # Map each date ("YYYY-MM-DD") to its 00:00 index in the hourly array
        midnight_idx = {
            t[:10]: i for i, t in enumerate(hourly.get("time", [])) if t.endswith("T00:00")
        }

        for i, date_str in enumerate(daily.get("time", [])):
            h_idx = midnight_idx.get(date_str)
            dt = make_aware(datetime.strptime(date_str, "%Y-%m-%d"))

            OpenMeteoEcosystemData.objects.update_or_create(
                latitude=lat,
                longitude=lon,
                timestamp=dt,
                defaults={
                    "precipitation_sum": daily["precipitation_sum"][i],
                    "soil_moisture_7cm": (
                        hourly["soil_moisture_3_to_9cm"][h_idx]
                        if h_idx is not None
                        else None
                    ),
                    "soil_temperature_7cm": (
                        hourly["soil_temperature_6cm"][h_idx]
                        if h_idx is not None
                        else None
                    ),
                },
            )
        self.stdout.write(f"Saved {len(daily.get('time', []))} Open-Meteo forecast rows.")

    def fetch_world_bank(self, country, date_range):
        indicators = {
            "co2_emissions": "EN.GHG.CO2.MT.CE.AR5",
            "forest_cover_percent": "AG.LND.FRST.ZS",
            "protected_biodiversity_percent": "ER.LND.PTLD.ZS",
            "water_stress": "ER.H2O.FWST.ZS",
        }

        yearly_data = {}
        for field_name, code in indicators.items():
            url = f"https://api.worldbank.org/v2/country/{country}/indicator/{code}"
            params = {"format": "json", "date": date_range, "per_page": 100}
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            payload = response.json()

            # World Bank v2 returns [metadata, [records...]]
            if len(payload) < 2 or not payload[1]:
                continue

            for entry in payload[1]:
                year = int(entry["date"])
                yearly_data.setdefault(year, {})[field_name] = entry["value"]

        for year, fields in yearly_data.items():
            WorldBankEnvironmentData.objects.update_or_create(
                country_iso3=country,
                year=year,
                defaults=fields,
            )
        self.stdout.write(f"Saved {len(yearly_data)} World Bank rows for {country}.")