import numpy as np
import scipy.constants

import vtk

from callback import vtkTimerCallback

from bodies.create_bodies import create_plane, create_sphere


class BallPlateSystem(object):
    # Class to store all the visualization objects and data

    def __init__(self, normal, radius):
        self.normal = normal
        self.radius = radius

        self.plate = Plate(self.normal)
        self.ball = Ball(self.radius, self.normal)

        fps = 60
        self.frame_delay = round(1000 / fps)
        self.dt = 0.01


    def init_visualization(self):
        # Initialize the graphical section of the simulation

        # Create renderer and render window
        self.ren = vtk.vtkRenderer()
        self.renwin = vtk.vtkRenderWindow()
        self.renwin.AddRenderer(self.ren)

        # Create an interactor
        self.iren = vtk.vtkRenderWindowInteractor()
        self.iren.SetInteractorStyle(None)
        self.iren.SetRenderWindow(self.renwin)

        # Assign actors to the renderer
        self.ren.AddActor(self.plate.actor)
        self.ren.AddActor(self.ball.actor)

        self.iren.Initialize()

    def init_callback(self):
        # Initialize the repeating callback

        # Define callback class
        callback = vtkTimerCallback(self.ren, self.renwin, self.iren)
        callback.system = self

        # Add keyboard and mouse observers
        ## can move this section to CallBack?
        self.iren.AddObserver('TimerEvent', callback.execute)
        self.iren.AddObserver('LeftButtonPressEvent', callback.mouse_button)
        self.iren.AddObserver('MouseMoveEvent', callback.mouse_move)
        self.iren.AddObserver('LeftButtonReleaseEvent', callback.mouse_button)
        self.iren.AddObserver('RightButtonPressEvent', callback.mouse_button)
        self.iren.AddObserver('MouseWheelForwardEvent', callback.MouseWheelForwardEvent)
        self.iren.AddObserver('MouseWheelBackwardEvent', callback.MouseWheelBackwardEvent)

        self.iren.CreateRepeatingTimer(self.frame_delay) # milliseconds between frames

    def update_normal(self, new_normal):
        self.normal = new_normal

    def update_positions(self):
        self.plate.update(self.normal)
        self.ball.update(self.normal, self.dt)

    def reset(self):
        # Reset the system to initial values
        self.update_normal((0, 0, 1))
        self.ball.pos_world = np.array((0, 0, self.ball.radius/2))
        self.ball.vel_world = np.array((0, 0, 0))
        self.ball.acc_world = np.array((0, 0, 0))

    def kill(self):
        # Quit program
        self.iren.DestroyTimer()
        self.iren.GetRenderWindow().Finalize()
        self.iren.TerminateApp()

class Plate(object):
    # Class defining the plate using a vtkPlate object

    def __init__(self, normal):
        position = (0, 0, 0)
        self.source, self.actor = create_plane(position, normal)

    def update(self, normal):
        # Update normal and plane source
        self.source.SetNormal(normal)
        self.source.Update()


class Ball(object):
    # Class defining the ball using vtkSphere object

    def __init__(self, radius, normal):
        # Physical parameters
        self.radius = radius
        self.mass = 1
        ball_I = (2/5) * self.mass * self.radius**2
        self.const = scipy.constants.g \
            / (1 + (ball_I/(self.mass * self.radius**2)))

        self.pos_world = np.array((0, 0, radius/2))
        self.vel_world = np.array((0, 0, 0))
        self.acc_world = np.array((0, 0, 0))

        self.source, self.actor = create_sphere(radius, self.pos_world)

    def update(self, normal, dt):
        # Calculate ball position iteratively
        plate_x_angle = np.arctan2(normal[0], normal[2])
        plate_y_angle = np.arctan2(normal[1], normal[2])

        self.acc_world = np.array((self.const * np.sin(plate_x_angle), self.const * np.sin(plate_y_angle), 0))
        self.vel_world = self.vel_world + self.acc_world * dt
        self.pos_world = self.pos_world + self.vel_world * dt

        # Fix z value according to the plate's normal
        self.pos_world[2] = (-self.pos_world[0]*normal[0] - \
            self.pos_world[1]*normal[1]) / normal[2] + self.radius

        self.source.SetCenter(self.pos_world)
        self.source.Update()

    def update_params(self, radius_delta, mass_delta):
        check_val = self.radius + radius_delta
        if check_val < 0.01 or check_val > 0.4:
            return

        self.radius += radius_delta
        self.source.SetRadius(self.radius)
        self.source.Update()

        self.mass += mass_delta
        ball_I = (2/5) * self.mass * self.radius**2
        self.const = scipy.constants.g \
            / (1 + (ball_I/(self.mass * self.radius**2)))

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
