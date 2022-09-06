
import sys
sys.path.insert(0, r"E:\Hello wolrd Python")


import glob
import random
import time
import pyscreenshot as ImageGrab
from PIL import ImageEnhance, ImageOps

# Win32 Imports
import win32gui
import win32api
import win32con as wcon

# Connect to the Application
from pywinauto import Application

from ImgRec import processdetails

Lookfor = 'LOSTARK.exe'  # Name of the process to look for

from pytesseract import *
import pytesseract
from PIL import ImageTk, Image

# Import from other files/classes
from FINDWINDOW import WindowMgr

# Import IMG Recognition
from ImgRec import imagesearch
from ImgRec import imagesearch_region_loop
from ImgRec import ImageCropSEARCH
from ImgRec import Search_image_return_count
from ImgRec import imagesearch_count
from ImgRec import click
from ImgRec import Click_on_Image
from ImgRec import form
from ImgRec import imagesearch_numLoop

#Import from window
from window import Window


#TopLeft corner coordinates of the screen and then resoluton (Height and with)
Topleftx = Window.WindowCoordArr[0]
Toplefty = Window.WindowCoordArr[1]
WIDTH = Window.WindowCoordArr[2]
HEIGHT = Window.WindowCoordArr[3]
def Fishing():
    while True:
        count = 0
        # cast W at position START
        form.send_keystrokes('')
        win32api.SetCursorPos((1200, 642))

        # Check if you can cast NET/Possibly same as normal one with priority of finding net
        for f in FINDFishingSTART:
            pos = imagesearch(f, 0.9)
            GlobalLabel = (pos)
            # pydirectinput.moveTo(int(pos[0]),int(pos[1]))
            if pos != [-1, -1]:
                form.send_keystrokes('a')
                count = 1
                time.sleep(6)
            else:
                form.send_keystrokes('w')

        if count == 1:
            GlobalLabel = ("count is :")
            GlobalLabel = (count)
            for i in range(0, 20, 1):
                # repetition time in loop add it
                for f in FINDFishingNETGAME:
                    # search for exclamation mark
                    pos = imagesearch_region_loop(f, 230, 270, 500, 700, 0.05, 0.8)
                    if pos != [-1, -1]:
                        GlobalLabel = ("Found PERFECT")
                        for i in range(0, 20, 1):
                            form.send_keystrokes('space')
                            time.sleep(0.07)

        # If you want to cast buffs
        # for f in FishingBUFFS:
        # search for exclamation mark
        for f in FINDFishingCATCH:
            # search for exclamation mark
            time.sleep(5)
            GlobalLabel = ("this is a string :")
            GlobalLabel = (f)
            # pos = imagesearch_loop(f, 0.1)
            # pos = imagesearch_region_loop(f, TOPLMIDLE[0],TOPLMIDLE[1], BOTRMIDLE[0],BOTRMIDLE[1], 0.05, 0.8)
            pos = ImageCropSEARCH(f, TOPLMIDLE[0], TOPLMIDLE[1], BOTRMIDLE[0], BOTRMIDLE[1], 0.05, 0.8)
            GlobalLabel = (pos)
            if pos != [-1, -1]:
                GlobalLabel = ("FOUND MARK")
                form.send_keystrokes('w')
                time.sleep(6)
        GlobalLabel = ("finished fishing loop")


# app = Application(backend="win32").connect(process=processdetails(Lookfor)[0])
# form = app.window(title_re="LOST ARK")


def Start_of_stage(count):
    count += 1
    form.send_keystrokes('')
    win32api.SetCursorPos((990, 160))
    click(990, 160, button='right')
    time.sleep(2)
    if count == 2:
        return count
    GlobalLabel = ("finished this shit")  # ends the if and foo at the same time


def REVIVECHARACTER():
    # randomnumber = random.randint(1, 5)  # Integer from 1 to 10, endpoints included
    # randomnumber1 = random.randint(1, 6)
    # randomfloat = random.uniform(0.2, 1)
    # list1 = ['w', 's']
    # defense = ['d', 'e']
    # randomjump = ['r', 'a']
    # randomATTACK = random.sample(list1, 1)
    # randomDEFENSE = random.sample(defense, 1)
    GlobalLabel = ("Character died reviving and V")
    for f in checkIFDEAD:
        Click_on_Image(f, 'left', 1)
    time.sleep(2)
    form.send_keystrokes('a')
    time.sleep(0.5)
    form.send_keystrokes('v')
    time.sleep(2)
    Skills_no_movement(23)


def ENTERstage():
    GlobalLabel = ("Enter stage has started")
    for z in checkIFENTER:
        Click_on_Image(z, 'left', 1)


