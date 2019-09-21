from vtk import vtkCamera


class vtkTimerCallback(object):
    def __init__(self, renderer, renWin):
        self.timer = 1
        
        self.renderer = renderer

        cam_distance = (1, 1, 1)
        self.camera = vtkCamera()
        self.renderer.SetActiveCamera(self.camera)
        self.camera.SetViewUp(0,0,1)
        self.camera.SetFocalPoint(0, 0, 0)
        self.camera.SetPosition(cam_distance)
        

    def keypress(self, obj, event):
        pass


    def execute(self, obj, event):
        normal = self.data['plate'].normal
        self.data['plate'].source.SetNormal(*normal)
        self.data['plate'].source.Update()

        obj.GetRenderWindow().Render()
        self.timer += 1

