import matplotlib.path as mpath
from svgpath2mpl import parse_path
import csv
import math
import os

path = parse_path("M 196 56 C 200 160 92 184 116 60")

pathVerts = path.interpolated(25).vertices

motor1Reversed = False
motor2Reversed = False

motor1x = 0
motor1y = 145

motor2x = 0
motor2y = 0

motorArmLength = 200
extensionArmLength = 200
penOffset = 50


#why in the world did I DESIGN IT LIKE THIS WHY CANT THE PEN JUST BE AT THE PIVOT POINT I HATE MYSELF NOW I HAVE TO DO LIKE ITERATIVE STUFF AND ITS STUPID AND NOW IT ISNT LIKE A CLOSED SOLUTION
def getElbowAngle(vert):
    x = vert[0]
    y = vert[1]

    return math.acos((x**2 + y**2 - motorArmLength**2 - extensionArmLength**2)/(2 * motorArmLength * extensionArmLength))

def getShoulderAngle(vert, reverse = False):
    x = vert[0]
    y = vert[1]
    if reverse:
        return math.atan(y / x) - math.atan((extensionArmLength * math.sin(-getElbowAngle(vert))) / (motorArmLength + extensionArmLength * math.cos(-getElbowAngle(vert))))
    return math.atan(y/x) - math.atan((extensionArmLength * math.sin(getElbowAngle(vert))) / (motorArmLength + extensionArmLength * math.cos(getElbowAngle(vert))))

def getMarkerAngle(vert):
    return getShoulderAngle(vert) + getElbowAngle(vert)

def adjustTarget(vert, angle):
    return [vert[0] - penOffset * math.cos(angle), vert[1] - penOffset * math.sin(angle)]

def getMotorAngle(vert, iterations):

    target = vert

    for i in range(iterations):
        markerAngle = getMarkerAngle(target)
        target = adjustTarget(vert, markerAngle)

    local1 = (target[0] - motor1x, target[1] - motor1y)
    local2 = (target[0] - motor2x, target[1] - motor2y)

    shoulder1 = getShoulderAngle(local1, reverse = True)
    shoulder2 = getShoulderAngle(local2)

    return [shoulder1, shoulder2]

def convertToTicks(angles):
    motor1ticks = round(angles[0] * 509.3)
    motor2ticks = round(angles[1] * 509.3)

    return [motor1ticks, motor2ticks]

motorAngles = []
for vert in pathVerts:
    motorAngle = getMotorAngle(vert, 3)
    motorAngles.append(convertToTicks(motorAngle))

if os.path.exists("MotorRotations.csv"):
    os.remove("MotorRotations.csv")

with open("MotorRotations.csv", mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(motorAngles)