def ENDSTAGE(image):
    form.send_keystrokes('')
    win32api.SetCursorPos((990, 160))
    click(990, 160, button='right')
    time.sleep(2)


def StateCHECKimg(repeat):
    global GlobalLabel
    count = 0;
    countreward = 0;
    # looksofr image this amount of times before it gives up
    thistimes = 3
    for i in range(0, repeat, 1):
        GlobalLabel = (count)
        # count = imagesearch_count(checkstate + 'reward for passings.bmp')
        GlobalLabel = ('Current state is:')
        for g in checkIFDEAD:
            GlobalLabel = (g)
            # g = str
            count = Search_image_return_count(g, 0.05, thistimes, 0.9)
            if count <= 2:
                GlobalLabel = ('Character is DEAD')
                GlobalLabel = (count)
                REVIVECHARACTER()
        for c in checkIFDISMANTLE:
            GlobalLabel = (c)
            count = Search_image_return_count(c, 0.05, thistimes, 0.85)
            if count <= 2:
                DismantleBalls()
        for z in checkIFENTER:
            GlobalLabel = (z)
            count = Search_image_return_count(z, 0.05, thistimes, 0.95)
            if count <= 2:
                GlobalLabel = ('Entering stage... Found this image : ' + z)
                ENTERstage()
                Skills_no_movement(23)


def Skills_no_movement(repeat):
    global GlobalLabel
    # GlobalLabel = (Topleftx)
    # GlobalLabel = (Toplefty)
    # GlobalLabel = (WIDTH)
    # GlobalLabel = (HEIGHT)
    GlobalLabel = ("skill_no_movement started")
    testx = int(Topleftx+(WIDTH*0.6))
    testy = int(Toplefty+(HEIGHT*0.25))
    GlobalLabel = (testx , testy)
    # MOVING CHARACTER closer to middle
    time.sleep(0.5)
    form.send_keystrokes('')
    win32api.SetCursorPos((testx, testy))
    click(testx, testy, 'right')
    time.sleep(1)
    form.send_keystrokes('')
    win32api.SetCursorPos((testx, testy))
    click(testx, testy, 'right')
    # pydirectinput.click(1106, 298, button='right')
    time.sleep(1)
    count = 0
    checkLcount = 0
    # while (countx < 3):

    for i in range(0, repeat, 1):
        GlobalLabel = (count)
        # count = imagesearch_count(checkstate + 'reward for passings.bmp')
        for g in checklist:
            checkLcount = 0
            # GlobalLabel = ('Current state is:')
            # GlobalLabel = (g)
            checkLcount += imagesearch_count(g)
            # cases errors
            if checkLcount >= 1:
                GlobalLabel = ('Something is wrong StateCheck found... image: ' + g)
                StateCHECKimg(1)
            else:
                GlobalLabel = ("Keep on fighting baby")
            # extract the name of the image that is found on the screen
            # DO THIS : based on the name of the image prob GOTO command or something
            # similar or all placed in one loop under definition of check
            # g = str
            # if str.find("DEAD") != -1
            # GOTO here
            # GlobalLabel = (count)
        if count == 0:
            # GlobalLabel = (count)

            randomnumber = random.randint(1, 5)  # Integer from 1 to 10, endpoints included
            randomnumber1 = random.randint(1, 6)
            randomfloat = random.uniform(0.2, 1)

            list1 = ['w', 's']
            defense = ['d', 'e']

            randomjump = ['r', 'a']
            randomATTACK = random.sample(list1, 1)
            randomDEFENSE = random.sample(defense, 1)
            # move to center
            form.send_keystrokes('')
            win32api.SetCursorPos((640 + randomnumber, 533 + randomnumber1))

            time.sleep(randomfloat)
            form.send_keystrokes('a')
            time.sleep(randomfloat)
            form.send_keystrokes('f')
            time.sleep(0.07)
            form.send_keystrokes('f')
            time.sleep(randomfloat)
            form.send_keystrokes('a')
            time.sleep(randomfloat)
            form.send_keystrokes(randomDEFENSE)
            time.sleep(randomfloat)
            form.send_keystrokes('a')
            time.sleep(randomfloat)
            form.send_keystrokes(randomATTACK)
            form.send_keystrokes('a')
            time.sleep(randomfloat)
        else:
            for g in checkIFDEAD:
                # GlobalLabel = ('Current state is:')
                # GlobalLabel = (g)
                deadcheck = 0
                deadcheck += imagesearch_count(g)
                # extract the name of the image that is found on the screen
                # DO THIS : based on the name of the image prob GOTO command or something
                # similar or all placed in one loop under definition of check
                # g = str
                # if str.find("DEAD") != -1
                # GOTO here
                # GlobalLabel = (count)
                if deadcheck >= 1:
                    GlobalLabel = ('Character died reviving...')
                    REVIVECHARACTER()
                else:
                    GlobalLabel = ("STOPPING and restarting")
                    continue
                    break


