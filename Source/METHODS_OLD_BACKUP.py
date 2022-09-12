import cv2
import numpy as np
import pyautogui
import pydirectinput
import random
import time
from numpy import asarray
from os import path
import threading
import os
import sys
import glob
import keyboard
import mss
import mss.tools
import win32gui
import re

# from skimage import io
from multiprocessing import Manager, Process, Pool
from multiprocessing.managers import NamespaceProxy, BaseManager
import inspect  # part of multiprocessing stuff

from pytesseract import pytesseract
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract

sys.path.insert(0, 'E:\Hello wolrd Python\LOSTARKB')

Resolution = [2560, 1080]
MiniMCOORD = [Resolution[0] / 100 * 86,
              Resolution[1] / 100 * 4.17,
              Resolution[0] / 100 * 98.7,
              Resolution[1] / 100 * 30.28]

Elites = 0
Enemies = 0
Bosses = 0
Portals = 0
Towers = 0
# # Defining process lists
# if __name__ == '__main__':
#     listmanager = Manager()
#     normal_processes = listmanager.list()
#     combat_processes = listmanager.list()
#     all_processes = listmanager.list()


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

    return pyautogui.screenshot(region=(x1, y1, width, height), imageFilename="Regiongrabber.jpeg")


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
    # im = pyautogui.screenshot()
    with mss.mss() as sct:

        # The screen part to capture
        region = {'left': 0, 'top': 0, 'width': Resolution[0], 'height': Resolution[1]}

        # Grab the data
        image_screenshot = mss.mss().grab(region)

        # Save to the picture file
        mss.tools.to_png(image_screenshot.rgb, image_screenshot.size, output='Screenshot_imagesearch.png')

    im = cv2.imread('Screenshot_imagesearch.png')
    # im.save('testarea' + '.png') # usefull for debugging purposes, this will save the captured region as "testarea.png"
    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # avg_x = (min_loc[0] + max_loc[0]) / 2
    # avg_y = (min_loc[1] + max_loc[1]) / 2
    #
    # center_of_image = [max_loc[0], max_loc[1]]
    if max_val < precision:
        return [-1, -1]
    # return max_loc
    return max_loc


def imagesearch_fast_area(image, x1=0, y1=0, x2=Resolution[0], y2=Resolution[1], precision=0.8):
    # im = pyautogui.screenshot("Screenshot.png", region=(x1, y1, x2, y2))
    with mss.mss() as sct:

        # The screen part to capture
        region = {'left': x1, 'top': y1, 'width': x2, 'height': y2}

        # Grab the data
        image_screenshot = mss.mss().grab(region)

        # Save to the picture file
        mss.tools.to_png(image_screenshot.rgb, image_screenshot.size, output='Screenshot_imagesearch_fast_area.png')

    im = cv2.imread('Screenshot_imagesearch_fast_area.png')
    # im.save('testarea' + '.png') # usefull for debugging purposes, this will save the captured region as "testarea.png"
    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # avg_x = (min_loc[0] + max_loc[0]) / 2
    # avg_y = (min_loc[1] + max_loc[1]) / 2
    #
    # center_of_image = [max_loc[0], max_loc[1]]
    if max_val < precision:
        return [-1, -1]
    # return max_loc
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
        print(image + " not found, waiting")
        time.sleep(timesample)
        pos = imagesearch(image, precision)
        print(pos)
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
        print(image + " not found, waiting")
        time.sleep(timesample)
        pos = imagesearch(image, precision)
        count = count + 1
        if count > maxSamples:
            break
    return pos


def Searchimage_return_position(image, maxSamples=1, precision=0.8):
    pos = imagesearch(image, precision)
    count = 0
    while pos == [-1, -1]:
        splitstring = image.rsplit('\\')[2]
        # print(splitstring)
        # print(image + " not found, waiting")
        pos = imagesearch(image, precision)
        count = count + 1
        if count > maxSamples:
            break
    return pos


