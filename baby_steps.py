from breadboard import *

def main():

    case = 'abs mirrors' # angle, abs mirrors, rel mirrors

    if case == 'angle':
        # demonstrate variable angle of mirrors
        bb = {}
        for i in range(10):
            angle = 10 * (i+1)
            bb[i] = Breadboard()
            bb[i].draw(30, 15, anodized=False)
            bb[i].add_mirror(10, 10, angle, 1)
            bb[i].place_mirrors()
            bb[i].shoot_laser((0, 10), (10, 10))
            plt.title(f"angle {angle}°")
            plt.xlim(0, 20)
            plt.ylim(0, 20)
        plt.show()
    elif case == 'abs mirrors':
        # place two mirrors
        bb = {}
        bb = Breadboard()
        bb.draw(30,15)
        bb.add_mirror(5, 20, 45, 1)
        #bb.add_mirror(20, 15, 180+45, 1)
        bb.place_mirrors()
        bb.shoot_laser((0, 10), (10, 10))
        plt.show()
    elif case == 'rel mirrors':
        # place two mirrors relative
        bb = {}
        bb = Breadboard()
        bb.draw(30,15,anodized=False)
        x1 = 20
        y1 = 10
        angle1 = 15
        bb.add_mirror(x1, y1, angle1, 1)
        l2 = 15
        x2 = x1 + l2 * np.cos(rad(angle1*2))
        y2 = y1 + l2 * np.sin(rad(angle1*2))
        angle2 = angle1
        bb.add_mirror(x2, y2, angle2 + 180, 1)
        x3 = x2 + 20
        y3 = y2
        bb.add_mirror(x3,y3,45,1)
        bb.place_mirrors()
        bb.shoot_laser((0, 10), (10, 10))
        plt.show()


if __name__ == "__main__":
    main()