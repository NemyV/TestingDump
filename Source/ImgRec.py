


import sys
sys.path.insert(0, 'E:\Hello wolrd Python\LOSTARKB')

import glob
from os import path
import os
import cv2
import numpy as np
import pyautogui
import pydirectinput
import random
import time
from numpy import asarray


# Win32 Imports
import win32gui
import win32api
import win32con as wcon

# Connect to the Application
from pywinauto import Application

# importing for processdetails()
from ProcessName import findProcessIdByName
from ProcessName import checkIfProcessRunning

Lookfor = 'steam.exe'


# Import WINDOWS class
from window import Window

# USER SETTINGS
import usersettings as userset

# Initilize Window Class
Window.init()

def click(x: int, y: int, button: str = "left", fast: bool = False) -> None:
    """Click at pixel xy."""
    # print(Window.init())
    # Window.init()
    x += Window.x
    y += Window.y
    lParam = win32api.MAKELONG(x, y)
    # MOUSEMOVE event is required for game to register clicks correctly
    win32gui.PostMessage(Window.id, wcon.WM_MOUSEMOVE, 0, lParam)
    while (win32api.GetKeyState(wcon.VK_CONTROL) < 0 or
           win32api.GetKeyState(wcon.VK_SHIFT) < 0 or
           win32api.GetKeyState(wcon.VK_MENU) < 0):
        time.sleep(0.005)
    # CALL IF TESTING OR BUGGS
    #print('i was in click id is:')
    #print(Window.id)
    if button == "left":
        win32gui.PostMessage(Window.id, wcon.WM_LBUTTONDOWN,
                             wcon.MK_LBUTTON, lParam)
        win32gui.PostMessage(Window.id, wcon.WM_LBUTTONUP,
                             wcon.MK_LBUTTON, lParam)
    else:
        win32gui.PostMessage(Window.id, wcon.WM_RBUTTONDOWN,
                             wcon.MK_RBUTTON, lParam)
        win32gui.PostMessage(Window.id, wcon.WM_RBUTTONUP,
                             wcon.MK_RBUTTON, lParam)
    # Sleep lower than 0.1 might cause issues when clicking in succession
    if fast:
        time.sleep(userset.FAST_SLEEP)
    else:
        time.sleep(userset.MEDIUM_SLEEP)

def processdetails(processname):
    if checkIfProcessRunning(processname):
        print('Yes a ' + processname + ' process was running')
    else:
        print('No ' + processname + ' process was not running')
    print("*** Find PIDs of a running process by Name ***")

    listOfProcessIds = findProcessIdByName(processname)
    if len(listOfProcessIds) > 0:
        print('Process Exists | PID and other details are')
        for elem in listOfProcessIds:
            PID = processID = elem['pid']
            processName = elem['name']
            processCreationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(elem['create_time']))
            print(PID, processName, processCreationTime)
            return PID, processName, processCreationTime


app = Application(backend="win32").connect(process=processdetails(Lookfor)[0])
form = app.window(title_re="LOST ARK")

def r(num, rand):
    return num + rand * random.random()


'''
grabs a region (topx, topy, bottomx, bottomy)
to the tuple (topx, topy, width, height)
input : a tuple containing the 4 coordinates of the region to capture
output : a PIL image of the area selected.
'''


def region_grabber(region):
    x1 = region[0]
    y1 = region[1]
    width = region[2]
    height = region[3]

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


def imagesearcharea(image, x1, y1, x2, y2, precision=0.9, im=None):
    if im is None:
        im = region_grabber(region=(x1, y1, x2, y2))
        im.save('1 Testarea.png')#usefull for debugging purposes, this will save the captured region as "testarea.png"

    #Change Color
    #img_rgb = np.array(im)
    img_rgb = cv2.imread('1 Testarea.png')

    #img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2HSV)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    template = cv2.imread(image, 0)
    #template = np.array(image)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCORR_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # print("values before min max")
    # print(x1, y1, x2, y2)

    # print("values inside imagesearcharea: ")
    # print(min_val, max_val, min_loc, max_loc)
    #This transforms back x and y To actual position on the screen rather than inside region
    x = max_loc[0] + x1
    y = max_loc[1] + y1
    #print(x,y)
    max_loc = [x, y]
    # print(max_loc)
    #For testing purposes
    w, h = template.shape[::-1]
    loc = np.where(res >= precision)
    count = 0

    for pt in zip(*loc[::-1]):  # Swap columns and rows
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255),2)  # Uncomment to draw boxes around found occurances
        count = count + 1
        cv2.imwrite('AreaResult.png', img_rgb)  # Uncomment to write output image with boxes drawn around occurances
    #test
    print("Found : ", count, " MATCHES")

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
    form.send_keystrokes('')
    win32api.SetCursorPos((pos[0] + r(width / 2, offset), pos[1] + r(height / 2, offset), timestamp))
    click((pos[0] + r(width / 2, offset), pos[1] + r(height / 2, offset), timestamp), button=action)


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
    im.save('imagesearch.png') #usefull for debugging purposes, this will save the captured region as "testarea.png"
    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # For testing purposes
    w, h = template.shape[::-1]
    loc = np.where(res >= precision)
    count = 0
    for pt in zip(*loc[::-1]):  # Swap columns and rows
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255),2)  # Uncomment to draw boxes around found occurances
        count = count + 1
        cv2.imwrite('imagesearch.png', img_rgb)  # Uncomment to write output image with boxes drawn around occurances
    #####################
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
        GlobalLabel = (image + " not found, waiting")
        time.sleep(timesample)
        pos = imagesearch(image, precision)
        GlobalLabel = (pos)
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
        GlobalLabel = (image + " not found, waiting")
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
        GlobalLabel = (image + " not found, waiting")
        time.sleep(timesample)
        pos = imagesearch(image, precision)
        count = count + 1
        if count > maxSamples:
            break
    return pos


# Same as above just returns count
def Search_image_return_count(image, timesample, maxSamples, precision=0.75):
    pos = imagesearch(image, precision)
    count = 0
    while pos[0] == -1:
        print(image + " not found, current count : "+str(count))
        # print("not found after :")
        # print(count)
        time.sleep(timesample)
        pos = imagesearch(image, precision)
        count = count + 1
        if count > maxSamples:
            break
    else:
        print(image + " found after this many samples:" + str(count))
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
        # print("still searcing in region")
        # #print(image)
        # print(x1,y1,x2,y2)
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
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255),
                      2)  # Uncomment to draw boxes around found occurances
        count = count + 1
        cv2.imwrite('result.png', img_rgb)  # Uncomment to write output image with boxes drawn around occurances
    return count


def searchimageinarea(image, x1, y1, x2, y2, precision=0.8, im=None):
    if im is None:
        im = region_grabber(region=(x1, y1, x2, y2))
        #im = ImageGrab.grab(bbox =(x1, y1, x2, y2))
        im.save('testarea.png') #usefull for debugging purposes, this will save the captured region as "testarea.png"
    img_rgb = pyautogui.screenshot()
    # this is cropped screenshot
    # GlobalLabel = (x1)
    # GlobalLabel = (y1)
    # GlobalLabel = (x2)
    # GlobalLabel = (y2)
    img_rgb.crop((x1, y1, x1+x2, y1+y2)).save('MIDDLEsearch.png')

    crop_img = img_rgb
    crop_img = asarray(crop_img)
    img_gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    template = cv2.imread(image, 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # For testing purposes
    w, h = template.shape[::-1]
    loc = np.where(res >= precision)
    count = 0
    for pt in zip(*loc[::-1]):  # Swap columns and rows
        img_rgb = np.array(im)
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255),2)  # Uncomment to draw boxes around found occurances
        count = count + 1
        cv2.imwrite('AreaResult.png', img_rgb)  # Uncomment to write output image with boxes drawn around occurances

    if max_val < precision:
        return [-1, -1]
    return max_loc


def ImageCropSEARCH(image, x1, y1, x2, y2, timesample, precision=0.8):
    pos = searchimageinarea(image, x1, y1, x2, y2, precision)

    while pos[0] == -1:
        time.sleep(timesample)
        pos = searchimageinarea(image, x1, y1, x2, y2, precision)
    return pos


def PressKey_image(image):
    img = cv2.imread(image)
    height, width, channels = img.shape
    x = path.basename(image)[0]
    pyautogui.press('' + x)


def Click_on_Image(image, action='left', repeat=1, offset=5):
    print("click on image started")
    print(image)
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
        # if pos != [-1, -1]:
        #     form.send_keystrokes('')
        #     win32api.SetCursorPos((int(pos[0] + r(width / 2, offset)), int(pos[1] + r(height / 2, offset))))

        # action ( (button='left')
        x, y = pyautogui.position()
        if x > 100:
            print(string)
            form.send_keystrokes('')
            win32api.SetCursorPos((int(pos[0] + r(width / 2, offset)), int(pos[1] + r(height / 2, offset))))
            click(x, y, button=action)
        else:
            GlobalLabel = ('this is height of x:')
            GlobalLabel = (height)
    # GlobalLabel = (count)
    # return count

