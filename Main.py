import json
import BallisticCalculationClass as BCC
import sight_adjustment as SI

from kivy.app import App
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.config import Config
Builder.load_file('GUI_layout.kv')

Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '640')
Config.set('kivy','window_icon','window_icon.png')
Config.write()

file = "data.json"

class load_json():
    # read JSON file
    def __init__(self):
        self.data = json.load(open(file))

    def write_json(self,json_data):
        with open(file,'w') as outfile:
            json.dump(json_data,outfile)




class ContainerBox(BoxLayout):
    def __init__(self, **kwargs):
        super(ContainerBox, self).__init__(**kwargs)

# Fill in data boxes on right side of GUI with saved data---------------------------------------------------------------
        param_data = load_json()

        if (param_data.data["BallisticSolver"]['parameters']['muzzle_units'] == 'fps'):
            self.ids.paramfps.state = 'down'
            self.ids.parammuzzlevelocity.text = str(int(param_data.data["BallisticSolver"]['parameters']['muzzle_velocity']/0.3048))
        elif (param_data.data["BallisticSolver"]['parameters']['muzzle_units'] == 'mps'):
            self.ids.parammps.state = 'down'
            self.ids.parammuzzlevelocity.text = str(param_data.data["BallisticSolver"]['parameters']['muzzle_velocity'])


        if (param_data.data["BallisticSolver"]['parameters']['elevation_units'] == 'mil'):
            self.ids.paramemil.state = 'down'
            self.ids.paramelevation.text = str(param_data.data["BallisticSolver"]['parameters']['elevation'])
        elif (param_data.data["BallisticSolver"]['parameters']['elevation_units'] == 'moa'):
            self.ids.paramemoa.state = 'down'
            self.ids.paramelevation.text = str(param_data.data["BallisticSolver"]['parameters']['elevation']*3.44)


        if (param_data.data["BallisticSolver"]['parameters']['windage_units'] == 'mil'):
            self.ids.paramwmil.state = 'down'
            self.ids.paramwindage.text = str(param_data.data["BallisticSolver"]['parameters']['windage'])
        elif (param_data.data["BallisticSolver"]['parameters']['windage_units'] == 'moa'):
            self.ids.paramwmoa.state = 'down'
            self.ids.paramwindage.text = str(param_data.data["BallisticSolver"]['parameters']['windage']*3.44)


        if (param_data.data["BallisticSolver"]['parameters']['wind_speed_units'] == 'mph'):
            self.ids.parammph.state = 'down'
            self.ids.paramwindspeed.text = str(round(param_data.data["BallisticSolver"]['parameters']['wind_speed']/0.44704,1))
        elif (param_data.data["BallisticSolver"]['parameters']['windage_units'] == 'kmh'):
            self.ids.paramkmh.state = 'down'
            self.ids.paramwindspeed.text = str(round(param_data.data["BallisticSolver"]['parameters']['wind_speed']/0.277778,1))

        self.ids.paramwindangle.text = str(param_data.data["BallisticSolver"]['parameters']['wind_angle'])

        self.ids.airdensity.text = str(param_data.data["BallisticSolver"]['bullet']['air_density'])
