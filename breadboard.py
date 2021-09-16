import numpy as np
import matplotlib.pyplot as plt
import shapely.geometry
import descartes

class Breadboard:
    ''' docstring '''
    def __init__(self):
        self.mirror_center = []
        self.mirror_rot = []
        self.mirror_side = []
        self.mirror = []
        self.laser = []

    def draw(self, nx, ny, anodized=True):
        ''' doc '''

        if anodized is True:
            fc_color = 'xkcd:almost black'
            hl_color = 'xkcd:dark blue gray'
        else:
            fc_color = 'lightgray'
            hl_color = 'silver'

        fig, self.ax = plt.subplots( 1 , figsize=(nx/2,ny))

        self.ax.set_facecolor(fc_color)

        x = np.linspace(0, 2.54*(nx-1), nx)
        y = np.linspace(0, 2.54*(ny-1), ny)
        for i in range(nx):
            for j in range(ny):
                holes = shapely.geometry.Point([x[i], y[j]])
                poly = holes.buffer(0.3)
                patch = descartes.PolygonPatch(poly,
                                   fc=hl_color,
                                   ec='dimgray',
                                   alpha=0.75,
                                   zorder=10)
                self.ax.add_patch( patch )
        self.ax.set_aspect( 1 )
        self.ax.set_ylim(-2.54, ny * 2.54)
        self.ax.set_xlim(-2.54, nx * 2.54)

    def add_mirror(self, x , y, rot, s, D=2.54):
        ''' doc '''
        self.mirror_center.append((x, y))
        self.mirror_rot.append(rad(rot))
        self.mirror.append(mirror_coordinates((x, y), rad(rot), D / 2))
        self.mirror_side.append(s)

    def place_mirrors(self):
        ''' doc '''
        for i in range(len(self.mirror)):
            #for i in self.mirror:
            xvals = [self.mirror[i][0][0], self.mirror[i][1][0]]
            yvals = [self.mirror[i][0][1], self.mirror[i][1][1]]
            #xvals = [i[0][0]], i[1][0]]
            #yvals = [i[0][1]], i[0][0]]
            temp = shapely.geometry.LineString(self.mirror[i])
            poly = temp.buffer(.6 * self.mirror_side[i], single_sided=True)
            patch = descartes.PolygonPatch(poly, fc='silver', ec='k', zorder=20)
            self.ax.add_patch(patch)
            temp = shapely.geometry.LineString(self.mirror[i])
            poly = temp.buffer(.2 * self.mirror_side[i], single_sided=True)
            patch = descartes.PolygonPatch(poly, fc='w', ec='none', zorder=20)
            self.ax.add_patch(patch)

    def draw_circle(self, x, y ,r):
        angle = np.linspace(0, 2 * np.pi, 150)
        xx = r * np.cos(angle) + x
        yy = r * np.sin(angle) + y
        self.ax.fill(xx,yy,fc='dimgray',ec='k',zorder=10)

    def shoot_laser(self, o1, o2):
        # origin and direction
        self.laser.append(o1)
        self.laser.append(o2)

        # bounce laser off of mirrors (should work automatically)
        for i in range(len(self.mirror)):
            intersect = line_intersection((self.laser[i], self.laser[i + 1]), self.mirror[i])
            self.laser[i + 1] = intersect
            dx = self.laser[i + 1][0] - self.laser[i][0]
            dy = self.laser[i + 1][1] - self.laser[i][1]
            if dx <= 0 and dy <= 0:
                fx = -1
                fy = -1
            elif dx <= 0 and dy >= 0:
                fx = -1
                fy =  1
            elif dx >= 0 and dy <= 0:
                fx =  1
                fy = 1
            elif dx >= 0 and dy >= 0:
                fx =  1
                fy =  -1
            else:
                print('error')
                print(dx)
                print(dy)

            r = np.sqrt(dx**2 + dy**2)
            laser_angle = fx * fy * np.arccos(dx / r)
            new_dir_x = intersect[0] + 2 * 2.54 * np.cos(laser_angle + 2 * self.mirror_rot[i])
            new_dir_y = intersect[1] + 2 * 2.54 * np.sin(laser_angle + 2 * self.mirror_rot[i])
            self.laser.append((new_dir_x, new_dir_y))

        self.laser = shapely.geometry.LineString(self.laser)
        poly = self.laser.buffer(0.25, single_sided=False)
        patch = descartes.PolygonPatch(poly, fc='red', ec='darkred', alpha=0.75, zorder=10)
        self.ax.add_patch(patch)

def rad(phi):
    ''' doc '''
    return phi / 360 * 2 * np.pi



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

    #print(y)
    #print(min(line2[:][1]))
    #print(max(line2[:][1]))
    print([line2[0][1], line2[1][1]])
    print(x, y)
    if min([line2[0][1], line2[1][1]]) < y < max([line2[0][1], line2[1][1]]):
        if min([line2[0][0], line2[1][0]]) < x < max([line2[0][0], line2[1][0]]):
            print('laser hits mirror')
        else:
            print('laser misses mirror in x')
            x = line1[1][0]
            y = line1[1][1]
    else:
        print('laser misses mirror in y')
        x = line1[1][0]
        y = line1[1][1]

    print(x, y)
    return x, y

def mirror_coordinates(center, rot, r):
    x1 = center[0] + r * np.cos(rot)
    y1 = center[1] + r * np.sin(rot)
    x2 = center[0] - r * np.cos(rot)
    y2 = center[1] - r * np.sin(rot)
    return[(x1,y1),(x2,y2)]


'''

# hole pattern
lx = 30
ly = 15
nx, ny = (lx, ly)
x = np.linspace(0, 2.54*(lx-1), nx)
y = np.linspace(0, 2.54*(ly-1), ny)

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

# bounce laser off of mirrors (should work automatically)
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

# plot that breadboard
figure, axes = plt.subplots(1)
axes.set_facecolor(bb_color)


for i in range(lx):
    for j in range(ly):
        Holes = shapely.geometry.Point([x[i], y[j]])
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
'''
