import glob
from os import path
import cv2
import numpy as np
import pyautogui
import pydirectinput
import random
import time
import re
import numpy
import pyscreenshot as ImageGrab
from PIL import ImageEnhance, ImageOps
from PIL import Image
import PIL.Image
from numpy import asarray
from pytesseract import *
import pytesseract
from PIL import ImageTk, Image

import sys
sys.path.insert(0, 'E:\Hello wolrd Python\LOSTARKB')

#Import from other files/classes
# from METHODS import WindowMgr



'''
grabs a region (topx, topy, bottomx, bottomy)
to the tuple (topx, topy, width, height)
input : a tuple containing the 4 coordinates of the region to capture
output : a PIL image of the area selected.
'''


def region_grabber(region):
    x1 = region[0]
    y1 = region[1]
    width = region[2] - x1
    height = region[3] - y1

    return pyautogui.screenshot(region=(x1, y1, width, height))


'''
Searchs for an image within an area
input :
image : path to the image file (see opencv imread for supported types)
x1 : top left x value
y1 : top left y value
x2 : bottom right x value
y2 : bottom right y value
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8
im : a PIL image, usefull if you intend to search the same unchanging region for several elements
returns :
the top left corner coordinates of the element if found as an array [x,y] or [-1,-1] if not
'''


def imagesearcharea(image, x1, y1, x2, y2, precision=0.8, im=None):
    if im is None:
        im = region_grabber(region=(x1, y1, x2, y2))
        # im.save('testarea.png') usefull for debugging purposes, this will save the captured region as "testarea.png"

    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc


'''
click on the center of an image with a bit of random.
eg, if an image is 100*100 with an offset of 5 it may click at 52,50 the first time and then 55,53 etc
Usefull to avoid anti-bot monitoring while staying precise.
this function doesn't search for the image, it's only ment for easy clicking on the images.
input :
image : path to the image file (see opencv imread for supported types)
pos : array containing the position of the top left corner of the image [x,y]
action : button of the mouse to activate : "left" "right" "middle", see pyautogui.click documentation for more info
time : time taken for the mouse to move from where it was to the new position
'''


def click_image(image, pos, action, timestamp, offset=5):
    img = cv2.imread(image)
    height, width, channels = img.shape
    pyautogui.moveTo(pos[0] + r(width / 2, offset), pos[1] + r(height / 2, offset),
                     timestamp)
    pyautogui.click(button=action)


'''
Searchs for an image on the screen
input :
image : path to the image file (see opencv imread for supported types)
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8
im : a PIL image, usefull if you intend to search the same unchanging region for several elements
returns :
the top left corner coordinates of the element if found as an array [x,y] or [-1,-1] if not
'''


def imagesearch(image, precision=0.8):
    im = pyautogui.screenshot()
    # im.save('testarea.png') usefull for debugging purposes, this will save the captured region as "testarea.png"
    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc


'''
Searchs for an image on screen continuously until it's found.
input :
image : path to the image file (see opencv imread for supported types)
time : Waiting time after failing to find the image
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8
returns :
the top left corner coordinates of the element if found as an array [x,y]
'''


def imagesearch_loop(image, timesample, precision=0.8):
    pos = imagesearch(image, precision)
    while pos[0] == -1:
        # print(image + " not found, waiting")
        time.sleep(timesample)
        pos = imagesearch(image, precision)
        # print(pos)
    return pos


'''
Searchs for an image on screen continuously until it's found or max number of samples reached.
input :
image : path to the image file (see opencv imread for supported types)
time : Waiting time after failing to find the image
maxSamples: maximum number of samples before function times out.
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8
returns :
the top left corner coordinates of the element if found as an array [x,y]
'''


def imagesearch_numLoop(image, timesample, maxSamples, precision=0.8):
    pos = imagesearch(image, precision)
    count = 0
    while pos[0] == -1:
        # print(image + " not found, waiting")
        time.sleep(timesample)
        pos = imagesearch(image, precision)
        count = count + 1
        if count > maxSamples:
            break
    return pos