#-----------------------------------------------------------------------------------------------------------------------

    def saveParams(self):
        param_data = load_json()
        #ALWAY SAVE IN STD UNITS (MIL, m/s)

        if (self.ids.paramfps.state == 'down'):
            param_data.data["BallisticSolver"]['parameters']['muzzle_units'] = 'fps'
            param_data.data["BallisticSolver"]['parameters']['muzzle_velocity'] = int(self.ids.parammuzzlevelocity.text)*0.3048
        elif (self.ids.parammps.state == 'down'):
            param_data.data["BallisticSolver"]['parameters']['muzzle_units'] = 'mps'
            param_data.data["BallisticSolver"]['parameters']['muzzle_velocity'] = int(self.ids.parammuzzlevelocity.text)

        if (self.ids.paramemil.state == 'down'):
            param_data.data["BallisticSolver"]['parameters']['elevation_units'] = 'mil'
            param_data.data["BallisticSolver"]['parameters']['elevation'] = float(self.ids.paramelevation.text)
        elif (self.ids.paramemoa.state == 'down'):
            param_data.data["BallisticSolver"]['parameters']['elevation_units'] = 'moa'
            param_data.data["BallisticSolver"]['parameters']['elevation'] = float(self.ids.paramelevation.text)/3.44

        if (self.ids.paramwmil.state == 'down'):
            param_data.data["BallisticSolver"]['parameters']['windage_units'] = 'mil'
            param_data.data["BallisticSolver"]['parameters']['windage'] = float(self.ids.paramwindage.text)
        elif (self.ids.paramwmoa.state == 'down'):
            param_data.data["BallisticSolver"]['parameters']['windage_units'] = 'moa'
            param_data.data["BallisticSolver"]['parameters']['windage'] = float(self.ids.paramwindage.text)/3.44

        if (self.ids.parammph.state == 'down'):
            param_data.data["BallisticSolver"]['parameters']['wind_speed_units'] = 'mph'
            param_data.data["BallisticSolver"]['parameters']['wind_speed'] = float(self.ids.paramwindspeed.text)*0.44704
        elif (self.ids.paramkmh.state == 'down'):
            param_data.data["BallisticSolver"]['parameters']['windage_units'] = 'kmh'
            param_data.data["BallisticSolver"]['parameters']['wind_speed'] = float(self.ids.paramwindspeed.text)*0.277778

        param_data.data["BallisticSolver"]['parameters']['wind_angle'] = int(self.ids.paramwindangle.text)

        param_data.data["BallisticSolver"]['bullet']['air_density'] = float(self.ids.airdensity.text)

        param_data.write_json(param_data.data)


    def show_bullet(self):
        self.ids.main.clear_widgets()
        self.ids.main.add_widget(BulletInfo())

    def show_trajectory(self):
        self.ids.main.clear_widgets()
        self.ids.main.add_widget(Trajectory())

    def show_calculate(self):
        self.ids.main.clear_widgets()
        self.ids.main.add_widget(Calculate())

    def show_simulation(self):
        self.ids.main.clear_widgets()
        self.ids.main.add_widget(Simulation())

    def show_sight_in(self):
        self.ids.main.clear_widgets()
        self.ids.main.add_widget(SightIn())

    def show_graph_units(self):
        self.ids.main.clear_widgets()
        self.ids.main.add_widget(GraphUnits())

    def clear_main(self):
        self.ids.main.clear_widgets()


class BulletInfo(BoxLayout):
    def __init__(self, **kwargs):
        super(BulletInfo, self).__init__(**kwargs)
        bullet_data = load_json()
        self.ids.bulletweight.text = str(bullet_data.data["BallisticSolver"]['bullet']['bullet_mass'])
        self.ids.bulletBC.text = str(bullet_data.data["BallisticSolver"]['bullet']['ballistic_coeff'])
        self.ids.bulletdia.text = str(bullet_data.data["BallisticSolver"]['bullet']['bullet_dia'])

        if (bullet_data.data["BallisticSolver"]['bullet']['drag_model'] == "G7"):
            self.ids.dragG7.state = 'down'
        elif (bullet_data.data["BallisticSolver"]['bullet']['drag_model'] == "G1"):
            self.ids.dragG1.state = 'down'

    def saveBullet(self):
        bullet_data = load_json()
        bullet_data.data["BallisticSolver"]['bullet']['bullet_mass'] = int(self.ids.bulletweight.text)
        bullet_data.data["BallisticSolver"]['bullet']['ballistic_coeff'] = float(self.ids.bulletBC.text)
        bullet_data.data["BallisticSolver"]['bullet']['bullet_dia'] = float(self.ids.bulletdia.text)

        if (self.ids.dragG7.state == 'down'):
            bullet_data.data["BallisticSolver"]['bullet']['drag_model'] = "G7"
        elif (self.ids.dragG1.state == 'down'):
            bullet_data.data["BallisticSolver"]['bullet']['drag_model'] = "G1"

        bullet_data.write_json(bullet_data.data)

class Trajectory(BoxLayout):
    def __init__(self, **kwargs):
        super(Trajectory, self).__init__(**kwargs)

    def plotTrajectory(self):
        trajectoryData = load_json()

        velocity = int(trajectoryData.data["BallisticSolver"]['parameters']['muzzle_velocity'])
        bullet = trajectoryData.data["BallisticSolver"]['bullet']
        elevation = float(trajectoryData.data["BallisticSolver"]['parameters']['elevation'])
        windage = float(trajectoryData.data["BallisticSolver"]['parameters']['windage'])
        ballisticsolver = BCC.Trajectory(velocity,bullet,elevation,windage)

        ballisticsolver.crosswind = float(trajectoryData.data["BallisticSolver"]['parameters']['wind_speed'])
        ballisticsolver.windDirection = int(trajectoryData.data["BallisticSolver"]['parameters']['wind_angle'])

        elevationUnits = trajectoryData.data["BallisticSolver"]['graphUnits']['elevation_units']
        distanceUnits = trajectoryData.data["BallisticSolver"]['graphUnits']['distance_units']
        ballisticsolver.graphUnits(elevationUnits, distanceUnits)

        if (self.ids.trajectory3d.state == 'down' and self.ids.excelfile.state == 'down'):
            ballisticsolver.trajectoryGraph(True, True, True)
        elif (self.ids.excelfile.state == 'down'):
            ballisticsolver.trajectoryGraph(True, False, True)
        elif(self.ids.trajectory3d.state == 'down'):
            ballisticsolver.trajectoryGraph(True, True)
        else:
            ballisticsolver.trajectoryGraph(True)


