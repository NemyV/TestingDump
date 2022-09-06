import glob
import time
import pydirectinput
import matplotlib.pyplot as plt
from kivy.config import ConfigParser
import os
import mss
import keyboard
import random
from Source.METHODS import im_search_in_area
import cv2
import numpy as np
import pyautogui
from multiprocessing.managers import NamespaceProxy, BaseManager
import multiprocessing
import inspect
from multiprocessing import Manager, Process, Pool

from pytesseract import pytesseract
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract
# DETECTING HP BARS IS VERY IMPORTANT with high % chance

Resolution = [2560, 1080]

MiniMCOORD = [round(Resolution[0] / 100 * 87.25),
              round(Resolution[1] / 100 * 3.75),
              round(Resolution[0] / 8.7),
              round(Resolution[1] / 4.25)]

txtfiles = []
for file in glob.glob("*.bmp"):
    txtfiles.append(file)

Buttons = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\"
CDung = Buttons + "ChaosDungeon\\"
Dead = Buttons + "Dead\\"
passing = Buttons + "Passing\\"
ReENTER = Buttons + "ReENTER\\"
Portal_no_mini = Buttons + "PortalNoMinimap\\"
Minimap = Buttons + "Minimap\\"

ChaosDung = [m for m in glob.glob(CDung + "/*.png")]
checkIFDEAD = [m for m in glob.glob(Dead + "**/*.png")]
passingthrough = [m for m in glob.glob(passing + "**/*.png")]
ReENTERing = [m for m in glob.glob(ReENTER + "**/*.png")]
PortalNOMINI = [m for m in glob.glob(Portal_no_mini + "**/*.png")]

minimap_red = [m for m in glob.glob(Minimap + "\\Red" + "**/*.png")]
minimap_boss = [m for m in glob.glob(Minimap + "\\Boss" + "**/*.png")]
minimap_portal = [m for m in glob.glob(Minimap + "\\Portal" + "**/*.png")]
minimap_elite = [m for m in glob.glob(Minimap + "\\Elite" + "**/*.png")]
minimap_tower = [m for m in glob.glob(Minimap + "\\Tower" + "**/*.png")]
minimap_dir = [m for m in glob.glob(Minimap + "/*.png")]

stage_fail = Buttons + "CheckIFclear\\Failed"

ChaosDung = [m for m in glob.glob(CDung + "**/*.png")]

checkIFDEAD = [m for m in glob.glob(Dead + "**/*.png")]
check_if_failed = [m for m in glob.glob(stage_fail + "/*.png")]


path = 'C:\\Users\\Ggjustice\\Pictures\\Buttons\\Testing\\HPbars\\'

path1 = 'C:\\Users\\Ggjustice\\Pictures\\Buttons\\Testing\\'

raw_path = 'C:\\Users\\Ggjustice\\Pictures\\Buttons\\Testing\\No filter\\'

try:
    filelist = glob.glob(os.path.join(path, "*"))
    for f in filelist:
        os.remove(f)
except IOError:
    123
try:
    filelist1 = glob.glob(os.path.join(path1, "*"))
    for f in filelist1:
        os.remove(f)
except IOError:
    123
try:
    filelist2 = glob.glob(os.path.join(raw_path, "*"))
    for f in filelist2:
        os.remove(f)
except IOError:
    123

Daily = Buttons + 'Daily Quest\\'

DailySwampLoc = Daily + 'Walling Swamp'
DailySwamp = [x for x in glob.glob(DailySwampLoc + "**/*.png")]

feiton_fail_check = Daily + 'Misc\\Feiton door'
fail_proof_faiton = [x for x in glob.glob(feiton_fail_check + "**/*.png")]


def r(num, rand):
    return num + rand * random.random()

def im_screenshot(filename='.png', x1=0, y1=0, x2=Resolution[0], y2=Resolution[1]):
    with mss.mss() as sct:
        # The screen part to capture
        region = {'left': x1, 'top': y1, 'width': x2, 'height': y2}
        # Grab the data
        image_screenshot = mss.mss().grab(region)
        # try to remove
        try:
            os.remove('Screenshot' + filename)
        except IOError:
            123
        # Save to the picture file
        mss.tools.to_png(image_screenshot.rgb, image_screenshot.size, output=('Temp_files\\Screenshot' + filename))
    #  VERY IMPORTANT so that multiple process don't conflict on same file name
    # NEW SOLUTION DELETE IF IT DOESNT WORK  = , cv2.IMREAD_UNCHANGED)
    img_rgb = cv2.imread('Temp_files\\Screenshot' + filename, cv2.IMREAD_UNCHANGED)
    return img_rgb


