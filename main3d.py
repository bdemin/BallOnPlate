import numpy as np
#import mpl_toolkits.mplot3d.axes3d as p3
from mpl_toolkits.mplot3d import Axes3D
import scipy.constants
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from classes.Plate import Plate
from classes.Ball import Ball


def find_angle(vec1, vec2):
    num = vec1.dot(vec2)
    den = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    return np.rad2deg(np.arccos(num/den))

fig1 = plt.figure()
ax1 = fig1.gca(projection = '3d')
#ax1.set_aspect('equal')
ax1.set_xlim3d(-2,2)
ax1.set_ylim3d(-2,2)
ax1.set_zlim3d(-2,2)


#fig1.set_figheight(7)
#fig1.set_figwidth(7)
#ax1 = fig1.add_subplot(111, projection = '3d')


ball_r = 0.5
ball_b = 1
ball_m = 100
ball_I = 0.5*ball_m*ball_r**2
const = -scipy.constants.g/(1+(ball_I/(ball_m*ball_b^2)))

#normal = np.array([0,1,10])
normal = np.array([0,0,1])

point = np.array((0,0,0))
plate = Plate(point, normal)
ball = Ball(ball_r, plate.normal)


plane = plate.DrawPlate(ax1)
sphere = ball.DrawBall(ax1)



#angle_text = ax1.text(0.05, 0.9, '', transform = ax1.transAxes)
#time_template = 'Angle = %i[deg]'

#def press(event):
##    if self.angle < np.deg2rad(45) and self.angle > np.deg2rad(-45):
#    if event.key == 'a'and plate.angle < np.deg2rad(angle_limit):
#        plate.TiltPlate(1 * (np.pi/180))
#    if event.key == 'd' and plate.angle > np.deg2rad(-angle_limit):
#        plate.TiltPlate(-1 * (np.pi/180))
#    sys.stdout.flush()
        

def init():
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_zlim(-1, 1)
#    angle_text.set_text('')
    return plane, sphere
#    
def animate(i):
#    ball.acc = const*np.sin(find_angle(plate.angle, np.array([1,0,0])))
##    2d angle?
#    
#    ball.acc = const*np.sin(plate.angle)
#    ball.pvel = ball.pvel_last + ball.acc*dt
#    ball.ppos = ball.ppos_last + ball.pvel*dt
#    
#    ball.Move(0.5 + ball.ppos*np.cos(plate.angle),
#              0.5 + ball.rad/np.cos(plate.angle) + ball.ppos*np.sin(plate.angle))
#    
#    ball.ppos_last = ball.ppos
#    ball.pvel_last = ball.pvel
#    
#    line.set_data(plate.x_coords, plate.y_coords)
#    circle = ball.DrawBall(ax1)
#    angle_text.set_text(time_template % ((180/np.pi)*plate.angle))
    plate.z = (-i*normal[0]*plate.xx - normal[1]*plate.yy - plate.d) * 1./normal[2]
    plane = plate.DrawPlate(ax1)
    sphere = ball.DrawBall()
    
    print(i)
    return plane, sphere


#fig1.canvas.mpl_connect('key_press_event', press)
T = 6
FPS = 48
total_frames = T*FPS
dt = (1/FPS)
#anim = animation.FuncAnimation(fig1, animate, interval = dt*1000,
#                               init_func = init, blit = True,
#                               repeat = False)
plt.show()