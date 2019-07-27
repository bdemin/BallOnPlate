import numpy as np


class Plate(object):
    def __init__(self, point, normal):
        self.point = point
        self.normal = normal
        self.Build()
        
        
    def Build(self):
        self.xx, self.yy = np.meshgrid(np.linspace(-1, 1, 2), np.linspace(-1, 1, 2))
        self.d = -self.point.dot(self.normal)
        self.z = (-self.normal[0]*self.xx - self.normal[1]*self.yy - self.d) * 1/self.normal[2]
        
        
    def DrawPlate(self, ax):
        self.plane = ax.plot_surface(self.xx, self.yy, self.z, alpha = 1, zorder = 1)
        return self.plane
        
    
    def TiltPlate(self, normal):
        self.z = (-normal[0]*self.xx - normal[1]*self.yy - self.d) * 1/normal[2]
        