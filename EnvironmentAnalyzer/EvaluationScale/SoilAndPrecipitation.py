class Soil_and_Precipitation:
     
    def __init__(self, soil_moisture_rate, soil_temp, precipitation):
        self.soil_moisture_rate = soil_moisture_rate
        self.soil_temp = soil_temp
        self.precipitation = precipitation

    def soil_moisture_evaluation(self):
        # depending on the plant time and soil type, assume a good soil percentage typically falls between 20% and 40%.
        # The scale ranges 0-3: 
        # 3 if within 20% and 40%;
        # 2 if 10% to less than 20%, or from 40% to less than 70%;
        # 1 if greater than 0% to less than 10%, or 70% to less than 100%;
        # 0 if 0% or 100%
        if (self.soil_moisture_rate >= 20 and self.soil_moisture_rate <= 40):
            return 3
        elif (self.soil_moisture_rate >= 10 and self.soil_moisture_rate < 20) or (self.soil_moisture_rate > 40 and self.soil_moisture_rate <= 70):
            return 2
        elif (self.soil_moisture_rate > 0 and self.soil_moisture_rate < 10) or (self.soil_moisture_rate > 70 and self.soil_moisture_rate < 100):
            return 1
        elif (self.soil_moisture_rate == 0 or self.soil_moisture_rate == 100):
            return 0

    def soil_temperature_evaluation(self):
        # depending on the plant time and soil type, assume a good temperature is 15-30C
        # The scale ranges 0-2:
        # 2 if within 15-30C
        # 1 if within 10-15C or 30-35C
        # 0 if less than 10C or greater than 35C
        if (self.soil_temp >= 15 and self.soil_temp <= 30): return 2
        elif (self.soil_temp >= 10 and self.soil_temp < 15) or (self.soil_temp >= 30 and self.soil_temp <= 35 ): return 1
        elif (self.soil_temp < 10 or self.soil_temp > 35): return 0

    def precipitation_evaluation(self):
        # A good range for precipitation of 7mm soil is typically 10 to 20mm.
        # The scale ranges 0-3:
        # 3 if within 10-20mm
        # 2 if within 5-10mm or 20-40mm
        # 1 if within 0-5mm or 40-60mm
        # 0 if 0mm or more than 60mm
        if (self.precipitation >= 10 and self.precipitation <= 20): return 3
        elif (self.precipitation >=5 and self.precipitation < 10) or (self.precipitation > 20 and self.precipiation <= 40): return 2
        elif (self.precipitation > 0 and self.precipitation < 5) or (self.precipitation > 40 and self.precipitation <= 60): return 1
        elif (self.precipitation == 0 or self.precipitation > 60): return 0
        