def focus_window(NameofWindow):
    w = WindowMgr()
    w.find_window_wildcard(NameofWindow)
    w.set_foreground()


def Storebracelet():
    Click_on_Image()

def OpenDisINV():
    # open dismantle button

    form.send_keystrokes('i')

    GlobalLabel = ("FOUND")


def DismantleBalls():
    global GlobalLabel
    randomnumber = random.randint(1, 5)  # Integer from 1 to 10, endpoints included
    randomnumber1 = random.randint(1, 6)
    randomfloat = random.uniform(0.2, 1)
    GlobalLabel = (randomfloat)
    randomwaittime = 0.25 + randomfloat

    #RESOLUTION FIX
    #1920x1080
    firstbottomrowX = 1500
    firstbottomrowY = 717
    steps = 39
    maxstepsX = steps * 10
    maxstepsY = steps * 2
    StartDIS = 50
    middle = 20

    PosDisBtn = imagesearch_numLoop(DisDetInv, 0.1, 7)
    GlobalLabel = ("position of dismantle button is : ")
    GlobalLabel = (PosDisBtn)

    while PosDisBtn == [-1,-1]:
        GlobalLabel = ("inside if")
        form.send_keystrokes('i')
        PosDisBtn = imagesearch_numLoop(DisDetInv, 0.1, 7)
    else:
        GlobalLabel = ("not -1 -1")



    x = PosDisBtn[0] #1567
    y = PosDisBtn[1] #741
    GlobalLabel = (x,y)
    StartDISX = x + 27
    StartDISY = y + 8

    SelEpicX = x - 160
    SelEpicY = y - 66

    AddingX = x - 68
    AddingY = y - 27

    DisBtnX = x - 239
    DisBtnY = y + 12

    TakeBtX = x + 111
    TakeBtY = y - 83
    #win32api.SetCursorPos((TakeBtX, TakeBtY))
    #####
    step = 0
    form.send_keystrokes('i')

    time.sleep(1)

    while True:
        form.send_keystrokes('')
        win32api.SetCursorPos((15, 15))
        count = (Search_image_return_count(DisDetInv, 0.1, 10))
        GlobalLabel = (count)
        if count < 7:
            # open dismantle button
            time.sleep(1)
            form.send_keystrokes('')
            win32api.SetCursorPos((StartDISX, StartDISY))
            click(StartDISX, StartDISY, button='left')
            countx = (Search_image_return_count(DisITEMwin, 0.1, 10))
            while countx > 5:
                GlobalLabel = ("NOT FOUND")
                form.send_keystrokes('i')
                time.sleep(1)
                form.send_keystrokes('')
                win32api.SetCursorPos((15, 15))
                countx = (Search_image_return_count(DisDetInv, 0.1, 10))
                if countx < 5:
                    form.send_keystrokes('')
                    win32api.SetCursorPos((StartDISX, StartDISY))
                    time.sleep(1)
                    form.send_keystrokes('')
                    win32api.SetCursorPos((StartDISX, StartDISY))
                    click(StartDISX, StartDISY, button='left')
                    # time.sleep(1)
                    # form.send_keystrokes('')
                    # win32api.SetCursorPos((15, 15))
                    countx = (Search_image_return_count(DisITEMwin, 0.1, 10))
            else:
                GlobalLabel = ("FOUND")
        # ##BRACELETS
        #     braceletO = (Search_image_return_count('D:\Lost ark serious\\Lost ark buttons\\Braclets\\Orange.png', 0.1,
        #                                            7))
        #
        #     braceletY = (Search_image_return_count('D:\Lost ark serious\\Lost ark buttons\\Braclets\\Yellow.png', 0.1,
        #                                            7))
        #     if braceletO < 5:
        #         GlobalLabel = ("found ORANGE")
        #         input("Press Enter to continue...")
        #
        #
        #     elif braceletY < 4:
        #         GlobalLabel = ("found Yellow")
        #         input("Press Enter to continue...")
        # ###BRACELETS

            # Select all epic - > dismantle -> enter - > ok
            time.sleep(1)
            form.send_keystrokes('')
            win32api.SetCursorPos((SelEpicX, SelEpicY))
            form.send_keystrokes('')
            click(SelEpicX, SelEpicY, button='left')
            time.sleep(1)

            for stepy in range(0, -maxstepsY, -steps):
                for stepx in range(0, maxstepsX, steps):
                    form.send_keystrokes('')
                    win32api.SetCursorPos((AddingX + stepx + randomnumber,
                                           AddingY + stepy + randomnumber1))
                    click(AddingX + stepx + randomnumber, AddingY + stepy + randomnumber1,
                          button='right')
                    # GlobalLabel = (step)
                    time.sleep(randomwaittime)

            time.sleep(1)
            form.send_keystrokes('')
            win32api.SetCursorPos((DisBtnX, DisBtnY,))
            click(DisBtnX, DisBtnY, button='left')
            time.sleep(1)
            form.send_keystrokes('{ENTER}')
            time.sleep(1)
            form.send_keystrokes('')
            win32api.SetCursorPos((TakeBtX, TakeBtY,))
            click(TakeBtX, TakeBtY, button='left')
            time.sleep(randomwaittime)

            form.send_keystrokes('i')

            time.sleep(0.25 + randomfloat)

            time.sleep(0.25 + randomfloat)

            break
        else:
            GlobalLabel = ('Did not find Dismantle window.bmp. Closing inventory')
            form.send_keystrokes('i')
            time.sleep(0.25 + randomfloat)
    GlobalLabel = ("Finished Dismantle")
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

    GlobalLabel = (text)