# Same as above just returns count
def Search_image_return_count(image, timesample=0.5, maxSamples=5, precision=0.8):
    pos = imagesearch(image, precision)
    count = 0
    while pos[0] == -1:
        print(image + " not found, waiting ")
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
                      2)  # // Uncomment to draw boxes around found occurances
        count = count + 1
        cv2.imwrite('RESULT' + image + '.png',
                    img_rgb)  # // Uncomment to write output image with boxes drawn around occurances

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val < precision:
        return [-1, -1]
    return max_loc


def searchimageinarea(image, filename, look_for="None", x1=0, y1=0, x2=Resolution[0], y2=Resolution[1],
                      count=False, precision=0.7, im=None):
    countx = 0
    name = filename + ".png"
    with mss.mss() as sct:
        # The screen part to capture
        region = {'left': x1, 'top': y1, 'width': x2, 'height': y2}
        # Grab the data
        image_screenshot = mss.mss().grab(region)
        # Save to the picture file
        mss.tools.to_png(image_screenshot.rgb, image_screenshot.size, output=('Screenshot' + filename))

    #  VERY IMPORTANT so that multiple process don't conflict on same file name
    # NEW SOLUTION DELETE IF IT DOESNT WORK  = , cv2.IMREAD_UNCHANGED)
    img_rgb = cv2.imread('Screenshot' + filename, cv2.IMREAD_UNCHANGED)

    # ERRORS READING FILES NEED TO FIX!!!!
    if img_rgb is None:
        print(img_rgb, "ERROR reading image")
    else:
        # print("FOUND IMAGE its not none", image)
        try:
            os.remove(name)
        except IOError:
            123
            # print("ERROR!")
        # img_rgb = np.array(img_rgb)

        hsv = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2HSV)
        # FILTERING COLORS for specific usage BGR 2 HSV
        red_mask = cv2.inRange(hsv, (0, 200, 90), (255, 255, 255))  # OLD_value (110, 150, 90)
        elites_mask = cv2.inRange(hsv, (100, 120, 110), (255, 255, 255))
        boss_mask = cv2.inRange(hsv, (0, 0, 25), (255, 255, 255))
        tower_mask = cv2.inRange(hsv, (0, 0, 25), (255, 255, 255))
        portal_mask = cv2.inRange(hsv, (0, 110, 50), (255, 255, 255))
        hpbar_mask = cv2.inRange(hsv, (0, 200, 180), (255, 255, 255))
        imask = 0
        # slice the mask
        if look_for == 'Red':
            imask = red_mask > 0
        if look_for == 'Elite':
            imask = elites_mask > 0
        if look_for == 'Boss':
            imask = boss_mask > 0
        if look_for == 'Tower':
            imask = tower_mask > 0
        if look_for == 'Portal':
            imask = portal_mask > 0
        if look_for == 'HPbar':
            imask = hpbar_mask > 0
        color = np.zeros_like(img_rgb, np.uint8)
        color[imask] = img_rgb[imask]
        # # save
        cv2.imwrite("0 Testing mask.png", color)
        # Convert/DELETE BLACK PIXELS(BACKGROUND)\
        # if nobackg != 0:
        #     src = cv2.imread(saveas, 1)
        #     tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        #     _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
        #     b, g, r = cv2.split(src)
        #     rgba = [b, g, r, alpha]
        #     dst = cv2.merge(rgba, 4)
        #     cv2.imwrite(saveas, dst)
        if look_for == "None":
            print("without mask mask")
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        else:
            # print("doing ", look_for, "MASK")
            img_gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)

        template = cv2.imread(image, 0)
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= precision)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # My own implementation of CENTER OF IMAGE found
        top_left = max_loc  # can change to min_loc or max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        avg_x = (bottom_right[0] + top_left[0]) / 2
        avg_y = (bottom_right[1] + top_left[1]) / 2
        average = [x1 + avg_x, y1 + avg_y]
        # print("AVERAGE ", average)

        path = 'C:\\Users\\Ggjustice\\Pictures\\Buttons\\Testing\\HPbars\\'
        path1 = 'C:\\Users\\Ggjustice\\Pictures\\Buttons\\Testing\\'
        raw_path = 'C:\\Users\\Ggjustice\\Pictures\\Buttons\\Testing\\No filter\\'

        cv2.imwrite(raw_path + "MASK" + name, img_gray)  # uncomment FOR MASKS
        cv2.imwrite(raw_path + name, img_rgb)  # Uncomment to write output image with boxes drawn around occurances

        for pt in zip(*loc[::-1]):  # Swap columns and rows
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255),
                          2)  # Uncomment to draw boxes around found occurances
        if max_val < precision:
            return [-1, -1]
        # Saves pictures For testing purposes only if meets precision requirment
        else:
            if "HPBAR" in name:
                # print("drawing boxes", name)
                cv2.imwrite(path + "\\Mask" + name, img_gray)
                cv2.imwrite(path + name, img_rgb)
                average = [x1 + avg_x, y1 + avg_y]
                my_list = list(max_loc)
                my_list[0] = my_list[0] + x1
                my_list[1] = my_list[1] + y1
                max_loc = tuple(my_list)
            else:
                # print("drawing boxes", name)
                cv2.imwrite(path1 + "\\Mask" + name, img_gray)
                cv2.imwrite(path1 + name, img_rgb)
        # print("Min and max LOC",min_loc, max_loc)
        return average
        # return max_loc


