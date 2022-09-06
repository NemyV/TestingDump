import time
import pydirectinput
import pyautogui
from kivy.config import Config
from kivy.config import ConfigParser
from pytesseract import pytesseract
from configparser import SafeConfigParser

import numpy as np
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract
list_of_char = ["Ggjustice", "Ggbard", "Stringsy",
                "Gladiatrixs", "Pureluckc", "Ggdin",
                "Mesmashy", "Sheeeshaa", "Ggsorc", "Ggwarlord"]

finished_char =[]
finished_char.append("Mesmashy")
Resolution = [2560, 1080]


def image2text(x1=0, y1=0, x2=Resolution[0], y2=Resolution[1]):
    count = 0
    # BaseCoord = imagesearcharea( 1182, 324, 1357, 381, precision=0.95)
    image = pyautogui.screenshot(region=(x1, y1, x2, y2))
    image.save('ItemName' + str(count) + '.png')
    text = pytesseract.image_to_string(image, config='--psm 12')
    # print(text)
    return text


def switching_char(finished_char):
    # maybe use dictionary ??
    count = 0

    switch_stepx = 250
    switch_stepy = 110

    first_x = 650
    first_y = 380

    box_size_x = 250
    box_size_y = 75
    # formula for going through all 9 characters
    for i in range(0, 4, 1):
        count = count + 1
        print(count)
        # count devideable by 3
        first_x = first_x + switch_stepx
        text = image2text(x1=first_x, y1=first_y,
                          x2=box_size_x, y2=box_size_y)
        print(text)
        if count % 3 == 0:
            print("count is DEVIDABLE", count)
            time.sleep(1)
            first_y = first_y + switch_stepy
            first_x = 900 - switch_stepx

        generator_expression = (x for x in finished_char if x in text)

        for g in generator_expression:
            print("GENERATOR WORKING")
            time.sleep(1)
            pydirectinput.click(first_x,
                                first_y, button="left")
            time.sleep(1)
    return text, first_x, first_y

import cv2
import numpy as np
import random

def r(num, rand):
    return num + rand * random.random()

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
        height, width, channels = img.shape
        # Added +x1 and +y1 IF YOU GET ERROR remove?
        pyautogui.moveTo(pos[0] + r(width / 2, offset) + x1,
                         pos[1] + r(height / 2, offset) + y1,
                         timestamp)
        pyautogui.click(button=action)

# for i in range(0, 9, 1):
#     print(list_of_char[i])
Buttons = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\"
Daily = Buttons + 'Daily Quest\\'
# switching_char(finished_char)
chat = Daily + "Misc\\Minimize_chat.png"



# ERROR WITH FUNCTION WHEN INSERTING COSTUM region for searching!!!!!


# search_click_image(chat, "left", x1=0, y1=710, x2=600, y2=1050)
test_array = ["qegeqeg", "qgwepgiojwe"]

# These changes need to be present !!!!BEFORE you import Window!!!!
Config.read("example.ini")
# Config.set('account', 'characters', 'fake')
character = 'character'
count = 0

list_of_char = ["Ggjustice", "Pureluckc",
                "Ggbard", "Stringsy", "Gladiatrixs", "Ggdin",
                "Mesmashy", "Sheeeshaa", "Ggsorc", "Ggwarlord"]

text_input = "gg"
text_input_remove = "gg"
# Config.remove_option('Account',)
list_of_char.append(text_input)

# print(list_of_char)

u = np.array(list_of_char)
for x in np.unique(u):
    character = 'character'
    count = count + 1
    character = ""+character + str(count)
    # print(character, x)
    Config.set('account', character, x)
    if x == text_input_remove:
        print(x, character)
        Config.remove_option('account', character)
    Config.write()
list_of_char.clear()
try:
    for i in range(1, 24, 1):
        character = 'character'
        character = "" + character + str(i)
        # print(character)
        list_of_char.append(Config.get('account', character))
        # if x == text_input_remove:
        #     Config.remove_option('account', character)
except:
    print("no option")
# configparser.ConfigParser()
parser = ConfigParser()
parser.read('example.ini')

for section_name in parser.sections():
    print('Section:', section_name)
    print('Options:', parser.options(section_name))
    # print('Values:'), parser.items(section_name)
    for name, value in parser.items(section_name):
        print('  %s = %s' % (name, value))

# for name, value in parser.items(section_name):
#     print('  %s = %s' % (name, value))

# print(list_of_char)
# print(list_of_char)

# test_array = Config.get('account', 'characters')
# print(test_array[5])
# Config.set('graphics', 'fullscreen', 'fake')