def im_search_count(image, precision=0.9):
    # Take screenshot
    img_rgb = im_screenshot("imagesearch_count.png")
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



def centeral_detection(switch):
    count_occurrance = 0
    while True:
        for g in ChaosDung:
            split_string = g.rsplit('\\')[6]
            print(split_string)
            startx = 600
            starty = 150
            count_occurrance = count_occurrance + 1
            occurances = ("0", count_occurrance, split_string)

            search = im_search_in_area(g, occurances,
                                       x1=startx, y1=starty,
                                       x2=2000, y2=900, precision=0.89)

def minimap_detection(switch):
    count_occurrance = 0
    while True:
        for g in Minimap_detection:
            # Get last 10 character
            # last_chars = g[-20:]
            split_string = g.rsplit('\\')[6]
            # print(split_string)

            count_occurrance = count_occurrance + 1
            occurances = "", count_occurrance, split_string
            # MINIMAP Searching
            search = im_search_in_area(g, occurances, look_for="Portal",
                                       x1=MiniMCOORD[0], y1=MiniMCOORD[1],
                                       x2=MiniMCOORD[2], y2=MiniMCOORD[3], precision=0.85)


def kill_all():
    print("KILLING ALL")
    time.sleep(1)
    for process in all_processes:
        process.terminate()
        process.kill()
        process.join()
    exit()
    os._exit(0)


def imagesearch_fast_area(image, x1=0, y1=0, x2=Resolution[0], y2=Resolution[1], precision=0.8):
    file_name = "imagesearch_fast_area.png"
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
    # Clicking on all occurances?
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
        h, w, c = img.shape
        # Added +x1 and +y1 IF YOU GET ERROR remove?
        print("FOUND IT")
        pyautogui.moveTo(pos[0] + r(w / 2, offset) + x1,
                         pos[1] + r(h / 2, offset) + y1,
                         timestamp)
        pyautogui.click(button=action)
        return pos


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


def imagesearch(image, precision=0.8):
    # im = pyautogui.screenshot()
    with mss.mss() as sct:

        # The screen part to capture
        region = {'left': 0, 'top': 0, 'width': Resolution[0], 'height': Resolution[1]}

        # Grab the data
        image_screenshot = mss.mss().grab(region)

        # Save to the picture file
        mss.tools.to_png(image_screenshot.rgb, image_screenshot.size, output='Screenshot.png')

    im = cv2.imread('Screenshot.png')
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


def Searchimage_return_position(image, maxSamples=1, precision=0.8):
    pos = imagesearch(image, precision)
    count = 0
    while pos == [-1, -1]:
        splitstring = image.rsplit('\\')[6]
        # print(splitstring)
        # print(image + " not found, waiting")
        pos = imagesearch(image, precision)
        count = count + 1
        if count > maxSamples:
            break
    return pos


def click_event(event, x, y, flags, params):
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)

        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,
                    str(x) + ',' + str(y),
                    (x, y), font,
                    1, (0, 125, 255), 2)
        cv2.imshow('image', img)
    # checking for right mouse clicks
    if event == cv2.EVENT_RBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        cv2.putText(img,
                    str(b) + ',' + str(g) + ',' + str(r),
                    (x, y), font, 1,
                    (0, 255, 255), 2)
        cv2.imshow('image', img)