class Calculate(BoxLayout):
    def __init__(self, **kwargs):
        super(Calculate, self).__init__(**kwargs)
        calculate_data = load_json()

        self.ids.calculatedistance.text = str(calculate_data.data["BallisticSolver"]['calculate']['distance'])

        if(calculate_data.data["BallisticSolver"]['calculate']['unit'] == 'yd'):
            self.ids.calculateyd.state = 'down'

        elif(calculate_data.data["BallisticSolver"]['calculate']['unit'] == 'm'):
            self.ids.calculatem.state = 'down'


    def runCalculation(self):

#SAVE CALCULATION PARAMETERS FOR NEXT TIME------------------------------------------------------------------------------
        calculate_data = load_json()

        calculate_data.data["BallisticSolver"]['calculate']['distance'] = int(self.ids.calculatedistance.text)

        if (self.ids.calculateyd.state == 'down'):
            calculate_data.data["BallisticSolver"]['calculate']['unit'] = 'yd'
        elif (self.ids.calculatem.state == 'down'):
            calculate_data.data["BallisticSolver"]['calculate']['unit'] = 'm'


        calculate_data.write_json(calculate_data.data)
#-----------------------------------------------------------------------------------------------------------------------
        trajectoryData = load_json()
        velocity = int(trajectoryData.data["BallisticSolver"]['parameters']['muzzle_velocity'])
        bullet = trajectoryData.data["BallisticSolver"]['bullet']
        elevation = float(trajectoryData.data["BallisticSolver"]['parameters']['elevation'])
        windage = float(trajectoryData.data["BallisticSolver"]['parameters']['windage'])

        ballisticsolver = BCC.Trajectory(velocity, bullet, elevation, windage)

        ballisticsolver.crosswind = float(trajectoryData.data["BallisticSolver"]['parameters']['wind_speed'])
        ballisticsolver.windDirection = int(trajectoryData.data["BallisticSolver"]['parameters']['wind_angle'])


        distanceUnits = trajectoryData.data["BallisticSolver"]['graphUnits']['distance_units']
        if(calculate_data.data["BallisticSolver"]['calculate']['unit'] == 'yd'):
            distance = trajectoryData.data["BallisticSolver"]['calculate']['distance']/1.09361
            distanceUnits = 'yd'
        else:
            distance = trajectoryData.data["BallisticSolver"]['calculate']['distance']


        elevationUnits = trajectoryData.data["BallisticSolver"]['graphUnits']['elevation_units']
        ballisticsolver.graphUnits(elevationUnits, distanceUnits)

        if(self.ids.calculate3d.state == 'down'):
            adjustments = ballisticsolver.calculation(distance,True)
        else:
            adjustments = ballisticsolver.calculation(distance,False)

        self.ids.calculateEAdjustMoa.text = str(adjustments["elevation"]*3.44) + " MOA"
        self.ids.calculateEAdjustMil.text = str(adjustments["elevation"]) + " MIL"

        self.ids.calculateWAdjustMoa.text = str(adjustments["windage"]*3.44) + " MOA"
        self.ids.calculateWAdjustMil.text = str(adjustments["windage"]) + " MIL"




