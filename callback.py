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
        # self.data['ball'].normal = self.data['plate'].normal
        # self.data['ball'].update_position(self.dt)
        # self.data['ball'].place_ball()

        normal = self.data['plate'].normal / np.linalg.norm(self.data['plate'].normal)
        ball_z = self.data['ball'].radius / normal[2]

        self.data['ball'].plate_pos = (0, 0, ball_z)
        # self.data['ball'].update_position(self.dt)
        self.data['ball'].place_ball()


        obj.GetRenderWindow().Render()
        self.timer += 1

    def mouse_button(self, obj, event):
        if event == "LeftButtonPressEvent":
            self.mouse_left_pressed = True
        elif event == "LeftButtonReleaseEvent":
            self.mouse_left_pressed = False
        elif event == "RightButtonPressEvent":
            self.data['plate'].update_normal((0,0,1))

    def mouse_move(self, obj, event):
        if self.mouse_left_pressed:
            lastXYpos = self.iren.GetLastEventPosition()
            lastX = lastXYpos[0]
            lastY = lastXYpos[1]

            xypos = self.iren.GetEventPosition()
            x = xypos[0]
            y = xypos[1]

            factor = 0.01
            roll = np.sign(x - lastX) * factor
            pitch = np.sign(lastY - y) * factor

            self.data['plate'].update_normal(self.data['plate'].normal + np.array([pitch, roll, 0]))
            