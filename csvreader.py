import csv,math
def dragCoefficient(model,velocity,mach_conversion):
    if model == "G7":
        with open("G7 Drag Function.csv") as G7DragFile:
            G7Drag = list(csv.reader(G7DragFile))
            #Used for interpolation y = (y1-y0)/(x1-x0)*(x-x0)+y0
            x_values = []
            y_values = []
            bottom_index = 0
            for row in G7Drag:
                velocity_table = float(row[0])*mach_conversion
                if velocity - velocity_table == 0:
                    return row[1]
                elif velocity - velocity_table > 0:
                    bottom_index += 1
                elif velocity - velocity_table < 0:
                    top_index = bottom_index
                    x_values.append(float(G7Drag[bottom_index-1][0]) * mach_conversion)
                    x_values.append(float(G7Drag[top_index][0]) * mach_conversion)
                    y_values.append(float(G7Drag[bottom_index-1][1]))
                    y_values.append(float(G7Drag[top_index][1]))
                    # print(bottom_index)
                    # print(top_index)
                    # print (x_values)
                    # print (y_values)
                    # print (velocity)
                    cd = (y_values[1]-y_values[0]) / (x_values[1]-x_values[0]) * (velocity-x_values[0]) + y_values[0]
                    return cd

    else:
        with open("G1 Drag Function.csv") as G1DragFile:
            G1Drag = list(csv.reader(G1DragFile))
            #Used for interpolation y = (y1-y0)/(x1-x0)*(x-x0)+y0
            x_values = []
            y_values = []
            bottom_index = 0

            for row in G1Drag:
                print (row)
                velocity_table = float(row[0])*mach_conversion
                if velocity - velocity_table == 0:
                    return row[1]
                elif velocity - velocity_table > 0:
                    bottom_index += 1
                elif velocity - velocity_table < 0:
                    top_index = bottom_index
                    x_values.append(float(G1Drag[bottom_index-1][0]) * mach_conversion)
                    x_values.append(float(G1Drag[top_index][0]) * mach_conversion)
                    y_values.append(float(G1Drag[bottom_index-1][1]))
                    y_values.append(float(G1Drag[top_index][1]))
                    # print(bottom_index)
                    # print(top_index)
                    # print (x_values)
                    # print (y_values)
                    # print (velocity)
                    cd = (y_values[1]-y_values[0]) / (x_values[1]-x_values[0]) * (velocity-x_values[0]) + y_values[0]
                    return cd

