import datetime
import BallisticCalculationClass as BCC

#INPUT CONDITIONS
fps = 2930
meters = 800
elevation_mils = 3.5
windage_mils = 0
wind_direction = 0

bullet_stats = {
    "bullet_grains":165,
    "ballistic_coefficient":0.48,
    "bullet_diameter":0.00762,
    "air_density":0.707,
    "drag_coefficient":0.1,
    "cross_area":0.000192
}

calculation = BCC.Trajectory(fps,bullet_stats,elevation_mils,windage_mils,'imp')
calculation.graphUnits('in','yd')
calculation.crosswind = 10
calculation.windDirection = wind_direction
#calculation.trajectoryGraph(True)
calculation.calculation(1000,'yd')
calculation.shotProbability(1000,'yd',45,2,10,10,True)