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


def r(num, rand):
    return num + rand * random.random()


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


def im_screenshot(filename='no_file_name', x1=0, y1=0, x2=Resolution[0], y2=Resolution[1]):
    with mss.mss() as sct:
        # The screen part to capture
        region = {'left': x1, 'top': y1, 'width': x2, 'height': y2}
        # Grab the data
        image_screenshot = mss.mss().grab(region)
        # try to remove
        try:
            os.remove('Temp_files\\Screenshot[' + filename + ']')
            time.sleep(0.5)
        except IOError:
            123
        # Save to the picture file
        mss.tools.to_png(image_screenshot.rgb, image_screenshot.size,
                         output=('Temp_files\\Screenshot[' + filename + '].png'))
    #  VERY IMPORTANT so that multiple process don't conflict on same file name
    # NEW SOLUTION DELETE IF IT DOESNT WORK  = , cv2.IMREAD_UNCHANGED)
    img_rgb = cv2.imread('Temp_files\\Screenshot[' + filename + ']', cv2.IMREAD_UNCHANGED)
    return img_rgb

'''
Searchs for an image on the screen
im : a PIL image, usefull if you intend to search the same unchanging region for several elements
returns:
top left corner coordinates of the element if found as an array [x,y] or [-1,-1] if not
'''


def im_search(image, return_value="center", precision=0.8):
    file_name = "im_search"
    img_rgb = im_screenshot(file_name)
    number_of_channels, w, h = img_rgb.shape[::-1]
    x1 = w
    y1 = h
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)

    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val < precision:
        return [-1, -1]
    if return_value == "top_left":
        return max_loc
    if return_value == "center":
        top_left = max_loc  # can change to min_loc or max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        avg_x = (bottom_right[0] + top_left[0]) / 2
        avg_y = (bottom_right[1] + top_left[1]) / 2
        average = [x1 + avg_x, y1 + avg_y]
        return average


