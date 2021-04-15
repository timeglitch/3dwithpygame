
import pygame

import math

import time

import random


wallHeight = 100

class Camera:
    def __init__(s, screen, pixAr, walls):
        s.x = 0
        s.y = 0
        s.rotation = 0
        s.fov = math.pi/4
        s.vfov = math.pi/3
        s.screen = screen
        s.pixAr = pixAr
        s.walls = walls
    
    

                





    def calcRay(s, x, y, angle):
        closestWall = None
        closestPoint = None
        closestDist = 10000
        wallPercent = 0
        x2 = x + math.cos(angle) * 10000
        y2 = y + math.sin(angle) * 10000
        for i in s.walls:
            for j in i.fourLines:
                #print(j)
                pt = s.lineIntersect((x, y), (x2, y2), j[0], j[1])
                if pt != None:
                    #print(pt)
                    if s.distance(x , y, pt[0], pt[1]) < closestDist:
                        closestPoint = pt
                        closestWall = i
                        closestWall = i
                        closestDist = s.distance(x , y, pt[0], pt[1])
                        if j[1][0] - j[0][0] == 0:
                            wallPercent = 0
                        else:
                            wallPercent = abs(pt[0] - j[0][0])/(j[1][0] - j[0][0])
        
        return(closestDist, closestWall, wallPercent)
    
    def lineIntersect(s, a, b, c, d):
        x1 = a[0]
        y1 = a[1]
        x2 = b[0]
        y2 = b[1]
        x3 = c[0]
        y3 = c[1]
        x4 = d[0]
        y4 = d[1]
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(denom) < 0.001:
            print("parellel error")
            return None
        outx = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4))/denom
        outy = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4))/denom
        if not(s.inBetween(x1, x2,outx) and s.inBetween(x3, x4, outx)):
            return None
        return (outx, outy)

    def inBetween(s, a, b, mid):
        if a > b:
            return a >= mid >= b
        else:
            return b >= mid >= a

    def distance(s, x1, y1, x2, y2):
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)
    
    def update(s, x, y, rotation):
        screenw = s.screen.get_width()
        screenh = s.screen.get_height()
        for i in range(screenw):
            angle = ((screenw - i)/screenw) * s.fov - s.fov/2 + rotation
            rayInfo = s.calcRay(x,y,angle)
            #print(rayInfo)

            if rayInfo[1] != None:
                texture = rayInfo[1].texture
                drawHeight = abs(math.atan2(wallHeight, rayInfo[0]))
            for j in range(screenh):
                degree = s.fov/2 - (j/screenh) * s.vfov
                if abs(degree) < drawHeight:
                    s.pixAr[i, j] = texture