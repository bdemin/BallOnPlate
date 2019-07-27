import numpy as np


class Ball(object):
    def __init__(self, rad, normal):
        self.rad = rad
        
        self.px_pos = 0
        self.py_pos = 0
        self.pz_pos = self.rad
        
        self.px_vel = 0
        self.py_vel = 0
        
        self.px_acc = 0
        self.py_acc = 0
        
        self.z = (np.sqrt(sum(normal**2)) * self.rad) / normal[2]
        
        self.ppos = 0
        self.ppos_last = self.ppos
        
        self.pvel = 0
        self.pvel_last = 0
        
#        self.acc = 0

    def DrawBall(self, ax):
        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        
#        x = np.cos(u)*np.sin(v)
#        y = np.sin(u)*np.sin(v)
#        z = np.cos(v)
        x = self.rad * np.cos(u)*np.sin(v)
        y = self.rad * np.sin(u)*np.sin(v)
        z = self.rad * np.cos(v) + self.z
        
        self.sphere = ax.plot_surface(x, y, z, color="r", zorder = 2)
        
#        circle = plt.Circle((self.x_pos, self.y_pos),
#                            radius = self.rad, fc='y')
#        circle = ax.add_patch(circle)
        return self.sphere


    def Move(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos