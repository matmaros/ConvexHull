import random #use this to get random
import rhinoscriptsyntax as rs

#returns list of random points sorted left to right
def random_points_sorted(num_points, x_max, y_max):
    points = []
    for i in range (0, num_points):
        points.append([random.random()*x_max, random.random()*y_max, 0])        
    
    points.sort()
    return points

num_points = rs.GetInteger('how many points for Convex Hull?')
points = random_points_sorted(num_points,num_points*2,num_points*2)
rs.AddPoints(points)

set = []
set.append(points[0])
i = -1
end_loop = 0

while True:
    
    i += 1
    if i == 0:
        plane = rs.PlaneFromPoints([0,0,0],[1,0,0],[0,1,0])
    else:
        point1 = set[i] #origin
        point2 = set[i-1] #-y vector
        vectorY = rs.VectorCreate(point2,point1) #(tp_point, from_point)
        vectorY = rs.VectorRotate(vectorY,180,[0,0,1])
        vectorX = rs.VectorRotate(vectorY,270,[0,0,1])
        plane = rs.PlaneFromFrame(point1, vectorX, vectorY)
        
    angles = []
    for point in points:
        if point == set[i]:            
            angles.append(-180)
        else:
            angles.append(rs.Angle(set[i],point,plane))
                
    index = angles.index(max(angles))
    set.append(points[index])
    
    if set[i] == set[0]:
        end_loop += 1
        if end_loop == 2:
            break
        
rs.AddPolyline(set)