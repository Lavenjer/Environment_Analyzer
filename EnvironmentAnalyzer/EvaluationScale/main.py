from SoilAndPrecipitation import Soil_and_Precipitation
from EnvironmentData import EnvironmentData


def EvaluationScale():
    # Overall Evaluation Scale will split between Soil-Precipitation and 
    # Environment Data Sample.
    soil_precip_totalScale = 8
    environment_totalScale = 18
    total_evaluationScale = soil_precip_totalScale + environment_totalScale

    # In this case, we will prioritize Environment Data making up 60% of the scale, 
    # and Soil-Precipitation data making up 40% of the scale.
    
    pass

if __name__ == "__main__":
    # Testing cases
    a = Soil_and_Precipitation(soil_moisture_rate=12,soil_temp=22,precipitation=11)
    print(f"""
        moisture evaluation: {a.soil_moisture_evaluation()}
        temperature evaluation: {a.soil_temperature_evaluation()}
        precipitation evaluation: {a.precipitation_evaluation()}
    """)

    b = EnvironmentData(co2_emission=1000,forest_cover=30,protected_biodiv=20,water_stress=10)
    print(f"""
        co2: {b.co2_emissions()}
        forest cover: {b.forest_cover()}
        protected biodiversity: {b.protected_biodiversity()}
        water stress: {b.water_stress()}
        """)
