
class SightAdjustment():

    def __init__(self,horizontal,vertical,units):
        if units[0] == "cm" and units[1] == "cm":
            self.vertical = vertical / 100
            self.horizontal = horizontal / 100
        elif units[0] == "cm" and units[1] == "in":
            self.vertical = vertical *0.0254
            self.horizontal = horizontal *0.0254
        elif units[0] == "in" and units[1] == "cm":
            self.vertical = vertical * 0.0254
            self.horizontal = horizontal / 100
        else:
            self.vertical = vertical * 0.0254
            self.horizontal = horizontal * 0.0254

    def sightadjust(self,distance,dist_unit):
        adjustments = []
        #MOA adjustment is 1/4MOA per inch at 100yds
        #MIL adjustment 0.1mil = 1cm at 100m
        #1 MOA = 1/60 degree = 0.0002907rad
        #1 MIL = 0.001 rad
        #3.4395 MOA in a MIL
        #Horizontal or vertical displacement = distance*angle(radians)
        #STD units is meters, convert everything afterward
        if dist_unit == "yd":
            distance = 0.9144*distance

        horizontal_mil = round(self.horizontal / distance * 1000, 2)
        vertical_mil = round(self.vertical / distance * 1000, 2)

        horizontal_moa = round(horizontal_mil * 3.4395, 2)
        vertical_moa = round(vertical_mil * 3.4395, 2)

        adjustments.append(horizontal_mil)
        adjustments.append(vertical_mil)
        adjustments.append(horizontal_moa)
        adjustments.append(vertical_moa)
        return adjustments