def Click_on_Image_inside_region(image,x1, y1, x2, y2, action='left', repeat=1, offset=5):
    print("click on image started")
    print(image)
    count = 0
    randomnumber = random.randint(1, 5)  # Integer from 1 to 10, endpoints included
    randomnumber1 = random.randint(1, 6)
    randomfloat = random.uniform(0.2, 1)
    for i in range(0, repeat, 1):
        # count += 1
        string = 'Clicking on: ' + image
        img = cv2.imread(image)
        # Get position of "image" [imagesearch_loop(image, timesample, precision=0.8):] !!!!!!!!!!!!!!!!!!!
        #pos = imagesearch_numLoop(image, 0.5, 2)
        pos = imagesearcharea(image, x1, y1, x2, y2)
        print("inside clickon area")
        print(pos)

        height, width, channels = img.shape
        time.sleep(randomfloat)
        #REVERT BACK IF BUGS in CLICK
        # if pos != [-1, -1]:
        #     form.send_keystrokes('')
        #     win32api.SetCursorPos((int(pos[0] + r(width / 2, offset)), int(pos[1] + r(height / 2, offset))))

        # action ( (button='left')
        x, y = pyautogui.position()
        if x > 100:
            print(string)
            print(x,y)
            form.send_keystrokes('')
            win32api.SetCursorPos((int(pos[0] + r(width / 2, offset)), int(pos[1] + r(height / 2, offset))))
            click(x, y, button=action)
        else:
            GlobalLabel = ('this is height of x:')
            GlobalLabel = (height)
    # GlobalLabel = (count)
    # return count

def FindImageArea(image, x1, y1, x2, y2, precision=0.8, im=None):
    if im is None:
        im = region_grabber(region=(x1, y1, x2, y2))
        im.save('testarea.png') #usefull for debugging purposes, this will save the captured region as "testarea.png"

    #Manipulating String
    file_name = os.path.basename(image)
    index_of_dot = file_name.index('.')
    file_name_without_extension = file_name[:index_of_dot]
    #print(file_name_without_extension)

    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print("values before min max")
    print(x1, y1, x2, y2)

    print("values inside imagesearcharea: ")
    print(min_val, max_val, min_loc, max_loc)
    #This transforms back x and y To actual position on the screen rather than inside region
    x = max_loc[0] + x1
    y = max_loc[1] + y1
    #print(x,y)
    max_loc = [x, y]
    print(max_loc)

    #For testing purposes
    w, h = template.shape[::-1]
    loc = np.where(res >= precision)
    count = 0
    for pt in zip(*loc[::-1]):  # Swap columns and rows
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255),2)  # Uncomment to draw boxes around found occurances
        count = count + 1
        cv2.imwrite('AreaResult.png', img_rgb)  # Uncomment to write output image with boxes drawn around occurances

    if max_val < precision:
        return [-1, -1]
    return file_name_without_extension


def movemouseto(pos , delay=0.5):
    time.sleep(delay)
    form.send_keystrokes('')
    win32api.SetCursorPos((pos))
    time.sleep(delay)

def imginsideimg(image,image2, x1, y1, precision=0.8, im=None, test=0):
    #Look for image inside image2
    # if im is None:
    #     im = region_grabber(region=(x1, y1, x2, y2))
    #     im.save('testarea.png') #usefull for debugging purposes, this will save the captured region as "testarea.png"

    im = cv2.imread(image2, 1)
    img_rgb = np.array(im)
    #img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2HSV)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    #Remove if errors
    #img_gray = cv2.GaussianBlur(img_gray, (5, 5), 0)
    #################
    template = cv2.imread(image, 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if test !=0:
        cv2.imshow("Image", img_gray)
        cv2.waitKey(0)
        cv2.imshow("Image", template)
        cv2.waitKey(0)
        print("values before min max")
        print(x1, y1)
        print("values inside imginsideimg: ")
        print(min_val, max_val, min_loc, max_loc)
        print(max_loc)

    #This transforms back x and y To actual position on the screen rather than inside region
    x = max_loc[0] + x1
    y = max_loc[1] + y1
    #print(x,y)
    max_loc = [x, y]

    #For testing purposes
    w, h = template.shape[::-1]
    loc = np.where(res >= precision)
    count = 0
    for pt in zip(*loc[::-1]):  # Swap columns and rows
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255),2)  # Uncomment to draw boxes around found occurances
        count = count + 1
        cv2.imwrite('AreaResult.png', img_rgb)  # Uncomment to write output image with boxes drawn around occurances

    if max_val < precision:
        return [-1, -1]
    return max_loc
