from .SoilAndPrecipitation import Soil_and_Precipitation
from .EnvironmentData import EnvironmentData


def EvaluationScale(meteo_data, wb_data):
    """
    Calculates the weighted Environment Index (0-100) using Open-Meteo (40%)
    and World Bank (60%) querysets from views.py.
    """
    if not meteo_data.exists() and not wb_data.exists():
        return None

    # 1. Extract 7-day averages from Open-Meteo queryset
    moistures = [r.soil_moisture_7cm for r in meteo_data if r.soil_moisture_7cm is not None]
    temps = [r.soil_temperature_7cm for r in meteo_data if r.soil_temperature_7cm is not None]
    precips = [r.precipitation_sum for r in meteo_data if r.precipitation_sum is not None]

    # Convert Open-Meteo soil moisture (m3/m3) to percentage (0-100) for Soil_and_Precipitation
    avg_moisture_pct = (sum(moistures) / len(moistures)) * 100 if moistures else 0
    avg_temp = sum(temps) / len(temps) if temps else 0
    total_precip = sum(precips) if precips else 0

    soil_eval = Soil_and_Precipitation(
        soil_moisture_rate=avg_moisture_pct,
        soil_temp=avg_temp,
        precipitation=total_precip,
    )

    moisture_score = soil_eval.soil_moisture_evaluation() or 0
    temp_score = soil_eval.soil_temperature_evaluation() or 0
    precip_score = soil_eval.precipitation_evaluation() or 0
    soil_precip_score = moisture_score + temp_score + precip_score

    # 2. Extract latest non-null values from World Bank queryset (ordered newest-first)
    co2_val = next((r.co2_emissions for r in wb_data if r.co2_emissions is not None), 0)
    forest_val = next((r.forest_cover_percent for r in wb_data if r.forest_cover_percent is not None), 0)
    biodiv_val = next((r.protected_biodiversity_percent for r in wb_data if r.protected_biodiversity_percent is not None), 0)
    water_val = next((r.water_stress for r in wb_data if r.water_stress is not None), 0)

    env_eval = EnvironmentData(
        co2_emission=co2_val,
        forest_cover=forest_val,
        protected_biodiv=biodiv_val,
        water_stress=water_val,
    )

    co2_score = env_eval.co2_emissions() or 0
    forest_score = env_eval.forest_cover() or 0
    biodiv_score = env_eval.protected_biodiversity() or 0
    water_score = env_eval.water_stress() or 0
    environment_score = co2_score + forest_score + biodiv_score + water_score

    # 3. Weighted final score (40% Soil/Precip out of 8, 60% Environment out of 18)
    soil_precip_totalScale = 8
    environment_totalScale = 18

    final_score = round(
        ((soil_precip_score / soil_precip_totalScale) * 40)
        + ((environment_score / environment_totalScale) * 60),
        1,
    )

    return {
        "final_score": final_score,
        "soil_precip_score": soil_precip_score,
        "soil_precip_max": soil_precip_totalScale,
        "environment_score": environment_score,
        "environment_max": environment_totalScale,
        "breakdown": {
            "moisture_score": moisture_score,
            "temp_score": temp_score,
            "precip_score": precip_score,
            "co2_score": co2_score,
            "forest_score": forest_score,
            "biodiv_score": biodiv_score,
            "water_score": water_score,
        },
    }
