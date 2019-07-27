# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 20:13:01 2018

@author: slavd
"""
import pygame
import scipy.constants
import matplotlib.pyplot as plt

#define Ball class
class Ball:
    def __init__(self,x,y,size):
        self.position = (x,y)
        self.last_position = (0,0)
        self.size = size
        self.colour = (0, 0, 255)
        self.thickness = 5
        self.mass = 0.2
        self.I = 1
        self.force_x = 0
        self.forces_y = -scipy.constants.g
        self.time = [0]
        self.pos = [0]
        
    def display(self):
            pygame.draw.circle(window, self.colour, self.position, self.size, self.thickness)

    def move(self):
        dt = 0.04
        self.time.append(self.time[-1]+dt)
        
        x = self.position[0]
        y = self.position[1]
        print(self.position)
        print(self.last_position)
        y = y*(2+scipy.constants.g*dt**2)-self.last_position[1]
        self.position = (int(x),int(y))
        self.pos.append(-y)
        
        self.last_position = (x,y)
    def forces(self):
        pass

    def collision(self):
        pass
    
    def update_location(self):
        pass
    
    def update_velocity(self):
        pass

#create window
background_colour = (255,255,255)
(width, height) = (1920, 1080)
(p_x,p_y,p_size) = (int(width/2),200,10)

window = pygame.display.set_mode((width, height))
pygame.display.flip()
pygame.display.set_caption('Ball on 1DOF Plate')
window.fill(background_colour)

#draw ball
ball = Ball(p_x,p_y,p_size)
ball.display()

pygame.event.get()


running = True
while running:
    window.fill(background_colour)
    if ball.position[1]<height-10:
        ball.move()
        ball.display()

#        print(ball.time[-1])
        pygame.display.flip()

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            
            
            
            

ball.pos[0]=ball.pos[1]
data = {'pos' : ball.pos, 
        'time' : ball.time}

plt.figure(1)
plt.plot(data['time'] ,data['pos'])
plt.gcf().autofmt_xdate()
plt.title('position vs time')
plt.show()


            

      
      
