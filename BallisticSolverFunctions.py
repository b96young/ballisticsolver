import math

def Cd(mass_bullet,velocity,ballistic_coefficient,bullet_diameter):
    print (mass_bullet)
    print (velocity)
    print (ballistic_coefficient)
    print (bullet_diameter)
    if (velocity > 480):
        Cg = 0.0000003*pow(velocity,2) - 0.0008*velocity + 0.9552
    elif(velocity > 400):
        Cg = 0.0034*velocity - 0.6928
    elif(velocity > 300):
        Cg = -2E-05*pow(velocity,2) + 0.0139*velocity - 2.4638
    else:
        Cg = 4E-06*pow(velocity,2) - 0.0011*velocity + 0.2689


    Cd = (mass_bullet*Cg*0.0014223)/((ballistic_coefficient)*pow(bullet_diameter,2))

    print ("Cg = " + str(Cg))
    return Cd

def targetGen(size,distance):
    #MOA = 1 inch / 100 yds
    MOA = 1/100

    r = size

    y_coords = []
    z_coords = []
    x_coord = []

    #Z^2 + Y^2 = r^2
    #Z = sqrt(r^2  - Y^2)

    for y in range(-r*1,r*1+1):
        y_coords.append(y/1.0)
        z = math.sqrt(pow(r,2) - pow(y/1.0,2))
        z_coords.append(z)
        x_coord.append(distance)

    for y in range(-r*1,r*1+1):
        y_coords.append(y/1.0)
        z = -1*math.sqrt(pow(r,2) - pow(y/1.0,2))
        z_coords.append(z)
        x_coord.append(distance)

    target = {'x':x_coord,'y':y_coords,'z':z_coords}
    #print (y_coords)
    #print(z_coords)
    return target