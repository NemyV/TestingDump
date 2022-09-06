import pyautogui
import glob
from ImgRec import imagesearch_region_loop
from ImgRec import Click_on_Image_inside_region
from window import Window
import cv2
import time
import win32api
from ImgRec import click
from ImgRec import Click_on_Image
from ImgRec import form
from ImgRec import imagesearcharea
from ImgRec import imagesearch_numLoop
from ImgRec import FindImageArea
import timeit
import argparse

import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open("tutorialx").sheet1  # Open the spreadhseet

from PIL import Image
from pytesseract import pytesseract

path_to_tesseract = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract

test1 = r"E:\Lost ark serious\Lost ark buttons\LA skills\Screenshot_1.png"
test2 = r"C:\Users\AdminN\Pictures\1Testing BLA\Rank Brick.png"
test3 = r"C:\Users\AdminN\Pictures\1Testing BLA\Gold Coin.jpg"
test4 = r"C:\Users\AdminN\Pictures\1Testing BLA\Screenshot_1.jpg"

posxEND = 2000
posyEND = 950

# Extracting AH
def a():
    BaseCoord = imagesearcharea(test2, 0, 0, posxEND, posyEND, precision=0.95)
    # BaseCoord = [100,25]
    # imagesearcharea(test3, 5, 5, posxEND, posyEND,precision=0.8)
    # Click_on_Image_inside_region(test1, 680, 850, posxEND, posyEND, 1)
    print(BaseCoord[0], BaseCoord[1])
    Name = [210, 45]
    Number = [70, 25]
    print(BaseCoord)
    count = 0
    countcell = 2
    dictionary = {}
    if BaseCoord != [-1, -1]:
        # name
        x = BaseCoord[0] + (15)
        y = BaseCoord[1] + (40)
        # number
        x1 = BaseCoord[0] + (704)
        y1 = BaseCoord[1] + (47)
        while 0 <= count < 10:
            count = count + 1
            # Name Screenshots
            im = pyautogui.screenshot(region=(x, y, Name[0], Name[1]))
            im.save('ItemName' + str(count) + '.png')
            x = x
            y = y + (57)
            text1 = pytesseract.image_to_string(im, config='--psm 12')

            # Number Screenshots
            im = pyautogui.screenshot(region=(x1, y1, Number[0], Number[1]))
            im.save('Number' + str(count) + '.png')
            x1 = x1
            y1 = y1 + (57)

            text = pytesseract.image_to_string(im, config="-c tessedit"
                                                          "_char_whitelist=1234567890"
                                                          " --psm 7"
                                                          " ")
            sheet.update_cell(2+count, 2, text1)
            sheet.update_cell(2+count, 3, text)

    #print(text)
    #print(dictionary)
    # insertRow = ["hello", 5, "red", "blue"]
    # sheet.insert_row(dictionary, 4)


def b():
    imagesearch_numLoop(test2, 0.5, 2)
    # Click_on_Image(test1, 'left', 1)


# while True:
#     for z in LAskillInFi:
#         Keypress = ''
#         Keypress = FindImageArea(z, 680, 850, posxEND, posyEND)
#         print("this is Keypress")
#         print(Keypress)
#         if Keypress == [-1, -1]:
#             123
#         else:
#             time.sleep(1.1)
#             form.send_keystrokes(Keypress)
#             time.sleep(0.07)
a()

