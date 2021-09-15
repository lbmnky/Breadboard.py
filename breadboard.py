import numpy as np
import matplotlib.pyplot as plt
import shapely.geometry
import descartes
#from shapely.figures import plot_line, plot_bounds, color_issimple


#def plot_lines(ax, ob):
#    color = color_issimple(ob)
#    for line in ob:
#        plot_line(ax, line, color=color, alpha=0.7, zorder=2)



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

bb = 'light'
if bb == 'dark':
    bb_color = 'xkcd:almost black'
    hole_color = 'xkcd:dark blue gray'
else:
    bb_color = 'lightgray'
    hole_color = 'silver'

# Mirror diameter
R = 2.54 / 2

M_center = []
M_rot = []
Mside = []

# M1
M_center.append((5,16))
M_rot.append(-45 / 360 * 2 * np.pi)
Mside.append(-1)

#M2
M_center.append((5, 6))
M_rot.append(135 / 360 * 2 * np.pi)
Mside.append(-1)

#M3
M_center.append((50, 6))
M_rot.append(45 / 360 * 2 * np.pi)
Mside.append(1)

#M4
M_center.append((49.5, 25))
M_rot.append(45 / 360 * 2 * np.pi)
Mside.append(-1)


# extend and rotate mirrors
Mirror = [mirror_coordinates(M_center[i],M_rot[i],R) for i in range(len(M_center))]

Laser = []
# origin and direction
Laser.append(( 0, 16))
Laser.append((10, 16))

print(Laser[1])
# bounce laser off of mirrors
for i in range(len(Mirror)):
    intersect = line_intersection((Laser[i], Laser[i + 1]), Mirror[i])
    Laser[i+1] = intersect
    dx = Laser[i+1][0] - Laser[i][0]
    dy = Laser[i+1][1] - Laser[i][1]
    fx = 1
    if dx < 0:
        fx = -1
    fy = 1
    if dy > 0:
        fy = -1
    r = np.sqrt(dx**2 + dy**2)
    laser_angle = fx * fy * np.arccos(dx / r)
    new_dir_x = intersect[0] + lx * 2.54 * np.cos(laser_angle + 2 * M_rot[i])
    new_dir_y = intersect[1] + ly * 2.54 * np.sin(laser_angle + 2 * M_rot[i])
    Laser.append((new_dir_x, new_dir_y))

print(Laser)
# plot that breadboard
figure, axes = plt.subplots(1)
axes.set_facecolor(bb_color)

for i in range(lx):
    for j in range(ly):
        Holes = shapely.geometry.Point([xv[j][i], yv[j][i]])
        poly = Holes.buffer(0.3)
        patch = descartes.PolygonPatch(poly,
                                   fc=hole_color,
                                   ec='dimgray',
                                   alpha=0.75,
                                   zorder=10)
        axes.add_patch(patch)


Laser = shapely.geometry.LineString(Laser)
poly = Laser.buffer(0.25, single_sided=False)
patch = descartes.PolygonPatch(poly, fc='red', ec='darkred', alpha=0.75, zorder=10)
axes.add_patch(patch)

for i in range(len(Mirror)):
    xvals = [Mirror[i][0][0], Mirror[i][1][0]]
    yvals = [Mirror[i][0][1], Mirror[i][1][1]]
    temp = shapely.geometry.LineString(Mirror[i])
    poly = temp.buffer(.6 * Mside[i], single_sided=True)
    patch = descartes.PolygonPatch(poly, fc='silver', ec='k', zorder=20)
    axes.add_patch(patch)
    axes.plot(xvals, yvals, 'b', linewidth=2, zorder=40)

plt.ylim(-1*2.54, ly*2.54)
plt.xlim(-1*2.54, lx*2.54)
axes.set_aspect(1)
plt.show()
