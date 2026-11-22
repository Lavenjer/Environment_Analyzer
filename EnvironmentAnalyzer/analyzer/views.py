import requests
from django.core.management import call_command
from django.shortcuts import render
from .models import OpenMeteoEcosystemData, WorldBankEnvironmentData


def _get_city_data(city_query):
    """Geocode a US city, fetch/cache Open-Meteo & World Bank data, and return querysets."""
    city_display = None
    error_msg = None

    if city_query:
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {
            "name": city_query,
            "count": 1,
            "language": "en",
            "format": "json",
            "countryCode": "US",
        }
        try:
            res = requests.get(geo_url, params=params, timeout=10)
            res.raise_for_status()
            results = res.json().get("results")

            if results:
                match = results[0]
                lat = round(match["latitude"], 2)
                lon = round(match["longitude"], 2)
                city_display = f"{match['name']}, {match.get('admin1', 'USA')}"

                if not OpenMeteoEcosystemData.objects.filter(
                    latitude=lat, longitude=lon
                ).exists():
                    call_command("fetch_data", lat=lat, lon=lon)

                meteo_data = OpenMeteoEcosystemData.objects.filter(
                    latitude=lat, longitude=lon
                )
            else:
                error_msg = f"Could not find a U.S. city named '{city_query}'."
                meteo_data = OpenMeteoEcosystemData.objects.none()
        except requests.RequestException:
            error_msg = "Geocoding service failed. Please try again."
            meteo_data = OpenMeteoEcosystemData.objects.none()
    else:
        meteo_data = OpenMeteoEcosystemData.objects.all()

    wb_data = WorldBankEnvironmentData.objects.all()
    return meteo_data, wb_data, city_display, error_msg


def index(request):
    return render(request, "analyzer/index.html")


def page(request):
    city_query = request.GET.get("city", "").strip()
    meteo_data, wb_data, city_display, error_msg = _get_city_data(city_query)

    context = {
        "meteo_data": meteo_data,
        "wb_data": wb_data,
        "city_query": city_query,
        "city_display": city_display,
        "error_msg": error_msg,
    }
    return render(request, "analyzer/page.html", context)


def analysis(request):
    city_query = request.GET.get("city", "").strip()
    meteo_data, wb_data, city_display, error_msg = _get_city_data(city_query)

    # TODO: Call your services/ environment index function here using meteo_data & wb_data

    context = {
        "meteo_data": meteo_data,
        "wb_data": wb_data,
        "city_query": city_query,
        "city_display": city_display,
        "error_msg": error_msg,
    }
    return render(request, "analyzer/analysis.html", context)


def acknowledgements(request):
    return render(request, "analyzer/acknowledgements.html")
#This file connects the urls.py and models.py to the html files.