class Simulation(BoxLayout):
    def __init__(self, **kwargs):
        super(Simulation, self).__init__(**kwargs)
        simulation_data = load_json()

        self.ids.simulationd.text = str(simulation_data.data["BallisticSolver"]['simulation']['distance'])
        if (simulation_data.data["BallisticSolver"]['simulation']['d_unit'] == 'yd'):
            self.ids.simulationyd.state = 'down'
        elif (simulation_data.data["BallisticSolver"]['simulation']['d_unit'] == 'm'):
            self.ids.simulationm.state = 'down'

        if (simulation_data.data["BallisticSolver"]['simulation']['SDV_unit'] == 'fps'):
            self.ids.simulationfps.state = 'down'
            self.ids.simulationsdv.text = str(simulation_data.data["BallisticSolver"]['simulation']['SDV']/0.3048)
        elif (simulation_data.data["BallisticSolver"]['simulation']['SDV_unit'] == 'mps'):
            self.ids.simulationms.state = 'down'
            self.ids.simulationsdv.text = str(simulation_data.data["BallisticSolver"]['simulation']['SDV'])

        if (simulation_data.data["BallisticSolver"]['simulation']['SDW_unit'] == 'mph'):
            self.ids.simulationmph.state = 'down'
            self.ids.simulationsdw.text = str(round(simulation_data.data["BallisticSolver"]['simulation']['SDW']/0.44704,1))
        elif (simulation_data.data["BallisticSolver"]['simulation']['SDW_unit'] == 'kmh'):
            self.ids.simulationkmh.state = 'down'
            self.ids.simulationsdw.text = str(round(simulation_data.data["BallisticSolver"]['simulation']['SDW']/0.277778,1))

        self.ids.simulationsdwa.text = str(simulation_data.data["BallisticSolver"]['simulation']['SDWA'])

        self.ids.simulationnumshots.text = str(simulation_data.data["BallisticSolver"]['simulation']['num_shots'])


    def runSimulation(self):

#SAVE SIMULATION PARAMETERS FOR NEXT TIME-------------------------------------------------------------------------------
        simulation_data = load_json()

        simulation_data.data["BallisticSolver"]['simulation']['distance'] = int(self.ids.simulationd.text)
        if (self.ids.simulationyd.state == 'down'):
            simulation_data.data["BallisticSolver"]['simulation']['d_unit'] = 'yd'
        elif (self.ids.simulationm.state == 'down'):
            simulation_data.data["BallisticSolver"]['simulation']['d_unit'] = 'm'

        if (self.ids.simulationfps.state == 'down'):
            simulation_data.data["BallisticSolver"]['simulation']['SDV_unit'] = 'fps'
            simulation_data.data["BallisticSolver"]['simulation']['SDV'] = float(self.ids.simulationsdv.text)*0.3048
        elif (self.ids.simulationms.state == 'down'):
            simulation_data.data["BallisticSolver"]['simulation']['SDV_unit'] = 'mps'
            simulation_data.data["BallisticSolver"]['simulation']['SDV'] = float(self.ids.simulationsdv.text)


        if (self.ids.simulationmph.state == 'down'):
            simulation_data.data["BallisticSolver"]['simulation']['SDW_unit'] = 'mph'
            simulation_data.data["BallisticSolver"]['simulation']['SDW'] = float(self.ids.simulationsdw.text)*0.44704
        elif (self.ids.simulationkmh.state == 'down'):
            simulation_data.data["BallisticSolver"]['simulation']['SDW_unit'] = 'kmh'
            simulation_data.data["BallisticSolver"]['simulation']['SDW'] = float(self.ids.simulationsdw.text)*0.277778

        simulation_data.data["BallisticSolver"]['simulation']['SDWA'] = float(self.ids.simulationsdwa.text)

        simulation_data.data["BallisticSolver"]['simulation']['num_shots'] = int(self.ids.simulationnumshots.text)

        simulation_data.write_json(simulation_data.data)

#-----------------------------------------------------------------------------------------------------------------------

        trajectoryData = load_json()
        velocity = int(trajectoryData.data["BallisticSolver"]['parameters']['muzzle_velocity'])
        bullet = trajectoryData.data["BallisticSolver"]['bullet']
        elevation = float(trajectoryData.data["BallisticSolver"]['parameters']['elevation'])
        windage = float(trajectoryData.data["BallisticSolver"]['parameters']['windage'])
        ballisticsolver = BCC.Trajectory(velocity, bullet, elevation, windage)

        ballisticsolver.crosswind = float(trajectoryData.data["BallisticSolver"]['parameters']['wind_speed'])
        ballisticsolver.windDirection = int(trajectoryData.data["BallisticSolver"]['parameters']['wind_angle'])

        elevationUnits = trajectoryData.data["BallisticSolver"]['graphUnits']['elevation_units']

        if(trajectoryData.data["BallisticSolver"]['simulation']['d_unit'] == 'yd'):
            distance = trajectoryData.data["BallisticSolver"]['simulation']['distance']/1.09361
        else:
            distance = trajectoryData.data["BallisticSolver"]['calculate']['distance']

        distance_unit = trajectoryData.data["BallisticSolver"]['simulation']['d_unit']

        SD_v = trajectoryData.data["BallisticSolver"]['simulation']['SDV']

        SDWind_v = trajectoryData.data["BallisticSolver"]['simulation']['SDW']
        SDWind_angle = trajectoryData.data["BallisticSolver"]['simulation']['SDWA']
        num_shots = trajectoryData.data["BallisticSolver"]['simulation']['num_shots']

        ballisticsolver.graphUnits(elevationUnits,distance_unit)

        if(self.ids.simulationTPaths.state == 'down'):
            ballisticsolver.shotProbability(distance,distance_unit,SD_v,SDWind_v,SDWind_angle,num_shots,True)
        else:
            ballisticsolver.shotProbability(distance,distance_unit,SD_v,SDWind_v,SDWind_angle,num_shots)

