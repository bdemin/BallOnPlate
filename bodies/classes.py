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
        self.plate_acc = np.array((self.const * np.sin(plate_x_angle), self.const * np.sin(plate_y_angle), 0))

        self.radius = radius
        self.plate_pos = np.array((0, 0, 0))
        self.plate_vel = np.array((0, 0, 0))
        self.normal = normal

        self.source, self.actor = create_sphere(self.radius, self.plate_pos)


    def update_position(self, dt):
        plate_x_angle = np.arctan2(self.normal[0], self.normal[2])
        plate_y_angle = np.arctan2(self.normal[1], self.normal[2])
        self.plate_acc = np.array((self.const * np.sin(plate_x_angle), self.const * np.sin(plate_y_angle), 0))

        self.plate_vel = self.plate_vel + self.plate_acc * dt
        self.plate_pos = self.plate_pos + self.plate_vel * dt


    def get_local_position(self, plane_normal):
        self.position = self.GetRotationMatrix(plane_normal) @ self.position
        return self.position


    def get_rotation_matrix(self):
        base_vector = np.array((0,0,1))

        # Collinear vectors:
        if np.cross(self.normal, base_vector).all() == False:
            return np.eye(3)

        # Rotation matrix based on 2 vectors
        v = np.cross(base_vector, self.normal)
        u = v/np.linalg.norm(v)
        c = np.dot(base_vector, self.normal)
        h = (1 - c)/(1 - c**2)

        vx, vy, vz = v
        rot_matrix = np.array([[c + h*vx**2, h*vx*vy - vz, h*vx*vz + vy, 0],
            [h*vx*vy+vz, c+h*vy**2, h*vy*vz-vx, 0],
            [h*vx*vz - vy, h*vy*vz + vx, c+h*vz**2, 0],
            [0, 0, 0, 1]])

        return rot_matrix


    def place_ball(self):
        trans = vtk.vtkTransform()
        trans.Identity()
        trans.Translate(*self.plate_pos)
        self.actor.SetUserTransform(trans)