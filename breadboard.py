import numpy as np
import matplotlib.pyplot as plt


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def mirror_coordinates(center, rot, r):
    x1 = center[0] + r * np.cos(rot)
    y1 = center[1] + r * np.sin(rot)
    x2 = center[0] - r * np.cos(rot)
    y2 = center[1] - r * np.sin(rot)
    return[(x1,y1),(x2,y2)]


# hole pattern
lx = 30
ly = 15
nx, ny = (lx, ly)
x = np.linspace(0, 2.54*(lx-1), nx)
y = np.linspace(0, 2.54*(ly-1), ny)
xv, yv = np.meshgrid(x, y)

# Mirror diameter
R = 2.54 / 2

M_center = []
M_rot = []

# M1
M_center.append((5,16))
M_rot.append(-45 / 360 * 2 * np.pi)

#M2
M_center.append((5, 6))
M_rot.append(135 / 360 * 2 * np.pi)

#M2
M_center.append((50, 6))
M_rot.append(45 / 360 * 2 * np.pi)


# extend and rotate mirrors
M = [mirror_coordinates(M_center[i],M_rot[i],R) for i in range(len(M_center))]

Laser = []
# origin and direction
Laser.append([(0, 16), (10, 16)])

# bounce laser off of mirrors
for i in range(len(M)):
    intersect = line_intersection((Laser[i][0],Laser[i][1]),M[i])
    Laser[i][1] = intersect
    dx = Laser[i][1][0] - Laser[i][0][0]
    dy = Laser[i][1][1] - Laser[i][0][1]
    laser_angle = np.arccos(dx / np.sqrt(dx**2 + dy**2))
    new_dir_x = intersect[0] + lx * 2.54 * np.cos(laser_angle + 2 * M_rot[i])
    new_dir_y = intersect[1] + ly * 2.54 * np.sin(laser_angle + 2 * M_rot[i])
    Laser.append([intersect,(new_dir_x, new_dir_y)])

# plot that breadboard
figure, axes = plt.subplots(1)
axes.set_facecolor('lightgray')
axes.plot(xv,
          yv,
          'gray',
          marker='o',
          markerfacecolor='silver',
          markeredgecolor='dimgray', linestyle='none')


[axes.plot([Laser[i][0][0], Laser[i][1][0]], [Laser[i][0][1], Laser[i][1][1]],
          'r-',
          linewidth=3) for i in range(len(Laser))]

#axes.plot([Laser[1][0][0], Laser[1][1][0]], [Laser[1][0][1], Laser[1][1][1]],
#          'k-',
#          linewidth=3)

[axes.plot([M[i][0][0], M[i][1][0]], [M[i][0][1], M[i][1][1]],
           'b', linewidth=5) for i in range(len(M))]

plt.ylim(-1*2.54, ly*2.54)
plt.xlim(-1*2.54, lx*2.54)
axes.set_aspect(1)
plt.show()
