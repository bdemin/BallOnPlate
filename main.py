# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 16:38:18 2018

@author: slavd
"""

import scipy.constants
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sys
        
class Plate(object):
    def __init__(self, angle):
        self.angle = angle
        self.x_coords = np.asarray([0,1])
        self.y_coords = np.asarray([0.5-np.tan(self.angle)/2,
                                    0.5+np.tan(self.angle)/2])
        
    def DrawPlate(self):
        line, = plt.plot(self.x_coords, self.y_coords, 'C2', 'o-', lw = 2)
        return line
        
    def TiltPlate(self, angle_delta):
        self.angle += angle_delta
        self.y_coords = np.asarray([0.5-np.tan(self.angle)/2,
                                    0.5+np.tan(self.angle)/2])

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

    def DrawBall(self, ax):
        circle = plt.Circle((self.x_pos, self.y_pos),
                            radius = self.rad, fc='y')
        circle = ax.add_patch(circle)
        return circle

    def Move(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

fig1, ax1 = plt.subplots()
fig1.set_figheight(7)
fig1.set_figwidth(7)

ball_r = 0.03
ball_b = 1
ball_m = 100
ball_I = 0.5*ball_m*ball_r**2
const = -scipy.constants.g/(1+(ball_I/(ball_m*ball_b^2)))


angle = 0 * (np.pi/180)
angle_limit = 30

plate = Plate(angle)
ball = Ball(ball_r, plate.angle)
line, = ax1.plot([], [], lw=2)
circle = ball.DrawBall(ax1)
angle_text = ax1.text(0.05, 0.9, '', transform = ax1.transAxes)
time_template = 'Angle = %i[deg]'

def press(event):
#    if self.angle < np.deg2rad(45) and self.angle > np.deg2rad(-45):
    if event.key == 'a'and plate.angle < np.deg2rad(angle_limit):
        plate.TiltPlate(1 * (np.pi/180))
    if event.key == 'd' and plate.angle > np.deg2rad(-angle_limit):
        plate.TiltPlate(-1 * (np.pi/180))
    sys.stdout.flush()
        

def init():
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    angle_text.set_text('')
    return line, circle, angle_text
    
def animate(i):
    ball.acc = const*np.sin(plate.angle)
    ball.pvel = ball.pvel_last + ball.acc*dt
    ball.ppos = ball.ppos_last + ball.pvel*dt
    
    ball.Move(0.5 + ball.ppos*np.cos(plate.angle),
              0.5 + ball.rad/np.cos(plate.angle) + ball.ppos*np.sin(plate.angle))
    
    ball.ppos_last = ball.ppos
    ball.pvel_last = ball.pvel
    
    line.set_data(plate.x_coords, plate.y_coords)
    circle = ball.DrawBall(ax1)
    angle_text.set_text(time_template % ((180/np.pi)*plate.angle))
#    print(i)
    return line, circle, angle_text


fig1.canvas.mpl_connect('key_press_event', press)
T = 6
FPS = 48
total_frames = T*FPS
dt = (1/FPS)
anim = animation.FuncAnimation(fig1, animate, interval = dt*1000,
                               init_func = init, blit = True,
                               repeat = False)
plt.show()