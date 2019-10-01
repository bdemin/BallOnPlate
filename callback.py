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
        self.system.update_positions()
        # self.system.ball.place_ball()

     
        # self.ball.plate_pos = (0, 0, ball_z)
        # self.ball.update_position(self.dt)
        
        # print(self.ball.plate_pos)
        if (np.abs(self.system.ball.pos_world) > 0.5).any():
            self.system.update_normal((0, 0, 1))
            # self.system.ball.plate_pos = np.array((0, 0, 0))
            # self.system.ball.plate_vel = np.array((0, 0, 0))
            # self.system.ball.plate_acc = np.array((0, 0, 0))

            self.system.pos_world = np.array((0, 0, self.system.ball.radius/2))
            self.system.vel_world = np.array((0, 0, 0))
            self.system.acc_world = np.array((0, 0, 0))
        
        obj.GetRenderWindow().Render()
        self.timer += 1

    def mouse_button(self, obj, event):
        if event == "LeftButtonPressEvent":
            self.mouse_left_pressed = True
        elif event == "LeftButtonReleaseEvent":
            self.mouse_left_pressed = False
        elif event == "RightButtonPressEvent":
            self.system.update_normal((0,0,1))

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

            self.system.update_normal(self.system.normal + np.array([pitch, roll, 0]))
            
    def key_press(self, obj, event):
        key = obj.GetKeySym()
        if key == 'e':
            self.iren.DestroyTimer()
            self.iren.GetRenderWindow().Finalize()
            self.iren.TerminateApp()
            