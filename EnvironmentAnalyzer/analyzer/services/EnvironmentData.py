# data gathered from World Bank Environment Data

class EnvironmentData():
    def __init__(self, co2_emission, forest_cover, protected_biodiv, water_stress):
        self.co2 = co2_emission
        self.forest = forest_cover
        self.probiodiv = protected_biodiv
        self.water = water_stress

    def co2_emissions(self):
        # The scale ranges 0-5:
        # 5 if the level is 0-50 Mt co2
        # 4 if the level is 50-200 Mt co2
        # 3 if the level is 200-500 Mt co2
        # 2 if the level is 500-1000 Mt co2
        # 1 if the level is 1000-2500 Mt co2
        # 0 if the level is 2500 Mt co2
        if (self.co2 <= 50): return 5
        elif (self.co2 > 50 and self.co2 <= 200): return 4
        elif (self.co2 > 200 and self.co2 <= 500): return 3
        elif (self.co2 > 500 and self.co2 <= 1000): return 2
        elif (self.co2 > 1000 and self.co2 <= 2500): return 1
        elif (self.co2 > 2500): return 0
        
    def forest_cover(self):
        # In terms of the US, Forest cover roughly 35% of land area.
        # The scale ranges 0-5:
        # 5 if the percentage is 35% or more.
        # 4 if 30-35%
        # 3 if 25-30%
        # 2 if 20-25%
        # 1 if 10-20%
        # 0 if 0-10%
        if (self.forest >= 35): return 5
        elif (self.forest < 35 and self.forest >= 30): return 4
        elif (self.forest < 30 and self.forest >= 25): return 3
        elif (self.forest < 25 and self.forest >= 20): return 2
        elif (self.forest < 20 and self.forest >= 10): return 1
        elif (self.forest < 10 and self.forest >= 0): return 0
        

    def protected_biodiversity(self):
        # The plan for protected biodiversity will be 30% by 2030. 
        # The scale ranges 0-4:
        # 4 if 30% or more
        # 3 if 20-30%
        # 2 if 10-20%
        # 1 if 5-10%
        # 0 if 0-5%
        if (self.probiodiv >= 30): return 4
        elif (self.probiodiv >= 20 and self.probiodiv < 30): return 3
        elif (self.probiodiv >= 10 and self.probiodiv < 20): return 2
        elif (self.probiodiv >= 5 and self.probiodiv < 10): return 1
        elif (self.probiodiv >= 0 and self.probiodiv < 5): return 0
        

    def water_stress(self):
        # Water stress thresholds starts at 25%
        # The scale ranges 0-4:
        # 4 if 0-10%
        # 3 if 10-20%
        # 2 if 20-40%
        # 1 if 40-80%
        # 0 if greater than 80%
        if (self.water >= 0 and self.water <= 10): return 4
        if (self.water > 10 and self.water <= 20): return 3
        if (self.water > 20 and self.water <= 40): return 2
        if (self.water > 40 and self.water <= 80): return 1
        if (self.water > 80): return 0
