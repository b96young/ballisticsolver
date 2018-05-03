import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from mpl_toolkits.mplot3d import Axes3D
from math import pow as pow
import math,random
import BallisticSolverFunctions as BSF
import csvreader

class Trajectory(object):

    def __init__(self,velocity,bullet,elevation=0,windage=0):
        #Simulation parameters (Runtime = steps*time_interval)
        #Simulation time, defaults 2s
        self.simTime = 2
        self.time_interval = .01
        self.steps = int(math.floor(self.simTime / self.time_interval))

        #ENVIRONMENT & BULLET PARAMETERS
        #CROSSWIND & DIRECTION DEFAULTS 0
        self.crosswind = 0
        self.windDirection = 0
        self.velocity = velocity
        self.elevation_angle = elevation / float(1000)
        self.windage_angle = windage / float(1000)
        self.bullet = bullet

        #Graphing Units
        #Default units are meters, therefore initial conversion factors are 1:1
        self.elevation_conversion = 1
        self.distance_conversion = 1
        self.elevation = 'm'
        self.windage = 'm'
        self.distance = 'm'

        #Create inital lists of trajectory data based on given parameters
        self.graphUnits(self.elevation,self.distance)
        self.trajectoryGraph(False)

    def graphUnits(self,elevation,distance):
        #Elevation defaults to m
        if elevation == 'in':
            self.elevation = 'in'
            self.elevation_conversion = 39.3701
        elif elevation == 'cm':
            self.elevation = 'cm'
            self.elevation_conversion = 100
        elif elevation == 'ft':
            self.elevation = 'ft'
            self.elevation_conversion = 3.28084
        elif elevation == 'yd':
            self.elevation = 'yd'
            self.elevation_conversion = 1.09361
        self.windage = self.elevation
        self.windage_conversion = self.elevation_conversion

        #Distance defaults to m
        if distance == 'mile':
            self.distance = 'miles'
            self.distance_conversion = 0.000621371
        elif distance == 'km':
            self.distance = 'km'
            self.distance_conversion = 0.001
        elif distance == 'yd':
            self.distance = 'yd'
            self.distance_conversion = 1.09361

    def trajectoryGraph(self,displayGraph,plot3D = False):
        # Initialize arrays holding graph data
        self.distance_graph = []
        self.elevation_graph = []
        self.velocity_graph = []
        self.windage_graph = []

        # Initial Conditions
        #STD Units are m/s, if imperial (fps, mph) they are converted
        #Angles converted from degrees to radians

        self.V = self.velocity
        self.windValue = self.crosswind*math.cos(self.windDirection*0.0174533)

        #Initial Distance [y] / Velocity [v] in X, Z components
        #(-1)*sin(Crosswind) since crosswind is defined as 90degrees opposing the bullet velocity
        self.yx0 = 0
        self.vx0 = self.V * math.cos(self.elevation_angle)+ self.crosswind*(-1)*math.sin(self.windDirection*0.0174533)
        self.yz0 = 0
        self.vz0 = self.V * math.sin(self.elevation_angle)

        vxk = self.vx0
        yxk = self.yx0
        #Bullet mass in kg converted from grains
        bullet_mass = self.bullet["bullet_mass"]*0.0000648
        #Bullet diameter from inch to meters
        bullet_dia = self.bullet["bullet_dia"]*0.0254
        #Bullet cross area
        bullet_area = math.pow(bullet_dia,2)*3.14/4
        print (bullet_area)

        for t in range(0,self.steps+1):
            #Calculate BC for the velocity
            ref_cd = csvreader.dragCoefficient(self.bullet["drag_model"],vxk,343)
            drag_coefficient = bullet_mass*ref_cd/self.bullet["ballistic_coeff"]/math.pow(bullet_dia,2)*0.0014223
            print (vxk)
            print (drag_coefficient)

            #CALCULATE BULLET DROP AND VELOCITY
            currentTime = t * float(self.time_interval)
            vxk1 = vxk + self.time_interval*(-0.5*self.bullet["air_density"]*drag_coefficient*bullet_area*pow(vxk,2)/bullet_mass)
            yxk1 = yxk + self.time_interval*(vxk)

            #Calculate Windage Effects (y direction, From right to left is positive direction)
            #Formula uses m/s for windspeed
            #Initial windage adjustment
            yyk = yxk*self.windage_angle
            wind_deflection = (-1)*self.windValue*(t*self.time_interval-yxk/self.V)
            total_deflection = yyk-wind_deflection

            #vxk is instantaneous velocity at current distance down range (x direction)
            #yxk is current distance downrange
            vxk = vxk1
            yxk = yxk1
            # Bullet Drop due to Gravity
            # my'' = -mg
            # y' = -gt + y'(0)

            #vz is instantaneous velocity in z direction at current distance downrange
            #yz is displacement of bullet at current distance downrange
            vz = -9.81*currentTime + self.vz0
            yz = -4.905*pow(currentTime,2) + self.vz0*currentTime + self.yz0

            self.distance_graph.append(yxk1)
            self.elevation_graph.append(yz)
            self.velocity_graph.append(vxk1)
            self.windage_graph.append(total_deflection)

            #Convert all list items using defined conversion factor
        if(displayGraph == True):
            elevation_graph = [x*self.elevation_conversion for x in self.elevation_graph]
            distance_graph = [x*self.distance_conversion for x in self.distance_graph]
            windage_graph = [x * self.elevation_conversion for x in self.windage_graph]

            # PLOT WINDAGE vs DISTANCE
            if plot3D == True:
                ax = plt.axes(projection='3d')
                ax.plot3D(distance_graph, windage_graph, elevation_graph, 'gray')
                # target_data = targetGen(3,1000)
                # ax.plot3D(target_data['x'],target_data['y'],target_data['z'])
                ax.set_xlabel("Distance (" + self.distance + ")")
                ax.set_ylabel("Wind Deflection (" + self.windage + ")")
                ax.set_zlabel("Elevation (" + self.elevation + ")")
                plt.grid(True)
            else:
                # PLOT ELEVATION vs DISTANCE
                trajectoryFig = plt.figure()
                drop = trajectoryFig.add_subplot(211)
                plt.ylabel("Elevation (" + self.elevation + ")")
                plt.margins(0.1, 0.1)
                plt.plot(distance_graph, elevation_graph, 'b-')
                plt.grid(True)

                # PLOT WINDAGE vs DISTANCE
                wind_deflection = trajectoryFig.add_subplot(212, sharex=drop)
                plt.ylabel("Wind Deflection (" + self.windage + ")")
                plt.xlabel("Distance (" + self.distance + ")")
                plt.plot(distance_graph, windage_graph, 'b-')
                plt.grid(True)
            plt.show()

    def calculation(self,distance,plot3D = False):
        adjustments = {"elevation":0,"windage":0}
        stop = False
        previous_elevation_angle = 0
        previous_windage_angle = 0
        #If yards is used for desired distance, convert from meters
        # if unit == 'yd':
        #     distance = distance/1.09361

        while stop != True:
            index = 0
            count = 0
            for item in self.distance_graph:
                if math.fabs(round(item) - round(distance)) < 10.0:
                    index = count
                else:
                    count += 1
            bullet_drop = self.elevation_graph[index]
            drop_adjustment = -1*bullet_drop / distance

            wind_deflection = self.windage_graph[index]
            windage_adjustment = -1*wind_deflection / distance

            if math.fabs(drop_adjustment) > 0.00001:
                self.elevation_angle = previous_elevation_angle + drop_adjustment
                self.trajectoryGraph(False)
                previous_elevation_angle = self.elevation_angle
            elif math.fabs(windage_adjustment) > 0.00001:
                self.windage_angle = previous_windage_angle + windage_adjustment
                self.trajectoryGraph(False)
                previous_windage_angle = self.windage_angle
                # print(self.windage_angle)
            else:
                stop = True
                # if unit == 'yd':
                #     distance = distance*1.09361
                print ("MIL Elevation Adjustment for " + str(distance) + "yd is " + str(round(self.elevation_angle*1000,1)))
                print ("MOA Elevation Adjustment for " + str(distance) + "yd is " + str(round(self.elevation_angle * 1000*3.44, 1)))
                print("MIL Windage Adjustment for " + str(distance) + "yd is " + str(round(self.windage_angle * 1000, 1)))
                print("MOA Windage Adjustment for " + str(distance) + "yd is " + str(round(self.windage_angle * 1000 * 3.44, 1)))
                # else:
                #     print ("MIL Elevation Adjustment for " + str(distance) + "m is " + str(round(self.elevation_angle*1000,1)))
                #     print ("MOA Elevation Adjustment for " + str(distance) + "m is " + str(round(self.elevation_angle * 1000*3.44, 1)))
                #     print("MIL Windage Adjustment for " + str(distance) + "m is " + str(round(self.windage_angle * 1000, 1)))
                #     print("MOA Windage Adjustment for " + str(distance) + "m is " + str(round(self.windage_angle * 1000 * 3.44, 1)))

                adjustments["elevation"] = round(self.elevation_angle*1000,1)
                adjustments["windage"] = round(self.windage_angle * 1000, 1)
                if plot3D == True:
                    self.trajectoryGraph(True,True)
                else:
                    self.trajectoryGraph(True)

                return adjustments

    def shotProbability(self,distance,unit,SD_v,SDWind_v,SDWind_a,simNumber,trajectoryPaths = False):
        shot_info = {}

        # #if distance is in yards, convert to m
        # if unit == 'yd':
        #     distance = distance /1.09361

        #Calculate variable range based on standard deviation
        POI_ycoords = []
        POI_zcoords = []

        #Create 1 MOA target
        #Default distance is in m, get 1 MOA then convert to elevation / windage units
        #1.1457inches / 100m distance
        targetSize = math.ceil(distance/100)*0.0291*self.elevation_conversion

        #Create variable to count number of shots that hit target
        shot_hit = 0

        #Create graph for trajectory data
        if(trajectoryPaths == True):
            simulateTrajectoryFig = plt.figure()
            drop = simulateTrajectoryFig.add_subplot(211)
            drop.set_ylabel("Elevation (" + self.elevation + ")")
            plt.margins(0.1, 0.1)
            plt.grid(True)

            wind_deflection = simulateTrajectoryFig.add_subplot(212, sharex=drop)
            wind_deflection.set_ylabel("Wind Deflection (" + self.windage + ")")
            wind_deflection.set_xlabel("Distance (" + self.distance + ")")
            plt.margins(0.1, 0.1)
            plt.grid(True)

        for trial in range(0,simNumber):
            #Get randomized values for vleocity, windspeed, wind direction
            random_velocity = random.normalvariate(self.velocity,SD_v)
            random_crosswind = random.normalvariate(self.crosswind,SDWind_v)
            random_windDirection = random.normalvariate(self.windDirection,SDWind_a)

            #Keep track of parameters for each shot
            shot_info[trial] = [round(random_velocity,0),round(random_crosswind,1),round(random_windDirection,1)]

            #Calculate POI using trajectoryGraph
            #Set class variables to random variables to calculate trajectory, no need to convert to m/s
            #done in the trajectoryGraph method
            self.velocity = random_velocity
            self.crosswind = random_crosswind
            self.windDirection= random_windDirection
            #Call trajectoryGraph method to get the trajectory data based on the random values
            self.trajectoryGraph(False)

            #Get index of the trajectory info at desired distance (get POI)
            index = 0
            count = 0
            for x in self.distance_graph:
                if math.fabs(round(x) - round(distance)) < 10.0:
                    index = count
                else:
                    count += 1
            #Convert the y,z coordinates into graph units. Ie inches
            y_coord = self.windage_graph[index]*self.elevation_conversion
            z_coord = self.elevation_graph[index]*self.elevation_conversion
            POI_ycoords.append(y_coord)
            POI_zcoords.append(z_coord)

            #Calculate if shot is inside target
            shot_displacement = math.sqrt(math.pow(y_coord,2)+math.pow(z_coord,2))
            if shot_displacement < targetSize:
                shot_hit = shot_hit + 1

            #Show trajectory paths
            if trajectoryPaths == True:
                # Convert all list items using defined conversion factor
                elevation_graph = [x * self.elevation_conversion for x in self.elevation_graph]
                distance_graph = [x * self.distance_conversion for x in self.distance_graph]
                windage_graph = [x * self.elevation_conversion for x in self.windage_graph]

                # PLOT ELEVATION vs DISTANCE
                drop.plot(distance_graph, elevation_graph, 'b-')

                # PLOT WINDAGE vs DISTANCE
                wind_deflection.plot(distance_graph, windage_graph, 'b-')


        #Calculate percentage of shots that hit
        percentage_hit = round((shot_hit/simNumber)*100,2)
        print("Percentage of shots on target: " + str(percentage_hit) + "%")

        #Plot the scatter data on a chart
        simulationHitFig = plt.figure()
        simPlot = simulationHitFig.add_subplot(211)
        #Plot target circle
        circle1 = plt.Circle((0,0),targetSize,edgecolor='b',fill=False)
        plt.gcf().gca().add_artist(circle1)
        plt.margins(1,1)
        plt.grid(True)

        #simPlot.axes.set_aspect(1)
        simPlot.set_ylabel("Vertical Deflection (" + self.elevation + ")")
        simPlot.set_xlabel("Horizontal Deflection (" + self.windage + ")")
        simPlot.scatter(POI_ycoords, POI_zcoords)
        plt.axis('equal')

        #Annotate each point with shot number
        for i in range(0,len(POI_ycoords)):
            simPlot.annotate(i,(POI_ycoords[i],POI_zcoords[i]))

        shotTable = plt.figure()

        cellText = []
        rowLabels = []
        #Display summary of simulation parameters
        for key in shot_info:
            row = []
            cellText.append([key+1,shot_info[key][0],shot_info[key][1],shot_info[key][2]])
            # cellText.append(row)
            rowLabels.append(key)
            print("Shot: " + str(key) + " | " + "FPS " + str(shot_info[key][0]) + " | " + "Wind Speed " +
                  str(shot_info[key][1]) + " | " + "Wind Angle " + str(shot_info[key][2]))
        colLabels = ("Shot #","Velocity","Wind Speed","Wind Angle")
        table = plt.table(cellText = cellText,colLabels = colLabels, loc='center')
        plt.axis('off')
        print(cellText)


        #Display graph after the shot table is shown

        plt.show()
