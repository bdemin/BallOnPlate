import numpy as np

from vtk import vtkCamera


class vtkTimerCallback(object):
    def __init__(self, renderer, renwin, iren):
        self.timer = 1
        self.mouse_left_pressed = False
        
        self.renderer = renderer
        self.renwin = renwin
        self.iren = iren

        cam_distance = (1, 1, 1)
        self.camera = vtkCamera()
        self.renderer.SetActiveCamera(self.camera)
        self.camera.SetViewUp(0,0,1)
        self.camera.SetFocalPoint(0, 0, 0)
        self.camera.SetPosition(cam_distance)


    def execute(self, obj, event):
        # self.data['plate'].source.SetNormal(*normal)

        obj.GetRenderWindow().Render()
        self.timer += 1


    def mouse_button(self, obj, event):
        if event == "LeftButtonPressEvent":
            self.mouse_left_pressed = True
        elif event == "LeftButtonReleaseEvent":
            self.mouse_left_pressed = False


    # General high-level logic
    def mouse_move(self, obj, event):
        if self.mouse_left_pressed:
            lastXYpos = self.iren.GetLastEventPosition()
            lastX = lastXYpos[0]
            lastY = lastXYpos[1]

            xypos = self.iren.GetEventPosition()
            x = xypos[0]
            y = xypos[1]

            center = self.renwin.GetSize()
            centerX = center[0]/2.0
            centerY = center[1]/2.0

            # print(lastX-x)
            # print(lastY-y)

            factor = 0.1
            roll = np.sign(lastX - x) * factor
            pitch = np.sign(lastY - y) * factor

            normal = self.data['plate'].normal
            print(normal)
            normal = normal + np.array([roll, pitch, 1])
            print(normal)
            # updated_normal = map(lambda x,y: x+y, normal, [roll,pitch,0])

            self.data['plate'].source.SetNormal(*normal)
            self.data['plate'].source.Update()