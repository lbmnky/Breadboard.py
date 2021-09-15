from breadboard import *

def main():

    bb = {}
    for i in range(4):
        bb[i] = Breadboard()
        bb[i].draw(9, 12, False)

        bb[i].add_mirror(10, 26, -45, -1, 2.5)

        alpha = 5 + 25 * i
        beta = 5

        xc = 10
        yc = 6
        xc_s = xc - .8 * np.cos(rad(alpha))
        yc_s = yc  - .8 * np.sin(rad(alpha))
        r = 5

        bb[i].add_mirror(xc_s, yc_s, 180 + alpha, -1)
        bb[i].draw_circle(xc, yc, r + 1)

        xn = xc + r * np.cos(rad(+alpha * 2 + 90))
        yn = yc + r * np.sin(rad(+alpha * 2 + 90))

        bb[i].add_mirror(xn, yn, 180 + alpha * 2 + beta, 1, 1.25)

        xm = xc + (2.54-0.8) * np.cos(rad(alpha))
        ym = yc + (2.54-0.8) * np.sin(rad(alpha))

        bb[i].add_mirror(xm, ym, 180 + alpha, -1)
        bb[i].add_mirror(14.5, 26, 45 - beta, -1)

        bb[i].place_mirrors()

        bb[i].shoot_laser((0, 26), (10, 26))
        plt.title(f"AOI = {alpha}°")
    plt.show()


if __name__ == "__main__":
    main()