###### RESOLUTION FIX UNDER
EpicPath = "E:\\Lost ark serious\\Lost ark buttons\\"

# EpicPath = "E:\\Lost ark serious\\Lost ark buttons\\1280x1024\\"  #UN-COMMENT for 1280x1024

DisDetInv = EpicPath + 'DISMANTLE\\Detect inventory.png'
DisITEMwin = EpicPath + 'Dismantle ITEMS window.bmp'

###RESOLUTION ISSUES FIXES ABOVE

txtfiles = []
for file in glob.glob("*.bmp"):
    txtfiles.append(file)

###PAY ATTENTION TO EXTENSION
#CONVERT EVERYTHING TO PNG FOR better implementation
# Coordinates on square on screen
TOPLMIDLE = (880, 350)
BOTRMIDLE = (1080, 800)

# Global stuff
checkthis = EpicPath + 'Check'
movement = EpicPath + 'Movement'

checklist = [f for f in glob.glob(checkthis + "**/*.png")]
movementlist = [m for m in glob.glob(movement + "**/*.png")]

# Yozmund
checkDEAD = EpicPath + 'DEAD'
checkENTER = EpicPath + 'ENTER'
checkDISMANTLE = EpicPath + 'DISMANTLE'

checkIFDEAD = [m for m in glob.glob(checkDEAD + "**/*.png")]
checkIFENTER = [z for z in glob.glob(checkENTER + "**/*.png")]
checkIFDISMANTLE = [e for e in glob.glob(checkDISMANTLE + "**/*.png")]

# Labels
GlobalLabel = ''

# Fishing
CheckFISHING = EpicPath + 'FISHING'
FishingBUFFS = EpicPath + 'FISHING\\BUFFS'
FishingCATCH = EpicPath + 'FISHING\\EXCLAMATION'
FishingSTART = EpicPath + 'FISHING\\STARTFishing'
FishingNETGAME = EpicPath + 'FISHING\\NETGAME'

CheckIFFISHING = [x for x in glob.glob(CheckFISHING + "**/*.png")]
FINDFishingCATCH = [x for x in glob.glob(FishingCATCH + "**/*.png")]
FINDFishingSTART = [x for x in glob.glob(FishingSTART + "**/*.png")]
FINDFishingNETGAME = [x for x in glob.glob(FishingNETGAME + "**/*.png")]

###PAY ATTENTION TO EXTENSION

# GlobalLabel = (checklist)

# x = click(935, 473, button='right')
# y = click(934, 561, button='right')
# z = click(1000, 530, button='right')
# c = click(870, 519, button='right')
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
#         GlobalLabel = ("program finished loop for " + str(restart) + "th time")
#         for f in checklist:
#             focus_window('LOST ARK')
#             # pyautogui.dragTo(1280, 436,0.6, button='left')
#             # focus_window('LOST ARK')
#             # GlobalLabel = ('finished')
#             # imagesearch_numLoop(f, 0.5, 2, 0.9)
#             StateCHECKimg(1)
#             # ENTERstage()
#             # Fishing()
#             # Click_on_Image(f, 'left', 1)
#         # Midlescreen_Circle_rightclick()
#         # Skills_no_movement(23)
#         # DismantleBalls()
#         # DO NOT FORGET TO DEBUG CHANGING KEYBOARD TO RUSSIAN FUKS the program
#         # Grabimage_text()
#         # pos = imagesearch_numLoop(m, 0.1, 1, 0.9)
#         # #GlobalLabel = (m)r
#         # #GlobalLabel = (path.basename(f)[0])
#         # if pos[0] != -1:
#         #      pyautogui.press('g')
#         #     #
#         #     # PressKey_image(f)
#         #     # pyautogui.press('f1'