def Searchimage_returncount(image, timesample, maxSamples, precision=0.8):
    pos = imagesearch(image, precision)
    count = 0
    while pos[0] == -1:
        print(image + " not found, waiting")
        time.sleep(timesample)
        pos = imagesearch(image, precision)
        count = count + 1
        if count > maxSamples:
            break
    return pos


# Same as above just returns count
def Search_image_return_count(image, timesample, maxSamples, precision=0.8):
    pos = imagesearch(image, precision)
    count = 0
    while pos[0] == -1:
        print(image + " not found, waiting")
        # print("not found after :")
        # print(count)
        time.sleep(timesample)
        pos = imagesearch(image, precision)
        count = count + 1
        if count > maxSamples:
            break
    else:
        print(image + " found")
        # print('After this many samples image found:')
        # print(count)
    return count


'''
Searchs for an image on a region of the screen continuously until it's found.
input :
image : path to the image file (see opencv imread for supported types)
time : Waiting time after failing to find the image
x1 : top left x value
y1 : top left y value
x2 : bottom right x value
y2 : bottom right y value
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.8
returns :
the top left corner coordinates of the element as an array [x,y]
'''


def imagesearch_region_loop(image, timesample, x1, y1, x2, y2, precision=0.8):
    pos = imagesearcharea(image, x1, y1, x2, y2, precision)

    while pos[0] == -1:
        time.sleep(timesample)
        pos = imagesearcharea(image, x1, y1, x2, y2, precision)
    return pos


'''
Searches for an image on the screen and counts the number of occurrences.
input :
image : path to the target image file (see opencv imread for supported types)
precision : the higher, the lesser tolerant and fewer false positives are found default is 0.9
returns :
the number of times a given image appears on the screen.
optionally an output image with all the occurances boxed with a red outline.
'''


def imagesearch_count(image, precision=0.9):
    img_rgb = pyautogui.screenshot()
    img_rgb = np.array(img_rgb)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= precision)
    count = 0
    for pt in zip(*loc[::-1]):  # Swap columns and rows
        # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2) // Uncomment to draw boxes around found occurances
        count = count + 1
    # cv2.imwrite('result.png', img_rgb) // Uncomment to write output image with boxes drawn around occurances
    return count