class SightIn(BoxLayout):
    def __init__(self, **kwargs):
        super(SightIn, self).__init__(**kwargs)


    def runSight(self):
        distance = int(self.ids.sightdistance.text)

        if self.ids.sightyd.state == "down":
            dist_unit = "yd"
        else:
            dist_unit = "m"

        vertical_dist = float(self.ids.sightverticaldistance.text)

        if self.ids.sightvin.state == "down":
            vertical_unit = "in"
        else:
            vertical_unit = "cm"

        horizontal_dist = float(self.ids.sighthorizontaldistance.text)

        if self.ids.sighthin.state == "down":
            horizontal_unit = "in"
        else:
            horizontal_unit = "cm"

        units = []
        units.append(vertical_unit)
        units.append(horizontal_unit)

        Sight = SI.SightAdjustment(horizontal_dist,vertical_dist,units)
        adjustments = Sight.sightadjust(distance,dist_unit)

        self.ids.sightEAdjustMoa.text = str(adjustments[3]) + " MOA"
        self.ids.sightEAdjustMil.text = str(adjustments[1]) + " MIL"
        self.ids.sightWAdjustMoa.text = str(adjustments[2]) + " MOA"
        self.ids.sightWAdjustMil.text = str(adjustments[0]) + " MIL"


class GraphUnits(BoxLayout):
    def __init__(self, **kwargs):
        super(GraphUnits, self).__init__(**kwargs)

        graphData = load_json()
        if (graphData.data["BallisticSolver"]['graphUnits']['elevation_units'] == 'in'):
            self.ids.graphElevationIn.state = 'down'
        elif (graphData.data["BallisticSolver"]['graphUnits']['elevation_units'] == 'cm'):
            self.ids.graphElevationCm.state = 'down'

        if (graphData.data["BallisticSolver"]['graphUnits']['windage_units'] == 'in'):
            self.ids.graphWindageIn.state = 'down'
        elif (graphData.data["BallisticSolver"]['graphUnits']['windage_units'] == 'cm'):
            self.ids.graphWindageCm.state = 'down'

        if (graphData.data["BallisticSolver"]['graphUnits']['distance_units'] == 'yd'):
            self.ids.graphDistanceYd.state = 'down'
        elif (graphData.data["BallisticSolver"]['graphUnits']['distance_units'] == 'm'):
            self.ids.graphDistanceM.state = 'down'

    def saveGraphUnits(self):
        graphData = load_json()
        if (self.ids.graphElevationIn.state == 'down'):
            graphData.data["BallisticSolver"]['graphUnits']['elevation_units'] = 'in'
        elif (self.ids.graphElevationCm.state == 'down'):
            graphData.data["BallisticSolver"]['graphUnits']['elevation_units'] = 'cm'

        if (self.ids.graphWindageIn.state == 'down'):
            graphData.data["BallisticSolver"]['graphUnits']['windage_units'] = 'in'
        elif (self.ids.graphWindageCm.state == 'down'):
            graphData.data["BallisticSolver"]['graphUnits']['windage_units'] = 'cm'

        if (self.ids.graphDistanceYd.state == 'down'):
            graphData.data["BallisticSolver"]['graphUnits']['distance_units'] = 'yd'
        elif (self.ids.graphDistanceM.state == 'down'):
            graphData.data["BallisticSolver"]['graphUnits']['distance_units'] = 'm'

        graphData.write_json(graphData.data)



class BallisticSolver(App):
    def build(self):
        return ContainerBox()


if __name__ == '__main__':

    BallisticSolver().run()