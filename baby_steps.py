from breadboard import *

def main():

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

    bb = {}
    bb = Breadboard()
    bb.draw(30,15)
    bb.add_mirror(20, 10, 45, 1)
    bb.add_mirror(20, 15, 180+45, 1)
    bb.place_mirrors()
    bb.shoot_laser((0, 10), (10, 10))
    plt.show()

    bb = {}
    bb = Breadboad()
    bb.draw(30,15)


if __name__ == "__main__":
    main()