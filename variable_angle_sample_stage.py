from breadboard import *

def main():
    bb1 = Breadboard()
    bb1.draw(30, 15, False)

    bb1.add_mirror(10, 26, -45, -1)

    alpha = 45
    beta = 5

    xc = 10
    yc = 6
    r = 5

    bb1.add_mirror(xc, yc, 180 + alpha, -1)
    bb1.draw_circle(xc, yc, r)

    xn = xc + r * np.sin(rad(180 + alpha * 2))
    yn = yc - r * np.cos(rad(180 + alpha * 2))

    bb1.add_mirror(xn, yn, 180 + alpha * 2 + beta, 1)

    #xn = xn - r * np.sin(rad(180 + alpha))
    #yn = yn + r * np.cos(rad(180 + alpha))

    bb1.add_mirror(xc, yc, 180 + alpha, -1)
    bb1.add_mirror(14.5, 26, 45 - beta, -1)

    bb1.place_mirrors()

    bb1.shoot_laser((0, 26), (10, 26))
    plt.show()


if __name__ == "__main__":
    main()
