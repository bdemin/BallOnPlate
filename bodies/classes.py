import numpy as np
import scipy.constants

import vtk

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

    def update_normal(self, new_normal):
        self.normal = np.array(new_normal)
        self.source.SetNormal(*self.normal)
        self.source.Update()


class Ball(object):
    def __init__(self, radius, normal):
        ball_mass = 0.25
        ball_I = (2/5) * ball_mass * radius**2
        self.const = scipy.constants.g/(1+(ball_I/(ball_mass*radius**2)))

        plate_x_angle = np.arctan2(normal[0], normal[2])
        plate_y_angle = np.arctan2(normal[1], normal[2])
        # self.plate_acc = np.array((self.const * np.sin(plate_x_angle), self.const * np.sin(plate_y_angle), 0))

        self.radius = radius
        self.plate_acc = np.array((0, 0, 0))
        self.plate_pos = np.array((0, 0, 0))
        self.plate_vel = np.array((0, 0, 0))
        self.world_pos = np.array((0, 0 ,0))
        self.normal = normal

        self.source, self.actor = create_sphere(self.radius, self.world_pos)


    def update_position(self, dt):
        plate_x_angle = np.arctan2(self.normal[0], self.normal[2])
        plate_y_angle = np.arctan2(self.normal[1], self.normal[2])
        self.plate_acc = np.array((self.const * np.sin(plate_x_angle), self.const * np.sin(plate_y_angle), 0))

        self.plate_vel = self.plate_vel + self.plate_acc * dt
        self.plate_pos = self.plate_pos + self.plate_vel * dt

        rot = self.rot_mat(plate_x_angle, plate_y_angle)
        print(rot)
        self.world_pos = self.plate_pos @ rot


    def get_local_position(self, plane_normal):
        self.position = self.GetRotationMatrix(plane_normal) @ self.position
        return self.position


    def rot_mat(self, x, y):
        sin = np.sin
        cos = np.cos
        matrix = []

        Cx = cos(x)
        Cy = cos(y)
        Cz = cos(0)

        Sx = sin(x)
        Sy = sin(y)
        Sz = sin(0)

        matrix.append(Cy * Cz)
        matrix.append(Cz * Sx * Sy-Cx * Sz)
        matrix.append(Sx * Sz+Cx * Cz * Sy)
        
        matrix.append(Cy * Sz)
        matrix.append(Cx * Cz+Sx * Sy * Sz)
        matrix.append(Cx * Sy * Sz-Cz * Sx)
        
        matrix.append(-Sy)
        matrix.append(Cy * Sx)
        matrix.append(Cx * Cy)
        
        matrix = np.asarray(matrix).reshape(3,3)
        return matrix

    def place_ball(self):
        trans = vtk.vtkTransform()
        trans.Identity()
        trans.Translate(*self.world_pos)
        self.actor.SetUserTransform(trans)