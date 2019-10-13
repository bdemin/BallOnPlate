from bodies.classes import BallPlateSystem


def main():
    ball_radius = 0.04
    plane_normal = (0, 0, 1)

    system = BallPlateSystem(plane_normal, ball_radius)
    system.init_visualization()
    system.init_callback()

    system.iren.Start()


def rl_model(system):
    # Input
    ball_pos = system.ball.pos_world
    ball_vel = system.ball.vel_world
    ball_acc = system.ball.acc_world

    # Output
    plate_normal = system.plane_normal
    


if __name__ == '__main__':
    main()
