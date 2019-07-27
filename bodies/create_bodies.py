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
    cubeSource = vtk.vtkPlaneSource()
    cubeSource.SetCenter(point)
    cubeSource.SetNormal(normal)

    cubeMapper = vtk.vtkPolyDataMapper()
    cubeMapper.SetInputConnection(cubeSource.GetOutputPort())

    cubeActor = vtk.vtkActor()
    cubeActor.SetMapper(cubeMapper)
    cubeActor.SetPosition(0, 0, 0)
    cubeActor.GetProperty().SetColor(0, 0, 1)

    return cubeSource, cubeActor
