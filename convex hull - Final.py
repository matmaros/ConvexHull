#requires Rhino 3d Software - open a new file in rhino and enter "edit python script" into the command bar
#copy paste the following code into the python editor and run the code

import random 
import rhinoscriptsyntax as rs

#generate random points sorted left to right from num of points and an x & y range
def random_points_sorted(num_points, x_max, y_max):
    points = []
    for i in range (0, num_points):
        points.append([random.random()*x_max, random.random()*y_max, 0])        
    
    points.sort()
    return points

#ask for number of points and generate random set of points
num_points = rs.GetInteger('how many points for Convex Hull?')
points = random_points_sorted(num_points,num_points*2,num_points*2)
rs.AddPoints(points)

#create empty set for convex hull points, add left most point as first point in set
set = []
set.append(points[0])
#set counter and loop termination var
i = -1
end_loop = 0

#intiate main loop
while True:
    
    i += 1

    #if first iteration set plane 
    if i == 0:
        plane = rs.PlaneFromPoints([0,0,0],[1,0,0],[0,1,0])
    #Create plane based on current and previous point in set for angle comparison in next step
    else:
        point1 = set[i] #origin
        point2 = set[i-1] #-y vector
        vectorY = rs.VectorCreate(point2,point1) #(tp_point, from_point)
        vectorY = rs.VectorRotate(vectorY,180,[0,0,1])
        vectorX = rs.VectorRotate(vectorY,270,[0,0,1])
        plane = rs.PlaneFromFrame(point1, vectorX, vectorY)

    #measure angle of all points to current point    
    angles = []
    for point in points:
        if point == set[i]:            
            angles.append(-180)
        else:
            angles.append(rs.Angle(set[i],point,plane))

    #get index of point with largest angle (longest counter clockwise angle from current point)             
    index = angles.index(max(angles))
    #set point at index to next point in convex hull set
    set.append(points[index])
    
    #check if set has moved around to original point and if so end script
    if set[i] == set[0]:
        end_loop += 1
        if end_loop == 2:
            break

#create polyline connecting convex hull set        
rs.AddPolyline(set)
