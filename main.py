import numpy as np

import vtk

from bodies.classes import BallPlateSystem


def main():
    ball_radius = 0.04
    plane_normal = (0, 0, 1)

    system = BallPlateSystem(plane_normal, ball_radius)
    system.init_visualization()
    system.init_callback()

    system.iren.Start()


if __name__ == '__main__':
    main()
