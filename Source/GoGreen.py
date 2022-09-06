import cv2
import numpy as np

"testarea.png"


def gcolor(Image, saveas="green.png", RGB='G', nobackg=0):
    ## Read
    img = cv2.imread(Image)

    ## convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    ## mask of green (36,25,25) ~ (86, 255,255)
    # mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))

    rmask = cv2.inRange(hsv, (0, 215, 189), (50, 255, 255))  ##Red mask
    rmask = rmask.astype('bool')
    rmask2 = cv2.inRange(hsv, (170, 100, 0), (180, 255, 255))
    rmask2 = rmask2.astype('bool')

    gmask = cv2.inRange(hsv, (55, 75, 55), (70, 255, 255))  # Green mask
    gmask = gmask.astype('bool')

    bmask = cv2.inRange(hsv, (75, 140, 175), (120, 200, 255))  # Blue Mask
    bmask = bmask.astype('bool')

    # maskmax = mask + mask2  ## Adding 2 masks #later displaying them both
    # cv2.imshow("resultingIMG",img * np.dstack((mask, mask, mask)))
    ## slice the mask
    if RGB == 'R':
        imask = rmask > 0
    if RGB == 'G':
        imask = gmask > 0
    if RGB == 'B':
        imask = bmask > 0

    color = np.zeros_like(img, np.uint8)
    color[imask] = img[imask]

    # pixels = img.load()  # create the pixel map
    #
    # for i in range(img.size[0]):  # for every pixel:
    #     for j in range(img.size[1]):
    #         if pixels[i, j] != (0, 0, 0):  # if not black:
    #             pixels[i, j] = (255, 255, 255)  # change to white
    ## save
    cv2.imwrite(saveas, color)
    # Convert/DELETE BLACK PIXELS(BACKGROUND)\
    if nobackg != 0:
        src = cv2.imread(saveas, 1)
        tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
        b, g, r = cv2.split(src)
        rgba = [b, g, r, alpha]
        dst = cv2.merge(rgba, 4)
        cv2.imwrite(saveas, dst)


gcolor("Green2Blue2.png", RGB='B')
