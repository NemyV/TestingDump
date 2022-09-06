# import the necessary packages
import imutils
import cv2
import time
import win32api
from Source.ImgRec import form
from Source.window import Window
from Source.ImgRec import click
from Source.ImgRec import imginsideimg
from Source.ImgRec import movemouseto
from Source.GoGreen import gcolor

Topleftx = Window.WindowCoordArr[0]
Toplefty = Window.WindowCoordArr[1]
WIDTH = Window.WindowCoordArr[2]
HEIGHT = Window.WindowCoordArr[3]

coordinates = []
font = cv2.FONT_HERSHEY_COMPLEX
Screenshotx = 700
Screenshoty = 250


# when you need to take new screenshot
# time.sleep(1)
# pyautogui.screenshot('crop.jpg', region=(800, 250, 500, 500))
#
# # load the image, convert it to grayscale, and blur it slightly
# image = cv2.imread("crop.jpg")
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# gray = cv2.GaussianBlur(gray, (5, 5), 0)
################ READ THIS def contour needs todetect contour of green  READ THIS
# READ THIS   cursor and give back coordinates thats how you detect player position WORK ON THIS!!
### READ THIS

def countour(im, test=0):
    # load the image, convert it to grayscale, and blur it slightly
    global image
    image = cv2.imread(im)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # threshold the image, then perform a series of erosions +
    # dilations to remove any small regions of noise
    thresh = cv2.threshold(gray, 127, 150, cv2.THRESH_BINARY, 100)[1]

    # thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Testing
    if test != 0:
        cv2.imshow("Image", thresh)
        cv2.waitKey(0)

    # find contours in thresholded image, then grab the largest
    # one
    global cnts
    global c
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # print("this is cnts" , cnts)
    c = max(cnts, key=cv2.contourArea)


# # Extract green cursor from player location on image
# ggreen("testarea.png","green.png")
#
# countour("green.png")
# currentcord = (800, 900)
#
# print("this is cnts", cnts)
# print("this is c ", c)
# # countour("crop.jpg")


def cordmovement(x1, y1, x2, y2):
    print("these are x1 y1", x1, y1, "and x2 y2", x2, y2)
    # x1 y1 character coordinates x2 y2 closest wall coordinance
    distanco = 100
    up = [int(WIDTH / 2), int(HEIGHT / 2 + distanco)]
    down = [int(WIDTH / 2), int(HEIGHT / 2 - distanco)]
    left = [int(WIDTH / 2 - distanco), int(HEIGHT / 2)]
    right = [int(WIDTH / 2 + distanco), int(HEIGHT / 2)]

    LeftUp = [left[0], up[1]]
    RightUp = [right[0], up[1]]
    LeftDown = [left[0], down[1]]
    RightDown = [right[0], down[1]]

    # print(up, down, left, right)
    if x1 < x2 and y1 < y2:  # + and +
        print("doing RightUp")
        form.send_keystrokes('')
        win32api.SetCursorPos((RightUp))
        click(up[0], up[1], 'right')
        time.sleep(1)
    if x1 < x2 and y1 > y2:  # + and -
        print("doing RightDown")
        form.send_keystrokes('')
        win32api.SetCursorPos((RightDown))
        click(up[0], up[1], 'right')
        time.sleep(1)
    if x1 > x2 and y1 < y2:  # - and +
        print("doing LeftUp")
        form.send_keystrokes('')
        win32api.SetCursorPos((LeftUp))
        click(up[0], up[1], 'right')
        time.sleep(1)
    if x1 > x2 and y1 > y2:  # - and -
        print("doing LeftDown")
        time.sleep(0.5)
        form.send_keystrokes('')
        win32api.SetCursorPos((LeftDown))
        click(up[0], up[1], 'right')
        time.sleep(1)


Player = r"E:\Hello wolrd Python\LOSTARKB\Testplayer1.png"
test3 = r"E:\Hello wolrd Python\LOSTARKB\green.png"
test45 = r"E:\Hello wolrd Python\LOSTARKB\testarea.png"
print(Player)

from Source.LostARKFOCUS import focus_window

