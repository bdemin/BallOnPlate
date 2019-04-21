# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 16:38:18 2018

@author: slavd
"""

import scipy.constants
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
#import matplotlib.animation as animation
import numpy as np

fig = plt.figure(figsize = (12,12))
angle = 30
ball_rad = 0.1

class Plate(object):
    def __init__(self, angle):
        self.angle = angle
        self.x_coords = np.asarray([0,1])
        self.y_coords = np.asarray([0.5-np.tan(self.angle)/2,
                                    0.5+np.tan(self.angle)/2])
        
    def DrawPlate(self):
        self.line = plt.plot(self.x_coords, self.y_coords, 'C2', 'o-', lw = 2)
        plt.pause(0.01)
        
    def TiltPlate(self, angle):
        plt.gca().lines.pop(0)
        self.angle = np.deg2rad(angle)
        self.y_coords = np.asarray([0.5-np.tan(self.angle)/2,
                                    0.5+np.tan(self.angle)/2])
        self.DrawPlate()
        


class Ball(object):
    def __init__(self, rad, angle):
        self.rad = rad
        
        self.x_pos = 0.5
        self.y_pos = 0.5 + (self.rad / np.cos((angle)))
        
        self.ppos = 0
        self.ppos_last = self.ppos
        
        self.pvel = 0
        self.pvel_last = 0
        
        self.acc = 0

    def DrawBall(self):
        self.circ = Circle((self.x_pos, self.y_pos),
                           radius = self.rad,
                           fill = True)
        plt.gca().add_patch(self.circ)
        plt.xlim(0,1)
        plt.ylim(0,1)
        plt.gca().set_aspect('equal')
        plt.show()
        plt.pause(0.01)
        ball.circ.remove()

    def Move(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        
        
angle = np.deg2rad(angle)
plate = Plate(angle)
plate.DrawPlate()

ball = Ball(ball_rad, plate.angle)
ball.DrawBall()
#plate.TiltPlate(10)
#plate.TiltPlate(45)
def main2center(vec):
    return vec+0.5

def center2plate(vec,angle):
    return vec[0]*np.cos(angle), vec[1]*np.sin(angle)
    

"""
def animate(i):
    angle = math.radians(i)
    xs = [0,1]
    ys = [0.5-np.tan(angle)/2,0.5+np.tan(angle)/2]
    line = plt.plot(xs,ys,'o-',lw = 5,c = 'k')
    return line

"""


ball_b = 1
ball_I = 1000
ball_m = 1000
const = -scipy.constants.g/(1+(ball_I/(ball_m*ball_b^2)))

dt = 0.01
T = 1
N = int(T/dt)
for t in range(N):
    ball.DrawBall()

    
    
    ball.acc = const*np.sin(plate.angle)
    ball.pvel = ball.pvel_last + ball.acc*dt

    ball.ppos = ball.ppos_last + ball.pvel*dt
    
#    ball.x_pos += ball.ppos*np.cos(angle)
#    ball.y_pos += ball.ppos*np.sin(angle)
    
    ball.Move(0.5 + ball.ppos*np.cos(plate.angle),
               0.5 + ball.rad/np.cos(plate.angle) + ball.ppos*np.sin(plate.angle))
    ball.ppos_last = ball.ppos
    ball.pvel_last = ball.pvel
    plate.TiltPlate(np.rad2deg(plate.angle)-1)
#    plate.TiltPlate(-10)
    



#ani = animation.FuncAnimation(fig,animate, interval=2,
#                              blit=True, save_count=50)
