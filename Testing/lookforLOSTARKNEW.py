import glob
from os import path
import cv2
import numpy as np
import pywinauto
import pyautogui
import win32gui
import win32con
#import pydirectinput
import random
import time
import pyscreenshot as ImageGrab
from PIL import ImageEnhance,ImageOps
from PIL import Image
from pytesseract import *
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
import pygetwindow as gw
import keyboard
from threading import Thread



'''
grabs a region (topx, topy, bottomx, bottomy)
to the tuple (topx, topy, width, height)
input : a tuple containing the 4 coordinates of the region to capture
output : a PIL image of the area selected.
'''


def region_grabber(region):
    x1 = region[0]
    y1 = region[1]
    width = region[2]-x1
    height = region[3]-y1

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


def click_image(image, pos,  action, timestamp, offset=5):
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
        print(image+" not found, waiting")
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
        print(image+" not found, waiting")
        time.sleep(timesample)
        pos = imagesearch(image, precision)
        count = count + 1
        if count > maxSamples:
            break
    return pos


#Same as above just returns count
def Search_image_return_count(image, timesample, maxSamples, precision=0.8):
    pos = imagesearch(image, precision)
    count = 0
    while pos[0] == -1:
        print(image+" not found, waiting")
        time.sleep(timesample)
        pos = imagesearch(image, precision)
        count = count + 1
        if count > maxSamples:
            break
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


def r(num, rand):
    return num + rand*random.random()


def PressKey_image(image):
    img = cv2.imread(image)
    height, width, channels = img.shape
    x = path.basename(image)[0]
    pyautogui.press(''+x)


def Start_of_stage(count):
    count += 1
    pyautogui.click(990, 160, button='right')
    time.sleep(2)
    if count == 2:
        return count
    print("finished this shit")  # ends the if and foo at the same time

def Fishing():
    for f in checkIFDEAD:
        Click_on_Image(f, 'left', 2, 1)
    time.sleep(1.5)


def Click_on_Image(image, action, timestamp, repeat, offset=5):
    count= 0
    randomnumber = random.randint(1, 5)  # Integer from 1 to 10, endpoints included
    randomnumber1 = random.randint(1, 6)
    randomfloat = random.uniform(0.2, 1)
    for i in range(0, repeat, 1):
        count += 1
        print('Checking '+image)
        img = cv2.imread(image)
        # Get position of "image" [imagesearch_loop(image, timesample, precision=0.8):]
        pos = imagesearch_numLoop(image, 0.5, 2)
        height, width, channels = img.shape
        time.sleep(randomfloat)
        #mouse.position = (int(pos[0] + r(width / 2, offset)), int(pos[1] + r(height / 2, offset)), timestamp)
        # action ( (button='left')
        x = int(pos[0] + r(width  / 2, offset))
        y = int(pos[1] + r(height / 2, offset))
        focus_window('LOST ARK')
        #x, y = pyautogui.position()
        pywinauto.mouse.move(coords=(x, y))
        #pydirectinput.click(button=action)
        if x > 100:
            pywinauto.mouse.click(button='left', coords=(x, y))
        else:
            print(height)
    print(count)
    return count



def REVIVECHARACTER():
    # randomnumber = random.randint(1, 5)  # Integer from 1 to 10, endpoints included
    # randomnumber1 = random.randint(1, 6)
    # randomfloat = random.uniform(0.2, 1)
    # list1 = ['w', 's']
    # defense = ['d', 'e']
    #
    # randomjump = ['r', 'a']
    # randomATTACK = random.sample(list1, 1)
    # randomDEFENSE = random.sample(defense, 1)

    #for i in range(0, repeat, 1):
    #count += 1
    for f in checkIFDEAD:
        Click_on_Image(f, 'left', 2, 1)
    time.sleep(1.5)
    keyboard.press_and_release('v')
    Skills_no_movement(23)


def ENTERstage():
    print("enter stage has started")
    for z in checkIFENTER:
        Click_on_Image(z, 'left', 2, 1)



def ENDSTAGE(image):
    pyautogui.click(990, 160, button='right')
    time.sleep(2)

def StateCHECKimg(repeat):
    count = 0;
    countreward= 0;
    for i in range(0, repeat, 1):
        print(count)
        # count = imagesearch_count(checkstate + 'reward for passings.bmp')
        for g in checkIFDEAD:
            print('Current state is:')
            print(g)
            # g = str
            count = Search_image_return_count(g, 1, 5)
            if count < 5:
                print('Character died reviving...')
                REVIVECHARACTER()
            for z in checkIFDISMANTLE:
                count = Search_image_return_count(z, 1, 5)
                if count < 5 and countreward < 1:
                    print('Entering stage...')
                    ENTERstage()
                for c in checkIFENTER:
                    count = Search_image_return_count(c, 1, 10)
                    if count < 10:
                        DismantleBalls()