focus_window('LOST ARK ')

# PPos = imagesearch_numLoop(Player, 0.1, 10, 0.6)
time.sleep(1)

currentcord = (800, 900)

# countour("crop.jpg")
# time.sleep(0.5)
# form.send_keystrokes('')
# win32api.SetCursorPos((PPos))
# time.sleep(0.5)



def cntCoordinates(img, test=0):
    # find contours inside image
    countour(img)

    # Count number of contours
    count = 0
    for cnt in cnts:
        count += 1
    print("there is this many detected contour areas", count)

    # Main function
    for cnt in cnts:
        area = cv2.contourArea(cnt)
        # print(area)
        if area > 50:

            c = cnt

            # determine the most extreme points along the contour
            extLeft = tuple(c[c[:, :, 0].argmin()][0])
            extRight = tuple(c[c[:, :, 0].argmax()][0])
            extTop = tuple(c[c[:, :, 1].argmin()][0])
            extBot = tuple(c[c[:, :, 1].argmax()][0])

            # draw the outline of the object, then draw each of the
            # extreme points, where the left-most is red, right-most
            # is green, top-most is blue, and bottom-most is teal
            cv2.drawContours(image, [c], -1, (255, 0, 255), 2)
            cv2.circle(image, extLeft, 8, (0, 0, 255), -1)
            cv2.circle(image, extRight, 8, (0, 255, 0), -1)
            cv2.circle(image, extTop, 8, (255, 0, 0), -1)
            cv2.circle(image, extBot, 8, (255, 255, 0), -1)

            epsilon = 0.0000001 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            # Used to flatted the array containing
            # the co-ordinates of the vertices.
            n = approx.ravel()
            i = 0

            for j in n:
                if (i % 2 == 0):
                    x = n[i]
                    y = n[i + 1]
                    # ACTUAL COORDINATES ARE Screenshotx / Screenshoty
                    # print(x, y)
                    cord = [x + Screenshotx, y + Screenshoty]
                    coordinates.append(cord)
                    if test != 0:
                        # print(x + Screenshotx, y + Screenshoty)
                        # String containing the co-ordinates.
                        # string = str(x) + " " + str(y)
                        string = str(x + Screenshotx) + " " + str(y + Screenshoty)

                        if (i == 0):
                            # text on topmost co-ordinate.
                            cv2.putText(image, "Arrow tip", (x, y),
                                        font, 0.5, (255, 0, 0))
                        else:
                            # text on remaining co-ordinates.
                            cv2.putText(image, string, (x, y),
                                        font, 0.5, (0, 255, 0))
                i = i + 1
            # dist = lambda x, y: math.sqrt(((x[0] - y[0]) ** 2) + ((x[1] - y[1]) ** 2))
            dist = lambda x, y: (x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2
            closest = min(coordinates, key=lambda co: dist(co, currentcord))
            print("closest cord is :", closest)

            # cordmovement(PPos[0], PPos[1], closest[0], closest[1])

            if test != 0:
                # TESTING distance between 2 coordinates (probably x=800,y=900)
                time.sleep(0.5)
                form.send_keystrokes('')
                win32api.SetCursorPos((currentcord))
                time.sleep(0.5)
                # asfwgwg
                time.sleep(0.5)
                form.send_keystrokes('')
                win32api.SetCursorPos((closest))
                time.sleep(0.5)

                # show the output image
                cv2.imshow("Image", image)
                cv2.waitKey(0)
    return closest


# Extract green cursor from player location on image
gcolor("testarea.png", "green.png", nobackg=1)  # gcolor(Image, saveas="green.png", RGB='G'):

gcolor("testarea.png", "blue.png", RGB='B', nobackg=0)

# Find contour COORDINATES ## cntCoordinates ()
player = cntCoordinates("green.png", test=0)
print("return coordinate : ", player)

# Finding the exit COORDINATES
exit = imginsideimg("lookingforblue.png", "blue.png", Screenshotx, Screenshoty)
print("coordinates of the exit :", exit)
movemouseto(exit)

# print("this is cnts", cnts)
# print("this is c ", c)