if __name__ == '__main__':
    keyboard.add_hotkey('ctrl+shift+q', kill_all)
    listmanager = Manager()
    normal_processes = listmanager.list()
    combat_processes = listmanager.list()
    all_processes = listmanager.list()
    switch = listmanager.list()

    BaseManager.register('Process', Process, ProcessProxy, exposed=tuple(dir(ProcessProxy)))
    manager = BaseManager()
    manager.start()
    # central_detectors = manager.Process(target=centeral_detection,
    #                                     args=(switch,))
    # combat_processes.append(central_detectors)
    # all_processes.append(central_detectors)
    # central_detectors.start()
    #
    # minimap_detections = manager.Process(target=minimap_detection,
    #                                      args=(switch,))
    # normal_processes.append(minimap_detections)
    # all_processes.append(minimap_detections)
    # minimap_detections.start()

    # # # Testing CENTRAL detection
    # # while True:
    # count_occurrance = 0
    # movementdelay = 0.4
    # for g in ChaosDung:
    #     split_string = g.rsplit('\\')[6]
    #     # print(split_string)
    #     startx = 0
    #     starty = round(Resolution[0]/100*1)
    #     count_occurrance = count_occurrance + 1
    #     occurances = str(count_occurrance) + str(split_string)
    #     # print(g)
    #     # RESOLUTION Searching
    #     search = im_search_in_area(g, occurances, look_for="HPbar", precision=0.8,
    #                                x1=startx, y1=starty, y2=round(Resolution[1]/100*83))
    #     print(search)
    #     if search == [-1, -1]:
    #         123
    #     else:
    #         print("Found HPbar ", split_string)
    #         x1 = round(search[0])
    #         y1 = round(search[1])
    #         pydirectinput.moveTo(x1, y1+125)
    #         time.sleep(movementdelay)
    #         if "PORT" in g:
    #             countingportattempt = 0
    #             break_switch = 0

    # Testing MINIMAP detection
    # count_occurrance = 0
    # for g in minimap_dir:
    #     if "Boss" in g:
    #         looking_for = "Boss"
    #     elif "Portal" in g:
    #         looking_for = "Portal"
    #     elif "Elite" in g:
    #         looking_for = "Elite"
    #     elif "Tower" in g:
    #         looking_for = "Tower"
    #
    #     split_string = g.rsplit('\\')[6]
    #     count_occurrance = count_occurrance + 1
    #     occurances = str(count_occurrance)+ str(split_string)
    #     # print(g, split_string)
    #     # MINIMAP Searching
    #     search = im_search_in_area(g, occurances, look_for=looking_for,
    #                                x1=MiniMCOORD[0], y1=MiniMCOORD[1],
    #                                x2=MiniMCOORD[2], y2=MiniMCOORD[3], precision=0.6)
    #     # print("other", looking_for)
    #     # print(search)
    #     if search != [-1, -1] and "Portal" in g:
    #         print("FOUND ", g)
    #         break
    #
    # for f in minimap_red:
    #     # print("red")
    #     print(f)
    #     split_string = f.rsplit('\\')[6]
    #     count_occurrance = count_occurrance + 1
    #     occurances = str(count_occurrance) + str(split_string)
    #     search = im_search_in_area(f, occurances, look_for="Red",
    #                                x1=MiniMCOORD[0], y1=MiniMCOORD[1],
    #                                x2=MiniMCOORD[2], y2=MiniMCOORD[3], precision=0.6)
    #     if search != [-1, -1]:
    #         print("found red")

    # LOADING SCREEN TESTS
    # def waiting_for_loading_screen(tries=15):
    #     count_loading = 0
    #     for i in range(0, tries, 1):
    #         count_loading = count_loading + 1
    #         im = pyautogui.screenshot(region=(1652, 168, 240, 210))
    #         r, g, b = im.getpixel((1772 - 1652, 272 - 168))
    #         if r == 0 and g == 0 and b == 0:
    #             break
    #         time.sleep(0.6)
    #     if count_loading == tries:
    #         print("Loading screen not found")
    #     else:
    #         teleport = "yes"
    #         print("Loading screen found")
    #         time.sleep(2.5)
    #         for i in range(0, 577, 1):
    #             print("looking for black")
    #             im = pyautogui.screenshot(region=(1652, 168, 240, 210))
    #             r, g, b = im.getpixel((1772 - 1652, 272 - 168))
    #             if r == 0 and g == 0 and b == 0:
    #                 print("finished loading screen")
    #                 break
    #             time.sleep(0.15)
    #         return teleport

    # waiting_for_loading_screen()

    # # testing TEXT DETECTION
    # text = image2text(x1=630, y1=655, x2=200, y2=30, method=' --oem 3 --psm 7')
    # print(text)

    # # Testing WEEKLIES
    # Weekly = Daily + "\\Weeklies"
    # weekly_tasks = [x for x in glob.glob(Weekly + '\\Weekly tasks' + "**/*.png")]
    # target = "weekly"
    # name = "ALL"
    # # focus_window('LOST ARK')
    # time.sleep(1)
    # pydirectinput.keyDown('alt')
    # time.sleep(0.2)
    # pydirectinput.press('j')
    # time.sleep(0.2)
    # pydirectinput.keyUp('alt')
    # if target == "weekly":
    #     daily_button = Daily + "Misc\\Guild_request_button.png"
    #     search_click_image(daily_button, "left", precision=0.8)
    #     print("PRESSING GUILD REQUEST")
    #     time.sleep(1)
    #     for x in weekly_tasks:
    #         weekly_task_pos = Searchimage_return_position(x, 1, precision=0.92)
    #         pydirectinput.leftClick(weekly_task_pos[0]+500,
    #                                 weekly_task_pos[1])
    #     print("pressing weekly button")
    #     daily_button = Daily + "Misc\\Weekly_button.png"
    #     search_click_image(daily_button, "left")
    #     time.sleep(1)
    #     menu = Daily + "Misc\\menu.png"
    #     search_click_image(menu, "left")
    #
    #     favorites = Daily + "Misc\\Favorites.png"
    #     search_click_image(favorites, "left")
    #
    #     if name == "ALL":
    #         accept_all = Daily + "Misc\\Accept_quest.png"
    #         search_click_image(accept_all, "left", click_all="yes")

    # if search != [-1, -1]:
    #     x1, y1 = process_search(search)
    #     print(x1, y1)
    #     pydirectinput.mouseDown(x1, y1, button="right")
    #     time.sleep(movementdelay)
    #     pydirectinput.mouseUp(button="right")
    #     break
    # # TESTING SKILLS
    # skills_dict = {'q': "normal", 'w': "normal", 'e': "normal", 'r': "normal",  # PALADIN NO COOLDOWNS
    #                'a': "combo", 's': "normal", 'd': "normal", 'f': "combo",
    #                'z': "combo"}
    #
    #
    # def casting_skills(skill_dictionary):
    #     template_1 = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\skill_S.png"
    #     x1_base = 960
    #     x1 = x1_base
    #     y1 = 980
    #     x2 = 40
    #     y2 = 42
    #     count = 0
    #     dictionary_values = list(skill_dictionary.values())
    #     dictionary_keys = list(skill_dictionary.keys())
    #     print(dictionary_keys)
    #     # print(dictionary_values)
    #     precision = 0.8
    #     for x in range(0, 8, 1):
    #         x1 = x1 + 47
    #         print(count)
    #         if count == 4:
    #             y1 = y1 + 50
    #             x1 = x1_base + 67
    #         with mss.mss() as sct:
    #             # The screen part to capture
    #             region = {'left': x1, 'top': y1, 'width': x2, 'height': y2}
    #             # Grab the data
    #             image_screenshot = mss.mss().grab(region)
    #             # Save to the picture file
    #             mss.tools.to_png(image_screenshot.rgb, image_screenshot.size,
    #                              output=('Screenshot' + str(count) + ".png"))
    #             #  VERY IMPORTANT so that multiple process don't conflict on same file name
    #             img_rgb = cv2.imread('Screenshot' + str(count) + ".png", cv2.IMREAD_UNCHANGED)
    #
    #             img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    #
    #             # plt.imshow(img_rgb)
    #             # plt.show()
    #
    #             template = cv2.imread(template_1, 0)
    #             w, h = template.shape[::-1]
    #
    #             res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    #             loc = np.where(res >= precision)
    #             min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    #
    #         if max_val < precision:
    #             print("CAST")
    #             ready = "yes"
    #             # print([-1, -1])
    #         else:
    #             ready = "no"
    #             print("DONT CAST")
    #
    #         if dictionary_values[count] == "normal" and ready != "no":
    #             print(dictionary_keys[count])
    #             pydirectinput.press(dictionary_keys[count])
    #         if dictionary_values[count] == "combo" and ready != "no":
    #             pydirectinput.press(dictionary_keys[count])
    #             time.sleep(0.4)
    #             pydirectinput.press(dictionary_keys[count])
    #             time.sleep(0.4)
    #             pydirectinput.press(dictionary_keys[count])
    #         if dictionary_values[count] == "holding" and ready != "no":
    #             pydirectinput.keyDown(dictionary_keys[count])
    #             time.sleep(2)
    #             pydirectinput.keyUp(dictionary_keys[count])
    #         count += 1
    #     print("FINISHED")
    #
    # for x in range(0, 20, 1):
    #     casting_skills(skills_dict)
    # from pynput.keyboard import *
    #
    # keys = [KeyCode.from_char(c) for c in 'wasd']
    #
    #
    # def on_press(key):
    #     if key in keys:
    #         print(f'good key: {key}')
    #     else:
    #         print(f'bad key: {key}')
    #
    #
    # def on_release(key):
    #     if key == Key.esc:
    #         return False
    #
    #
    # with Listener(on_press=on_press, on_release=on_release) as listener:
    #     listener.join()
    im_screenshot()
    # for y in check_if_failed:
    #     position, count_images = im_search_count(y, precision=0.3)
    #     print(position)
    #     # pydirectinput.moveTo(position)
    #     if position != [-1, -1]:
    #         print("FOUND FAIL")
    #         # count_stage_fail += 1
    #     print("ALL GOOD")



    # # GETTING COORDINATES AND PIXEL COLOR AMAZING
    # # reading the image
    # img = cv2.imread('Screenshot1None.png', 1)
    # # displaying the image
    # cv2.imshow('image', img)
    # # setting mouse handler for the image
    # # and calling the click_event() function
    # cv2.setMouseCallback('image', click_event)
    # # wait for a key to be pressed to exit
    # cv2.waitKey(0)
    # # close the window
    # cv2.destroyAllWindows()