def Skills_no_movement(repeat):
    print("skill_no_movement started")
    # MOVING CHARACTER closer to middle
    midleofscreenx = 1106
    midleofxcreeny = 298
    time.sleep(0.5)
    pywinauto.mouse.move(midleofscreenx, midleofxcreeny)
    pywinauto.mouse.click(midleofscreenx, midleofxcreeny)
    time.sleep(1)
    pywinauto.mouse.click(midleofscreenx, midleofxcreeny)   
    time.sleep(1)
    count = 0
    checklist
    #while (countx < 3):

    for i in range(0, repeat, 1):
        print(count)
        # count = imagesearch_count(checkstate + 'reward for passings.bmp')
        for g in checklist:
            print('Current state is:')
            print(g)
            count += imagesearch_count(g)
            #extract the name of the image that is found on the screen
            #DO THIS : based on the name of the image prob GOTO command or something
            # similar or all placed in one loop under definition of check
            #g = str
            #if str.find("DEAD") != -1
            #GOTO here

            print(count)

        if count == 0:
            #print(count)

            randomnumber = random.randint(1, 5)  # Integer from 1 to 10, endpoints included
            randomnumber1 = random.randint(1, 6)
            randomfloat = random.uniform(0.2, 1)

            list1 = ['w', 's']
            defense = ['d', 'e']

            randomjump = ['r', 'a']
            randomATTACK = random.sample(list1, 1)
            randomDEFENSE = random.sample(defense, 1)
            # move to center
            pywinauto.mouse.move(950 + randomnumber, 533 + randomnumber1)

            time.sleep(randomfloat)
            keyboard.press_and_release('a')
            time.sleep(randomfloat)
            keyboard.press_and_release('f')
            time.sleep(0.1)
            keyboard.press_and_release('f')
            time.sleep(randomfloat)
            keyboard.press_and_release('a')
            time.sleep(randomfloat)
            keyboard.press_and_release(randomDEFENSE)
            time.sleep(randomfloat)
            keyboard.press_and_release('a')
            time.sleep(randomfloat)
            keyboard.press_and_release(randomATTACK)
            keyboard.press_and_release('a')
            time.sleep(randomfloat)

        else:
            print("STOPPING and restarting")
            continue
            break


def alwaysontop():
    hwnd = win32gui.FindWindow('Notepad', None)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 100, 100, 300, 200, 0)



def focus_window(NameofWindow):
        focusthis = gw.getWindowsWithTitle(NameofWindow)[0]
        #focusthis.minimize()
        #focusthis.restore()
        focusthis.activate()





def DismantleBalls():
    randomnumber =random.randint(1, 5)  # Integer from 1 to 10, endpoints included
    randomnumber1=random.randint(1, 6)
    randomfloat=random.uniform(0.2, 1)
    print(randomfloat)
    firstbottomrowX = 1500
    firstbottomrowY = 717
    randomwaittime = 0.25 + randomfloat


    step = 0
    pyautogui.press('i')

    #open dismantle button
    time.sleep(1)
    pywinauto.mouse.move(1600, 754)
    time.sleep(1)
    pywinauto.mouse.click(1600, 754)
    
    #Click_on_Image('D:\\Lost ark serious\\Lost ark buttons\\Openthis\\Dissmantle.bmp', 'left', 2, 1)
    time.sleep(1)
    count = (Search_image_return_count('D:\\Lost ark serious\\Lost ark buttons\\DISMANTLE\\DISMANTLEwindow.bmp', 1, 10))
    print(count)
    if count < 10:
        # Select all epic - > dismantle -> enter - > ok
        time.sleep(1)
        pywinauto.mouse.click(1400, 677)
        time.sleep(1)
        # pywinauto.mouse.click(Button.right)
        #1307, 745, button='left')
        # time.sleep(1)
        # pyautogui.press('enter')
        # time.sleep(1)
        # pywinauto.mouse.click(Button.right)
        #1679, 660, button='left')
        # time.sleep(randomwaittime)

        for stepy in range(0, -80, -40):
            for stepx in range(0, 400, 40):
                pywinauto.mouse.move(firstbottomrowX + stepx + randomnumber, firstbottomrowY + stepy + randomnumber1)
                pywinauto.mouse.click(firstbottomrowX + stepx + randomnumber, firstbottomrowY + stepy + randomnumber1)
                
                # pyautogui.moveTo(firstbottomrowX + step + randomnumber, firstbottomrowY + randomnumber1, 2, pyautogui.easeInBounce)
                # pyautogui.click(firstbottomrowX + step + randomnumber, firstbottomrowY + randomnumber1, button='right')
                # print(step)
                time.sleep(randomwaittime)

        time.sleep(1)
        pywinauto.mouse.move(1307, 745)
        pywinauto.mouse.click(1307, 745)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)
        pywinauto.mouse.move(1679, 660)
        pywinauto.mouse.click(1679, 660)
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
        # pywinauto.mouse.move(244, 443)
        # time.sleep(0.25 + randomfloat)
        # pywinauto.mouse.move(1600, 750)
        # time.sleep(0.25 + randomfloat)
        # mouse.click(Button.left, 2)

        # pyautogui.write('rrr', interval=0.25+randomfloat)
        # CIRCLE MOVEMENT WITH RIGHTCLICK + R on KEYBOARD
        time.sleep(0.25 + randomfloat)

        time.sleep(0.25 + randomfloat)

        # pyautogui.dragTo(1857, 672,1)
    else:
        print('Did not find Dismantle window.bmp. Closing inventory')
        pyautogui.press('i')
        time.sleep(0.25 + randomfloat)
    return count