def searchimageinarea(image, x1, y1, x2, y2, precision=0.8, im=None):
    # if im is None:
    #     #im = region_grabber(region=(x1, y1, x2, y2))
    #     im = ImageGrab.grab(bbox =(x1, y1, x2, y2))
    #     # im.save('testarea.png') usefull for debugging purposes, this will save the captured region as "testarea.png"
    img_rgb = pyautogui.screenshot()
    # this is cropped screenshot
    # print(x1)
    # print(y1)
    # print(x2)
    # print(y2)
    img_rgb.crop((x1, y1, x2, y2)).save('MIDDLEsearch.png')
    crop_img = img_rgb
    crop_img = asarray(crop_img)
    img_gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    template = cv2.imread(image, 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val < precision:
        return [-1, -1]
    return max_loc


def ImageCropSEARCH(image, x1, y1, x2, y2, timesample, precision=0.8):
    pos = searchimageinarea(image, x1, y1, x2, y2, precision)

    while pos[0] == -1:
        time.sleep(timesample)
        pos = searchimageinarea(image, x1, y1, x2, y2, precision)
    return pos


def r(num, rand):
    return num + rand * random.random()


def PressKey_image(image):
    img = cv2.imread(image)
    height, width, channels = img.shape
    x = path.basename(image)[0]
    pyautogui.press('' + x)


def Fishing():
    while True:
        count = 0
        # cast W at position START
        pydirectinput.moveTo(1200, 642)

        # Check if you can cast NET/Possibly same as normal one with priority of finding net
        for f in FINDFishingSTART:
            pos = imagesearch(f, 0.9)
            print(pos)
            # pydirectinput.moveTo(int(pos[0]),int(pos[1]))
            if pos != [-1, -1]:
                pydirectinput.press('a')
                count = 1
                time.sleep(6)
            else:
                pydirectinput.press('w')

        if count == 1:
            print("count is :")
            print(count)
            for i in range(0, 20, 1):
                # repetition time in loop add it
                for f in FINDFishingNETGAME:
                    # search for exclamation mark
                    pos = imagesearch_region_loop(f, 230, 270, 500, 700, 0.05, 0.8)
                    if pos != [-1, -1]:
                        print("Found PERFECT")
                        for i in range(0, 20, 1):
                            pydirectinput.press('space')
                            time.sleep(0.07)

        # If you want to cast buffs
        # for f in FishingBUFFS:
        # search for exclamation mark
        for f in FINDFishingCATCH:
            # search for exclamation mark
            time.sleep(5)
            print("this is a string :")
            print(f)
            # pos = imagesearch_loop(f, 0.1)
            # pos = imagesearch_region_loop(f, TOPLMIDLE[0],TOPLMIDLE[1], BOTRMIDLE[0],BOTRMIDLE[1], 0.05, 0.8)
            pos = ImageCropSEARCH(f, TOPLMIDLE[0], TOPLMIDLE[1], BOTRMIDLE[0], BOTRMIDLE[1], 0.05, 0.8)
            print(pos)
            if pos != [-1, -1]:
                print("FOUND MARK")
                pydirectinput.press('w')
                time.sleep(6)
        print("finished fishing loop")


def Start_of_stage(count):
    count += 1
    pyautogui.click(990, 160, button='right')
    time.sleep(2)
    if count == 2:
        return count
    print("finished this shit")  # ends the if and foo at the same time


def Click_on_Image(image, action, timestamp, repeat, offset=5):
    # print("click on image started")
    count = 0
    randomnumber = random.randint(1, 5)  # Integer from 1 to 10, endpoints included
    randomnumber1 = random.randint(1, 6)
    randomfloat = random.uniform(0.2, 1)
    for i in range(0, repeat, 1):
        # count += 1
        string = 'Clicking on: ' + image
        img = cv2.imread(image)
        # Get position of "image" [imagesearch_loop(image, timesample, precision=0.8):] !!!!!!!!!!!!!!!!!!!
        pos = imagesearch_numLoop(image, 0.5, 2)

        height, width, channels = img.shape
        time.sleep(randomfloat)
        if pos != [-1, -1]:
            x = int(pos[0] + r(width / 2, offset))
            y = int(pos[1] + r(height / 2, offset))
            pydirectinput.click(x, y, timestamp)
            #pydirectinput.moveTo(int(pos[0] + r(width / 2, offset)), int(pos[1] + r(height / 2, offset)), timestamp)

        # # action ( (button='left')
        # x, y = pyautogui.position()
        # if x > 100:
        #     print(string)
        #     pydirectinput.click(button=action)
        # else:
        #     print('this is height of x:')
        #     print(height)
    return pos
    # print(count)
    # return count


def REVIVECHARACTER():
    # randomnumber = random.randint(1, 5)  # Integer from 1 to 10, endpoints included
    # randomnumber1 = random.randint(1, 6)
    # randomfloat = random.uniform(0.2, 1)
    # list1 = ['w', 's']
    # defense = ['d', 'e']
    # randomjump = ['r', 'a']
    # randomATTACK = random.sample(list1, 1)
    # randomDEFENSE = random.sample(defense, 1)
    for f in checkIFDEAD:
        Click_on_Image(f, 'left', 2, 1)
    time.sleep(2.1)
    pydirectinput.press('v')
    time.sleep(2)
    Skills_no_movement(23)


def ENTERstage():
    print("Enter stage has started")
    for z in checkIFENTER:
        Click_on_Image(z, 'left', 2, 1)


def ENDSTAGE(image):
    pyautogui.click(990, 160, button='right')
    time.sleep(2)


def StateCHECKimg(repeat):
    count = 0;
    countreward = 0;
    # looksofr image this amount of times before it gives up
    thistimes = 4
    for i in range(0, repeat, 1):
        print('STATECHECKING COUNT is :')
        print(count)
        # count = imagesearch_count(checkstate + 'reward for passings.bmp')
        for g in checkIFDEAD:
            print('Current state is:')
            print(g)
            # g = str
            count = Search_image_return_count(g, 0.1, thistimes, 0.9)
            if count < 3:
                print('Character died reviving...')
                print(count)
                REVIVECHARACTER()
        for z in checkIFENTER:
            count = Search_image_return_count(z, 0.1, thistimes, 0.9)
            if count < 4:
                print('Entering stage...')
                ENTERstage()
                Skills_no_movement(23)
        for c in checkIFDISMANTLE:
            count = Search_image_return_count(c, 0.1, thistimes, 0.85)
            if count < 4:
                DismantleBalls()


def Skills_no_movement(repeat):
    print("skill_no_movement started")
    # MOVING CHARACTER closer to middle
    time.sleep(0.5)
    pydirectinput.click(1106, 298, button='right')
    time.sleep(1)
    pydirectinput.click(1106, 298, button='right')
    time.sleep(1)
    count = 0
    checklist
    # while (countx < 3):

    for i in range(0, repeat, 1):
        print(count)
        # count = imagesearch_count(checkstate + 'reward for passings.bmp')
        for g in checklist:
            # print('Current state is:')
            # print(g)
            count += imagesearch_count(g)
            # extract the name of the image that is found on the screen
            # DO THIS : based on the name of the image prob GOTO command or something
            # similar or all placed in one loop under definition of check
            # g = str
            # if str.find("DEAD") != -1
            # GOTO here
            # print(count)
        if count == 0:
            # print(count)

            randomnumber = random.randint(1, 5)  # Integer from 1 to 10, endpoints included
            randomnumber1 = random.randint(1, 6)
            randomfloat = random.uniform(0.2, 1)

            list1 = ['w', 's']
            defense = ['d', 'e']

            randomjump = ['r', 'a']
            randomATTACK = random.sample(list1, 1)
            randomDEFENSE = random.sample(defense, 1)
            # move to center
            pydirectinput.moveTo(950 + randomnumber, 533 + randomnumber1, 0.4)

            time.sleep(randomfloat)
            pydirectinput.press('a')
            time.sleep(randomfloat)
            pydirectinput.press('f')
            time.sleep(0.1)
            pydirectinput.press('f')
            time.sleep(randomfloat)
            pydirectinput.press('a')
            time.sleep(randomfloat)
            pydirectinput.press(randomDEFENSE)
            time.sleep(randomfloat)
            pydirectinput.press('a')
            time.sleep(randomfloat)
            pydirectinput.press(randomATTACK)
            pydirectinput.press('a')
            time.sleep(randomfloat)
        else:
            for g in checkIFDEAD:
                # print('Current state is:')
                # print(g)
                count += imagesearch_count(g)
                # extract the name of the image that is found on the screen
                # DO THIS : based on the name of the image prob GOTO command or something
                # similar or all placed in one loop under definition of check
                # g = str
                # if str.find("DEAD") != -1
                # GOTO here
                # print(count)
                if count == 1:
                    print('Character died reviving...')
                    REVIVECHARACTER()
                else:
                    print("STOPPING and restarting")
                    continue
                    break


def Midlescreen_Circle_rightclick():
    for i in range(0, 33, 1):
        randomnumber = random.randint(1, 5)  # Integer from 1 to 10, endpoints included
        randomnumber1 = random.randint(1, 6)
        randomfloat = random.uniform(0.2, 1)
        list1 = ['d', 'e', 'f', 's']
        randomjump = ['r', 'a']
        randomletter = random.sample(list1, 1)
        movetodelay = 0.3
        print(randomfloat)

        time.sleep(0.4 + randomfloat)
        # pyautogui.write('rrr', interval=0.25+randomfloat)
        # CIRCLE MOVEMENT WITH RIGHTCLICK + R on KEYBOARD
        pyautogui.press(randomletter)
        # time.sleep(0.25 + randomfloat)
        # mouseDown(x=None, y=None, button=PRIMARY, duration=None, tween=None, logScreenshot=None, _pause=True):
        # UP
        # pyautogui.moveTo(943 + randomnumber, 364 + randomnumber1, 0.1, pyautogui.easeOutQuad)
        pydirectinput.press(randomletter)
        pyautogui.mouseDown(button='right', x=(943 + randomnumber), y=(364 + randomnumber1))
        # pydirectinput.mouseDown(943 + randomnumber, 364 + randomnumber1, button='right', duration=1)
        pydirectinput.press('r')
        time.sleep(randomfloat)
        # LEFT
        pyautogui.moveTo(807 + randomnumber, 503 + randomnumber1, movetodelay, pyautogui.easeOutQuad)
        pydirectinput.moveTo(807 + randomnumber, 503 + randomnumber1, 0.4)
        pyautogui.press('r')
        time.sleep(0.1 + randomfloat)
        # DOWN
        pyautogui.moveTo(960 + randomnumber, 599 + randomnumber1, movetodelay, pyautogui.easeOutQuad)
        pydirectinput.moveTo(960 + randomnumber, 599 + randomnumber1, 0.2)
        pyautogui.press(randomjump)
        time.sleep(0.1 + randomfloat)
        # RIGHT
        pyautogui.moveTo(1067 + randomnumber, 495 + randomnumber1, movetodelay, pyautogui.easeOutQuad)
        pydirectinput.moveTo(1067 + randomnumber, 495 + randomnumber1, 0.2)
        pyautogui.press('r')
        # pyautogui.moveTo(100, 100, 2, pyautogui.easeInQuad)

        # pyautogui.dragTo(943+randomnumber, 364+randomnumber1, 0.2, button='right')  # drag mouse to X of 100, Y of 200 while holding down right mouse button
        # pyautogui.press('r')
        # time.sleep(0.25 + randomfloat)
        # pyautogui.press('r')
        # time.sleep(0.25 + randomfloat)
        # pyautogui.dragTo(807+randomnumber, 503+randomnumber1,0.2, button='right')
        # pyautogui.press('r')
        # time.sleep(0.25 + randomfloat)
        # pyautogui.press('r')
        # time.sleep(0.25 + randomfloat)
        # pyautogui.dragTo(960+randomnumber, 599+randomnumber1,0.2, button='right')
        # pyautogui.press('r')
        # time.sleep(0.25 + randomfloat)
        # pyautogui.press('r')
        # time.sleep(0.25 + randomfloat)
        # pyautogui.dragTo(1067+randomnumber, 495+randomnumber1,0.2, button='right')
        # pyautogui.press('r')
        # time.sleep(0.25 + randomfloat)
        # pyautogui.press('r')
        # time.sleep(0.25 + randomfloat)
        pydirectinput.mouseUp(button='right')

    # img = cv2.imread(image)
    # height, width, channels = img.shape
    # x = path.basename(image)[0]
    # pyautogui.press(''+x)


# def focus_window(NameofWindow):
#         focusthis = gw.getWindowsWithTitle(NameofWindow)[0]
#         focusthis.activate()
#         #focusthis.minimize()
#         #focusthis.restore()
def focus_window(NameofWindow):
    w = WindowMgr()
    w.find_window_wildcard(NameofWindow)
    w.set_foreground()


def DismantleBalls():
    randomnumber = random.randint(1, 5)  # Integer from 1 to 10, endpoints included
    randomnumber1 = random.randint(1, 6)
    randomfloat = random.uniform(0.2, 1)
    print(randomfloat)
    firstbottomrowX = 1500
    firstbottomrowY = 717
    randomwaittime = 0.25 + randomfloat

    step = 0
    pyautogui.press('i')

    # Click_on_Image('D:\\Lost ark serious\\Lost ark buttons\\Openthis\\Dissmantle.bmp', 'left', 2, 1)
    time.sleep(1)

    while True:
        count = (Search_image_return_count('D:\\Lost ark serious\\Lost ark buttons\\DISMANTLE\\Detect inventory.png', 0.1, 10))
        print(count)
        if count < 9:
            # open dismantle button
            time.sleep(1)
            pydirectinput.moveTo(1600, 754)
            time.sleep(1)
            pydirectinput.click(1601, 754, button='left')

            # Select all epic - > dismantle -> enter - > ok
            time.sleep(1)
            pydirectinput.click(1400, 677, button='left')
            time.sleep(1)
            # pydirectinput.click(1307, 745, button='left')
            # time.sleep(1)
            # pyautogui.press('enter')
            # time.sleep(1)
            # pydirectinput.click(1679, 660, button='left')
            # time.sleep(randomwaittime)

            for stepy in range(0, -80, -40):
                for stepx in range(0, 400, 40):
                    pydirectinput.moveTo(firstbottomrowX + stepx + randomnumber, firstbottomrowY + stepy + randomnumber1)
                    pydirectinput.click(firstbottomrowX + stepx + randomnumber, firstbottomrowY + stepy + randomnumber1,
                                        button='right')
                    # pyautogui.moveTo(firstbottomrowX + step + randomnumber, firstbottomrowY + randomnumber1, 2, pyautogui.easeInBounce)
                    # pyautogui.click(firstbottomrowX + step + randomnumber, firstbottomrowY + randomnumber1, button='right')
                    # print(step)
                    time.sleep(randomwaittime)

            time.sleep(1)
            pydirectinput.moveTo(1307, 745, )
            pydirectinput.click(1307, 745, button='left')
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(1)
            pydirectinput.moveTo(1679, 660, )
            pydirectinput.click(1679, 660, button='left')
            time.sleep(randomwaittime)

            pyautogui.press('i')

            # mouse.move(255, 355, 1)
            # time.sleep(0.25 + randomfloat)
            # mouse.click(button='left')
            # time.sleep(0.25 + randomfloat)
            # mouse.move(1600, 750)
            # time.sleep(0.1)
            # mouse.move(1599, 755)
            # time.sleep(0.1)
            # mouse.move(1597, 762)
            # time.sleep(0.25 + randomfloat)
            # mouse.click(button='left')

            # Move pointer relative to current position
            # mouse.position = (244, 443)
            # time.sleep(0.25 + randomfloat)
            # mouse.position = (1600, 750)
            # time.sleep(0.25 + randomfloat)
            # mouse.click(Button.left, 2)

            # pyautogui.write('rrr', interval=0.25+randomfloat)
            # CIRCLE MOVEMENT WITH RIGHTCLICK + R on KEYBOARD
            time.sleep(0.25 + randomfloat)

            time.sleep(0.25 + randomfloat)

            # pyautogui.dragTo(1857, 672,1)
            break
        else:
            print('Did not find Dismantle window.bmp. Closing inventory')
            pyautogui.press('i')
            time.sleep(0.25 + randomfloat)
    print("Finished Dismantle")
    return count


def Grabimage_text():
    im = ImageGrab.grab(bbox=(710, 845, 779, 857))
    # im.show()
    im.save('hp_image.jpg')
    # img = Image.open('hp_image.jpg').convert('LA')
    # img.save('greyscale.png')
    imageObject = 'hp_image.jpg'
    im = Image.open('hp_image.jpg')

    # invert image colors [if numbers are white]!!
    im_invert = ImageOps.invert(im)
    im_invert.save('original-image-1.png');

    time.sleep(1)
    img = Image.open('original-image-1.png')
    text = pytesseract.image_to_string(img)

    print(text)


######
EpicPath = "E:\\Lost ark serious\\Lost ark buttons\\"

txtfiles = []
for file in glob.glob("*.bmp"):
    txtfiles.append(file)

###PAY ATTENTION TO EXTENSION
# Coordinates on square on screen
TOPLMIDLE = (880, 350)
BOTRMIDLE = (1080, 800)

# Global stuff
checkthis = EpicPath + 'Check'
movement = EpicPath + 'Movement'

checklist = [f for f in glob.glob(checkthis + "**/*.bmp")]
movementlist = [m for m in glob.glob(movement + "**/*.jpg")]

# Yozmund
checkDEAD = EpicPath + 'dead'
checkENTER = EpicPath + 'ENTER'
checkDISMANTLE = EpicPath + 'DISMANTLE'

checkIFDEAD = [m for m in glob.glob(checkDEAD + "**/*.bmp")]
checkIFENTER = [z for z in glob.glob(checkENTER + "**/*.bmp")]
checkIFDISMANTLE = [e for e in glob.glob(checkDISMANTLE + "**/*.bmp")]

# Labels
GlobalLabel = ''

# Fishing
CheckFISHING = EpicPath + 'FISHING'
FishingBUFFS = EpicPath + 'FISHING\\BUFFS'
FishingCATCH = EpicPath + 'FISHING\\EXCLAMATION'
FishingSTART = EpicPath + 'FISHING\\STARTFishing'
FishingNETGAME = EpicPath + 'FISHING\\NETGAME'

CheckIFFISHING = [x for x in glob.glob(CheckFISHING + "**/*.bmp")]
FINDFishingCATCH = [x for x in glob.glob(FishingCATCH + "**/*.png")]
FINDFishingSTART = [x for x in glob.glob(FishingSTART + "**/*.png")]
FINDFishingNETGAME = [x for x in glob.glob(FishingNETGAME + "**/*.png")]

###PAY ATTENTION TO EXTENSION

# print(checklist)

# x = pyautogui.click(935, 473, button='right')
# y = pyautogui.click(934, 561, button='right')
# z = pyautogui.click(1000, 530, button='right')
# c = pyautogui.click(870, 519, button='right')
# test_list = [1, 2, 3, 4]
# random_num = random.choice(test_list)
# if random_num == 1:
#     z

count = 0
restart = 0
#
# while (count < 9):
#     for m in checkIFDEAD:
#         # focus_window('LOST ARK')
#         restart += 1
#         print("program finished loop for " + str(restart) + "th time")
#         for f in checklist:
#             focus_window('LOST ARK')
#             # pyautogui.dragTo(1280, 436,0.6, button='left')
#             # focus_window('LOST ARK')
#             # print('finished')
#             # imagesearch_numLoop(f, 0.5, 2, 0.9)
#             StateCHECKimg(1)
#             # ENTERstage()
#             # Fishing()
#             # Click_on_Image(f, 'left', 2, 1)
#         # Midlescreen_Circle_rightclick()
#         # Skills_no_movement(23)
#         # DismantleBalls()
#         # DO NOT FORGET TO DEBUG CHANGING KEYBOARD TO RUSSIAN FUKS the program
#         # Grabimage_text()
#         # pos = imagesearch_numLoop(m, 0.1, 1, 0.9)
#         # #print(m)r
#         # #print(path.basename(f)[0])
#         # if pos[0] != -1:
#         #      pyautogui.press('g')
#         #     #
#         #     # PressKey_image(f)
#         #     # pyautogui.press('f1'