def ImageCropSEARCH(image, x1, y1, x2, y2, timesample, precision=0.8):
    pos = searchimageinarea(image, x1, y1, x2, y2, precision)

    while pos[0] == -1:
        time.sleep(timesample)
        pos = searchimageinarea(image, x1, y1, x2, y2, precision)
    return pos


def search_click_image(image, action, x1=0, y1=0, x2=Resolution[0], y2=Resolution[1], timestamp=0.1,
                       offset=5, precision=0.7, click_all="no"):
    # Searching for image x1 y1 x2 y1 are area in which it searches
    img_rgb = pyautogui.screenshot("Screenshot.png", region=(x1, y1, x2 - x1, y2 - y1))

    img_rgb = np.array(img_rgb)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= precision)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val < precision:
        pos = [-1, -1]
        return pos
    else:
        pos = max_loc
    if click_all == "yes":
        for pt in zip(*loc[::-1]):  # Swap columns and rows
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)  # drawing rectangles
            cv2.imwrite("0 RECTANGLES.png", img_rgb)
            img = cv2.imread(image)
            height, width, channels = img.shape
            pyautogui.moveTo(pt[0] + r(width / 2, offset) + x1,
                             pt[1] + r(height / 2, offset) + y1,
                             timestamp)
            pyautogui.click(button=action)
            time.sleep(0.4)
    else:
        # clicking on image
        img = cv2.imread(image)
        height, width, channels = img.shape
        # Added +x1 and +y1 IF YOU GET ERROR remove?
        pyautogui.moveTo(pos[0] + r(width / 2, offset) + x1,
                         pos[1] + r(height / 2, offset) + y1,
                         timestamp)
        pyautogui.click(button=action)
        return pos


def r(num, rand):
    return num + rand * random.random()


def PressKey_image(image):
    img = cv2.imread(image)
    height, width, channels = img.shape
    x = path.basename(image)[0]
    pyautogui.press('' + x)


