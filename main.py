import numpy as np

import vtk

from bodies.classes import Plate, Ball
from callback import vtkTimerCallback


def main():
    global iren, renWin, ren
    def ButtonEvent(obj, event):
        global Rotating, Panning, Zooming
        if event == "LeftButtonPressEvent":
            Rotating = 1
        elif event == "LeftButtonReleaseEvent":
            Rotating = 0
        elif event == "MiddleButtonPressEvent":
            Panning = 1
        elif event == "MiddleButtonReleaseEvent":
            Panning = 0
        elif event == "RightButtonPressEvent":
            Zooming = 1
        elif event == "RightButtonReleaseEvent":
            Zooming = 0

    # General high-level logic
    def MouseMove(obj, event):
        global Rotating, Panning, Zooming
        global iren, renWin, ren
        lastXYpos = iren.GetLastEventPosition()
        lastX = lastXYpos[0]
        lastY = lastXYpos[1]

        xypos = iren.GetEventPosition()
        x = xypos[0]
        y = xypos[1]

        center = renWin.GetSize()
        centerX = center[0]/2.0
        centerY = center[1]/2.0

        print(lastX-x)
        print(lastY-y)

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
    iren.SetInteractorStyle(None)
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
    
    iren.AddObserver('LeftButtonPressEvent', ButtonEvent)
    iren.AddObserver('MouseMoveEvent', MouseMove)

    iren.CreateRepeatingTimer(round(delay_between_frames)) # milliseconds between frames
    iren.Start()


    def ButtonEvent(obj, event):
        global Rotating, Panning, Zooming
        if event == "LeftButtonPressEvent":
            Rotating = 1
        elif event == "LeftButtonReleaseEvent":
            Rotating = 0
        elif event == "MiddleButtonPressEvent":
            Panning = 1
        elif event == "MiddleButtonReleaseEvent":
            Panning = 0
        elif event == "RightButtonPressEvent":
            Zooming = 1
        elif event == "RightButtonReleaseEvent":
            Zooming = 0

    # General high-level logic
    def MouseMove(obj, event):
        global Rotating, Panning, Zooming
        global iren, renWin, ren
        lastXYpos = iren.GetLastEventPosition()
        lastX = lastXYpos[0]
        lastY = lastXYpos[1]

        xypos = iren.GetEventPosition()
        x = xypos[0]
        y = xypos[1]

        center = renWin.GetSize()
        centerX = center[0]/2.0
        centerY = center[1]/2.0


if __name__ == '__main__':
    main()
