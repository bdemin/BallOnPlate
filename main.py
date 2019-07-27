import numpy as np

import vtk

from bodies.classes import Plate, Ball



def main():
    ball_radius = 0.02
    ball_position = (0, 0, ball_radius/2)

    normal = (0, 0, 1)
    plate = Plate(normal)
    ball = Ball(ball_radius, ball_position)

    # Numeric parameters
    dt = 0.01
    T = 1
    N = int(T/dt)


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
    renWin.Render()
    iren.Start()

if __name__ == '__main__':
    main()