def processing_task(function, normal_processes, combat_processes, all_processes,
                    arguments=None, append="ALL"):
    # n_processes = normal_processes
    # c_processes = combat_processes
    # a_processes = all_processes
    #
    # # global n_processes
    # # global c_processes
    # # global a_processes

    BaseManager.register('Process', Process, ProcessProxy, exposed=tuple(dir(ProcessProxy)))
    manager = BaseManager()
    manager.start()
    if arguments is None:
        start_function = manager.Process(target=function)
    else:
        start_function = manager.Process(target=function, args=arguments)

    # APPENDING
    if append == "ALL":
        all_processes.append(start_function)
        print(all_processes)
    elif append == "normal":
        normal_processes.append(start_function)
    elif append == "combat":
        combat_processes.append(start_function)

    start_function.start()
    # keyboard.add_hotkey('ctrl+shift+q', kill_all)
    print(normal_processes, combat_processes, all_processes)
    n_processes = normal_processes
    c_processes = combat_processes
    a_processes = all_processes
    return n_processes, c_processes, a_processes


def kill_all(a_processes):
    print("KILLING ALL")
    time.sleep(1)
    print("ATTEMPTING TO KILL : ", a_processes)
    for process in a_processes:
        # print(process)
        process.terminate()
        process.kill()
        process.join()
    exit()
    os._exit(0)

# keyboard.add_hotkey('ctrl+shift+q', kill_all)

class ObjProxy(NamespaceProxy):
    """Returns a proxy instance for any user defined data-type. The proxy instance will have the namespace and
    functions of the data-type (except private/protected callables/attributes). Furthermore, the proxy will be
    pickable and can its state can be shared among different processes. """

    @classmethod
    def populate_obj_attributes(cls, real_cls):
        DISALLOWED = set(dir(cls))
        ALLOWED = ['__sizeof__', '__eq__', '__ne__', '__le__', '__repr__', '__dict__', '__lt__',
                   '__gt__']
        DISALLOWED.add('__class__')
        new_dict = {}
        for (attr, value) in inspect.getmembers(real_cls, callable):
            if attr not in DISALLOWED or attr in ALLOWED:
                new_dict[attr] = cls._proxy_wrap(attr)
        return new_dict

    @staticmethod
    def _proxy_wrap(attr):
        """ This method creates function that calls the proxified object's method."""

        def f(self, *args, **kwargs):
            return self._callmethod(attr, args, kwargs)

        return f


attributes = ObjProxy.populate_obj_attributes(Process)
ProcessProxy = type("ProcessProxy", (ObjProxy,), attributes)


def image2text(x1=0, y1=0, x2=Resolution[0], y2=Resolution[1], method=' --oem 3 --psm 7'):
    count = 0
    # BaseCoord = imagesearcharea( 1182, 324, 1357, 381, precision=0.95)
    # image_screenshot = pyautogui.screenshot("Screenshot.png", region=(x1, y1, x2, y2))
    with mss.mss() as sct:

        # The screen part to capture
        region = {'left': x1, 'top': y1, 'width': x2, 'height': y2}

        # Grab the data
        image_screenshot = mss.mss().grab(region)

        # Save to the picture file
        mss.tools.to_png(image_screenshot.rgb, image_screenshot.size, output='Screenshot.png')

    image = cv2.imread('Screenshot.png')

    # get grayscale image
    def get_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # thresholding
    def thresholding(image):
        return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 19, 3)

    def get_weird(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    gray = get_grayscale(image)
    thresh = thresholding(gray)
    weird = get_weird(image)
    images = [image, gray, thresh,weird]
    titles = ['Original Image', 'gray',
              'thresh', 'weird']

    # # displaying image on screen for debuging
    # from matplotlib import pyplot as plt
    # for i in range(4):
    #     plt.subplot(2, 2, i + 1), plt.imshow(images[i], 'gray')
    #     plt.title(titles[i])
    #     plt.xticks([]), plt.yticks([])
    # plt.show()

    # image_screenshot.save('ItemName' + str(count) + '.png')
    text = pytesseract.image_to_string(image, config=method)  # change parameters in default
    # print(text)
    return text


class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)


def focus_window(NameofWindow):
    print("FOCUS SWITCH to ", NameofWindow)
    w = WindowMgr()
    w.find_window_wildcard(NameofWindow)
    w.set_foreground()
