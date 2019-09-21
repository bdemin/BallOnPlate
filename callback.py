class vtkTimerCallback(object):
    def __init__(self, renderer, renWin):
        self.timer = 1
        
        self.renderer = renderer
        # self.camera = vtkCamera()
        # self.renderer.SetActiveCamera(self.camera)
        

    def keypress(self, obj, event):
        pass

    def execute(self, obj, event):
        # self.data

        obj.GetRenderWindow().Render()
        self.timer += 1
