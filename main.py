import numpy as np

import vtk

from bodies.classes import Plate, Ball
from callback import vtkTimerCallback


def main():
    ball_radius = 0.02
    ball_position = (0, 0, ball_radius/2)

    normal = (0, 0, 1)
    plate = Plate(normal)
    ball = Ball(ball_radius, ball_position)

    # Numeric parameters
    dt = 0.01
    fps = 60
    delay_between_frames = 1000/fps

    # Create renderer and render window
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)

    # create a renderwindowinteractor
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # assign actor to the renderer
    ren.AddActor(plate.actor)
    ren.AddActor(ball.actor)

    # enable user interface interactor
    iren.Initialize()

    # Define callback class
    callback = vtkTimerCallback(ren, renWin)
    callback.data = {'plate':plate, 'ball': ball}
    
    iren.AddObserver('TimerEvent', callback.execute)
    iren.AddObserver('KeyPressEvent', callback.keypress)
    
    iren.CreateRepeatingTimer(round(delay_between_frames)) # milliseconds between frames
    iren.Start()


if __name__ == '__main__':
    main()
