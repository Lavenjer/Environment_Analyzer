import requests
from django.core.management import call_command
from django.shortcuts import render
from .models import OpenMeteoEcosystemData, WorldBankEnvironmentData
from .services.environmental_index import EvaluationScale


def _get_city_data(city_query, country_query=""):
    """Geocode any global city (supports 'City' or 'City, Country'), fetch/cache data, and return querysets."""
    city_display = None
    error_msg = None

    if city_query:
        # Split "City, Country" if a comma is present
        city_name = city_query
        country_filter = country_query.lower() if country_query else None

        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {
            "name": city_name,
            "count": 10 if country_filter else 1,
            "language": "en",
            "format": "json",
        }
        try:
            res = requests.get(geo_url, params=params, timeout=10)
            res.raise_for_status()
            results = res.json().get("results") or []

            # If user specified a country, match against full country name or 2-letter code
            match = None
            if country_filter:
                for r in results:
                    c_name = r.get("country", "").lower()
                    c_code = r.get("country_code", "").lower()
                    if country_filter in c_name or country_filter == c_code:
                        match = r
                        break
            elif results:
                match = results[0]

            if match:
                lat = round(match["latitude"], 2)
                lon = round(match["longitude"], 2)
                country_code = match.get("country_code", "US").upper()
                country_name = match.get("country", country_code)
                admin1 = match.get("admin1", "")
                city_display = (
                    f"{match['name']}, {admin1} ({country_name})"
                    if admin1
                    else f"{match['name']} ({country_name})"
                )

                missing_meteo = not OpenMeteoEcosystemData.objects.filter(
                    latitude=lat, longitude=lon
                ).exists()
                missing_wb = not WorldBankEnvironmentData.objects.filter(
                    country_iso3=country_code
                ).exists()

                if missing_meteo or missing_wb:
                    call_command("fetch_data", lat=lat, lon=lon, country=country_code)

                meteo_data = OpenMeteoEcosystemData.objects.filter(
                    latitude=lat, longitude=lon
                )
                wb_data = WorldBankEnvironmentData.objects.filter(
                    country_iso3=country_code
                )
            else:
                search_label = f"{city_query}, {country_query}" if country_query else city_query
                error_msg = f"Could not find '{city_query}'. Try 'City' or 'City, Country'."
                meteo_data = OpenMeteoEcosystemData.objects.none()
                wb_data = WorldBankEnvironmentData.objects.none()
        except requests.RequestException:
            error_msg = "Geocoding service failed. Please try again."
            meteo_data = OpenMeteoEcosystemData.objects.none()
            wb_data = WorldBankEnvironmentData.objects.none()
    else:
        meteo_data = OpenMeteoEcosystemData.objects.all()
        wb_data = WorldBankEnvironmentData.objects.all()

    return meteo_data, wb_data, city_display, error_msg


def index(request):
    return render(request, "analyzer/index.html")


def page(request):
    city_query = request.GET.get("city", "").strip()
    country_query = request.GET.get("country", "").strip()
    meteo_data, wb_data, city_display, error_msg = _get_city_data(city_query, country_query)

    context = {
        "meteo_data": meteo_data,
        "wb_data": wb_data,
        "city_query": city_query,
        "country_query": country_query,
        "city_display": city_display,
        "error_msg": error_msg,
    }
    return render(request, "analyzer/page.html", context)


def analysis(request):
    city_query = request.GET.get("city", "").strip()
    country_query = request.GET.get("country", "").strip()
    meteo_data, wb_data, city_display, error_msg = _get_city_data(city_query, country_query)

    score_data = None
    if city_display and not error_msg:
        score_data = EvaluationScale(meteo_data, wb_data)

    context = {
        "meteo_data": meteo_data,
        "wb_data": wb_data,
        "city_query": city_query,
        "country_query": country_query,
        "city_display": city_display,
        "error_msg": error_msg,
        "score_data": score_data,
    }
    return render(request, "analyzer/analysis.html", context)


def acknowledgements(request):
    return render(request, "analyzer/acknowledgements.html")
#This file connects the urls.py and models.py to the html files.