def Grabimage_text():
    im = ImageGrab.grab(bbox=(710, 845, 779, 857))
    #im.show()
    im.save('hp_image.jpg')
    # img = Image.open('hp_image.jpg').convert('LA')
    # img.save('greyscale.png')
    imageObject='hp_image.jpg'
    im = Image.open('hp_image.jpg')

    #invert image colors [if numbers are white]!!
    im_invert = ImageOps.invert(im)
    im_invert.save('original-image-1.png');

    time.sleep(1)
    img = Image.open('original-image-1.png')
    text = pytesseract.image_to_string(img)

    print(text)






######
EpicPath = "D:\\Lost ark serious\\Lost ark buttons\\"

checkthis = EpicPath+'Check'
movement = EpicPath+'Movement'

checkDEAD = EpicPath+'DEAD'
checkENTER = EpicPath+'ENTER'
checkDISMANTLE = EpicPath+'DISMANTLE'

txtfiles = []
for file in glob.glob("*.bmp"):
    txtfiles.append(file)

    ###PAY ATTENTION TO EXTENSION

checklist = [f for f in glob.glob(checkthis+"**/*.bmp")]
movementlist = [m for m in glob.glob(movement+"**/*.jpg")]

checkIFDEAD = [m for m in glob.glob(checkDEAD+"**/*.bmp")]
checkIFENTER = [z for z in glob.glob(checkENTER+"**/*.bmp")]
checkIFDISMANTLE = [e for e in glob.glob(checkDISMANTLE+"**/*.bmp")]



#checkIFDEAD = [m for m in glob.glob(checkDEAD+"**/*.bmp")]

print(checklist)


# x = pyautogui.click(935, 473, button='right')
# y = pyautogui.click(934, 561, button='right')
# z = pyautogui.click(1000, 530, button='right')
# c = pyautogui.click(870, 519, button='right')
# test_list = [1, 2, 3, 4]
# random_num = random.choice(test_list)
# if random_num == 1:
#     z

count = 0
restart=0
while (count < 9):
    for m in movementlist:
        #focus_window('LOST ARK')
        restart += 1
        print("program finished loop for " + str(restart) + "th time")
        for f in checklist:
            focus_window('LOST ARK')
            #pyautogui.dragTo(1280, 436,0.6, button='left')
           # focus_window('LOST ARK')
            #print('finished')
            #imagesearch_numLoop(f, 0.5, 2, 0.9)
            StateCHECKimg(1)
            #ENTERstage()
           # Click_on_Image(f, 'left', 2, 1)
        #Midlescreen_Circle_rightclick()
        #Skills_no_movement(23)
        #DismantleBalls()
        #DO NOT FORGET TO DEBUG CHANGING KEYBOARD TO RUSSIAN FUKS the program
        #Grabimage_text()
        # pos = imagesearch_numLoop(m, 0.1, 1, 0.9)
        # #print(m)r
        # #print(path.basename(f)[0])
        # if pos[0] != -1:
        #      pyautogui.press('g')
        #     #
        #     # PressKey_image(f)
        #     # pyautogui.press('f1')




