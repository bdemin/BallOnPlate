import vtk


def create_sphere(radius, position):
    sphereSource = vtk.vtkSphereSource()
    sphereSource.SetCenter(position)
    sphereSource.SetRadius(radius)
    sphereSource.SetThetaResolution(20)
    sphereSource.SetPhiResolution(20)

    sphereMapper = vtk.vtkPolyDataMapper()
    sphereMapper.SetInputConnection(sphereSource.GetOutputPort())

    sphereActor = vtk.vtkActor()
    sphereActor.SetMapper(sphereMapper)
    sphereActor.SetPosition(position)
    sphereActor.GetProperty().SetColor(1, 0, 0)

    return sphereSource, sphereActor


def create_plane(point, normal):
    planeSource = vtk.vtkPlaneSource()
    planeSource.SetCenter(point)
    planeSource.SetNormal(normal)

    planeMapper = vtk.vtkPolyDataMapper()
    planeMapper.SetInputConnection(planeSource.GetOutputPort())

    planeActor = vtk.vtkActor()
    planeActor.SetMapper(planeMapper)
    planeActor.SetPosition(0, 0, 0)
    planeActor.GetProperty().SetColor(0, 0, 1)

    return planeSource, planeActor
