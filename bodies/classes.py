import numpy as np
import scipy.constants

from bodies.create_bodies import create_plane, create_sphere


class Plate(object):
    def __init__(self, normal):
        self.normal = np.array(normal)
        self.position = (0, 0, 0)
        # self.z = (-i*normal[0]*plate.xx - normal[1]*plate.yy - plate.d) * 1./normal[2]
        self.source, self.actor = create_plane(self.position, self.normal)

        
    def TiltPlate(self, pitch, roll):
        self.angle = np.deg2rad(angle)
        self.y_coords = np.asarray([0.5-np.tan(self.angle)/2,
                                    0.5+np.tan(self.angle)/2])
        self.DrawPlate()


class Ball(object):
    def __init__(self, radius, position):
        ball_b = 1
        ball_I = 1000
        ball_m = 1000
        self.const = -scipy.constants.g/(1+(ball_I/(ball_m*ball_b^2)))

        self.radius = radius
        self.position = position
        
        # self.x_pos = 0.5
        # self.y_pos = 0.5 + (self.rad / np.cos((angle)))
        
        # self.ppos = 0
        # self.ppos_last = self.ppos
        
        self.pvel = 0
        self.pvel_last = 0
        
        self.acc = 0

        self.source, self.actor = create_sphere(self.radius, self.position)


    def update_position(self, x_pos, y_pos, plane_normal, dt):
        pitch = np.arctan(plane_normal[0], plane_normal[2])
        roll = np.arctan(plane_normal[1], plane_normal[2])
        self.acc = [self.const*np.sin(pitch), self.const*np.sin(roll), 0]

        self.velocity += self.acc*dt
        self.position += self.velocity*dt


    def get_local_position(self, plane_normal):
        self.position = self.GetRotationMatrix(plane_normal) @ self.position
        return self.position


    def get_rotation_matrix(self, plane_vector):
        base_vector = np.array((0,0,1))

        # Collinear vectors:
        if np.cross(plane_vector, base_vector).all() == False:
            return np.eye(3)

        # Rotation matrix based on 2 vectors
        v = np.cross(base_vector, plane_vector)
        u = v/np.linalg.norm(v)
        c = np.dot(base_vector, plane_vector)
        h = (1 - c)/(1 - c**2)

        vx, vy, vz = v
        rot_matrix = np.array([[c + h*vx**2, h*vx*vy - vz, h*vx*vz + vy],
            [h*vx*vy+vz, c+h*vy**2, h*vy*vz-vx],
            [h*vx*vz - vy, h*vy*vz + vx, c+h*vz**2]])

        return rot_matrix