# im_search_area_fast
def imagesearch_fast_area(image, x1=0, y1=0, x2=Resolution[0], y2=Resolution[1], precision=0.8):
    file_name = "imagesearch_fast_area"
    img_rgb = im_screenshot(file_name, x1, y1, x2, y2)

    img_rgb = np.array(img_rgb)
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
Searchs for an image on screen continuously until it's found or max number of samples reached.
returns : the top left corner coordinates of the element if found as an array [x,y]
'''
def imagesearch_numLoop(image, timesample, maxSamples, precision=0.8):
    pos = im_search(image, precision)
    count = 0
    while pos[0] == -1:
        print(image + " not found, waiting")
        time.sleep(timesample)
        pos = im_search(image, precision)
        count = count + 1
        if count > maxSamples:
            break
    return pos



'''
Searches for an image on the screen and counts the number of occurrences.
'''
# imagesearch_count
def im_search_count(image, precision=0.9):
    # Take screenshot
    img_rgb = im_screenshot("imagesearch_count")
    # img_rgb = pyautogui.screenshot()
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
        return [-1, -1] , count
    return max_loc, count


def im_search_until_found(image, time_sample=0.5, max_samples=5, return_value="center", precision=0.8):
    pos = im_search(image, return_value, precision)
    count = 0
    while pos[0] == -1:
        # print(image + " not found, waiting ")
        time.sleep(time_sample)
        pos = im_search(image, return_value, precision)
        count = count + 1
        if count > max_samples:
            break
    if return_value == "count":
        return count
    else:
        return pos


def im_processing(template_image, file_name, look_for,
                  x1, y1, rgb_screenshot, return_value="center", precision=0.7):
    img_rgb = rgb_screenshot
    if look_for == "None":
        print("without mask mask")
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    else:
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
        # cv2.imwrite("0 Testing mask.png", color)

        img_gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)

    template = cv2.imread(template_image, 0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= precision)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    for pt in zip(*loc[::-1]):  # Swap columns and rows
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255),
                      2)  # Uncomment to draw boxes around found occurances

    if max_val < precision:
        return [-1, -1]
    else:

        if return_value == "center":
            # My own implementation of CENTER OF IMAGE found
            top_left = max_loc  # can change to min_loc or max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            avg_x = (bottom_right[0] + top_left[0]) / 2
            avg_y = (bottom_right[1] + top_left[1]) / 2
            average = [x1 + avg_x, y1 + avg_y]

            path = 'C:\\Users\\Ggjustice\\Pictures\\Buttons\\Testing\\HPbars\\'
            path2 = 'C:\\Users\\Ggjustice\\Pictures\\Buttons\\Testing\\Towers\\'
            path1 = 'C:\\Users\\Ggjustice\\Pictures\\Buttons\\Testing\\'
            raw_path = 'C:\\Users\\Ggjustice\\Pictures\\Buttons\\Testing\\No filter\\'
            cv2.imwrite(raw_path + "MASK" + file_name, img_gray)  # uncomment FOR MASKS
            cv2.imwrite(raw_path + file_name,img_rgb)  # Uncomment to write output image with boxes drawn around occurances
            if "Tower" in file_name:
                # print("drawing boxes", name)
                cv2.imwrite(path2 + "\\Mask" + file_name, img_gray)
                cv2.imwrite(path2 + file_name, img_rgb)
                average = [x1 + avg_x, y1 + avg_y]
                my_list = list(max_loc)
                my_list[0] = my_list[0] + x1
                my_list[1] = my_list[1] + y1
                max_loc = tuple(my_list)
            if "HPBAR" in file_name:
                # print("drawing boxes", name)
                cv2.imwrite(path + "\\Mask" + file_name, img_gray)
                cv2.imwrite(path + file_name, img_rgb)
                average = [x1 + avg_x, y1 + avg_y]
                my_list = list(max_loc)
                my_list[0] = my_list[0] + x1
                my_list[1] = my_list[1] + y1
                max_loc = tuple(my_list)
            else:
                # print("drawing boxes", name)
                cv2.imwrite(path1 + "\\Mask" + file_name, img_gray)
                cv2.imwrite(path1 + file_name, img_rgb)
            return average

        if return_value == "top_left":
            return max_loc


def im_search_in_area(image, count, look_for="None",
                      x1=0, y1=0, x2=Resolution[0], y2=Resolution[1], precision=0.7, im=None):
    countx = 0
    return_value = "center"
    file_name = str(count) + str(look_for)
    # Take screenshot
    img_rgb = im_screenshot(file_name, x1, y1, x2, y2)
    if img_rgb is None:
        print(img_rgb, "ERROR reading image")
    else:
        try:
            os.remove(file_name)
        except IOError:
            123
            # print("ERROR!")
            result = im_processing(image, file_name, look_for,
                                   x1, y1, img_rgb, return_value,  precision)
            return result


def search_click_image(image, action, x1=0, y1=0, x2=Resolution[0], y2=Resolution[1], timestamp=0.1,
                       offset=5, precision=0.7, click_all="no"):
    file_name = "search_click_image"
    img_rgb = im_screenshot(file_name, x1, y1, x2, y2)

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


def PressKey_image(image):
    img = cv2.imread(image)
    height, width, channels = img.shape
    x = path.basename(image)[0]
    pyautogui.press('' + x)


def image2text(x1=0, y1=0, x2=Resolution[0], y2=Resolution[1], method=' --oem 3 --psm 7'):
    count = 0
    filename = "image2text"
    # BaseCoord = imagesearcharea( 1182, 324, 1357, 381, precision=0.95)
    # image_screenshot = pyautogui.screenshot("Screenshot.png", region=(x1, y1, x2, y2))
    with mss.mss() as sct:
        # The screen part to capture
        region = {'left': x1, 'top': y1, 'width': x2, 'height': y2}
        # Grab the data
        image_screenshot = mss.mss().grab(region)
        # Save to the picture file
        mss.tools.to_png(image_screenshot.rgb, image_screenshot.size, output='Temp_files\\Screenshot[' + filename + ']')
    image = cv2.imread('Temp_files\\Screenshot[' + filename + ']')

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


def casting_skills(skill_dictionary, my_class):
    template_1 = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\skill_S.png"
    x1_base = 960
    x1 = x1_base
    y1 = 980
    x2 = 40
    y2 = 42
    count = 0
    print(skill_dictionary)
    dictionary_values = list(skill_dictionary.values())
    dictionary_keys = list(skill_dictionary.keys())
    print(dictionary_keys)
    precision = 0.8
    identity = 'none'
    if my_class == "Bard":
        identity = "combo"
    elif my_class == "Paladin":
        identity = "normal"
    elif my_class == "Sorceress":
        identity = "normal"
    elif my_class == "Deathblade":
        identity = "normal"
    elif my_class == "Gunlancer":
        identity = "normal"
    elif my_class == "Lance master":
        identity = "normal"
    elif my_class == "Arcana":
        identity = "Arcana"
    elif my_class == "Artillerist":
        picture = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\Class\\Identity\\Artillerist_identity.png"
        position = imagesearch_fast_area(picture, x1=1100, y1=800, x2=300, y2=200, precision=0.9)
        print(position)
        if position != [-1, -1]:
            print("CASTING IDENTITY")
            pydirectinput.press("z")
            time.sleep(0.7)
            pydirectinput.press("r")
            pydirectinput.press("q")
            pydirectinput.press("q")
            pydirectinput.press("r")
            time.sleep(0.5)
            pydirectinput.keyDown("w")
            time.sleep(4)
            pydirectinput.keyUp("w")
            time.sleep(0.5)
            pydirectinput.press("e")
            time.sleep(6)
            pydirectinput.press("z")
    else:
        identity = "none"
        print("IDENTITY IS NONE")

    if identity == "combo":
        pydirectinput.press("x")
        time.sleep(0.4)
        pydirectinput.press("x")
    elif identity == "normal":
        pydirectinput.press("z")
    elif identity == "Arcana":
        pydirectinput.press("z")
        time.sleep(0.1)
        pydirectinput.press("x")

    for x in range(0, 8, 1):
        x1 = x1 + 47
        if count == 4:
            y1 = y1 + 50
            x1 = x1_base + 67
        file_name = str(count) + "casting_skills"
        # Take screenshot
        img_rgb = im_screenshot(file_name, x1=x1, y1=y1, x2=x2, y2=y2)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        # plt.imshow(img_rgb)
        # plt.show()
        template = cv2.imread(template_1, 0)
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= precision)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val < precision:
            ready = "yes"
            if dictionary_values[count] == "normal" and ready != "no":
                print(dictionary_keys[count])
                pydirectinput.press(dictionary_keys[count])
                pydirectinput.press(dictionary_keys[count])
                time.sleep(0.1)
                pydirectinput.press(dictionary_keys[count])
            if dictionary_values[count] == "combo" and ready != "no":
                pydirectinput.press(dictionary_keys[count])
                time.sleep(0.2)
                pydirectinput.press(dictionary_keys[count])
                time.sleep(0.2)
                pydirectinput.press(dictionary_keys[count])
                time.sleep(0.2)
                pydirectinput.press(dictionary_keys[count])
            if dictionary_values[count] == "holding" and ready != "no":
                pydirectinput.keyDown(dictionary_keys[count])
                time.sleep(2)
                pydirectinput.keyUp(dictionary_keys[count])
        else:
            print("DONT CAST")
        pydirectinput.mouseDown(button='right')
        time.sleep(0.5)
        pydirectinput.mouseUp(button='right')
        count += 1
    print("FINISHED")
