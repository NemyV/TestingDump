import pyautogui

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
import timeit


EpicPath = "E:\\Lost ark serious\\Lost ark buttons\\"

# EpicPath = "E:\\Lost ark serious\\Lost ark buttons\\1280x1024\\"  #UN-COMMENT for 1280x1024

DisDetInv = EpicPath + 'DISMANTLE\\Detect inventory.png'

PosDisBtn= imagesearch_numLoop(DisDetInv, 0.1, 7)

# print(PosDisBtn)
EpicPath = "E:\\Lost ark serious\\Lost ark buttons\\"
LASkills = EpicPath + 'LA skills'
#Screenshot_1.jpg #Hp bar left corner.png
HPbarLeft = r"E:\Lost ark serious\Lost ark buttons\LA skills\Hp bar left corner.png"
test1 = r"E:\Lost ark serious\Lost ark buttons\LA skills\Screenshot_1.png"



Topleftx = Window.WindowCoordArr[0]
Toplefty = Window.WindowCoordArr[1]
WIDTH = Window.WindowCoordArr[2]
HEIGHT = Window.WindowCoordArr[3]
print("madness shits")
print ( Topleftx,
Toplefty,
HEIGHT,
WIDTH)
# print("looking for")
# print("finished")
pyautogui.screenshot('123Fullscreenshot.png', region=(Topleftx, Toplefty, WIDTH*4/10, HEIGHT))

# startval = PositionHP[0] #1060, 844
# endvalue = PositionHP[1]
# posx = startval[0]
# posy = startval[1]
posxEND = 240
posyEND = 100
#
# print(posx, posy)
# #pyautogui.screenshot('145845t.png', region=(posx, posy, posxEND, posyEND))
# print(PositionHP)
# #TESTING images
# # img = cv2.imread(HPbarLeft, 0)
# # cv2.imshow('what a bich', img)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
#
# im = pyautogui.screenshot('my_screenshot.png', region=(posx, posy, posxEND, posyEND))
#
# returntest = imagesearch_region_loop(test1, 0.1, posx, posy, posxEND, posyEND,0.5)
# #foundPOSITIONoftheIMAGe = [posx+returntest[0], posy+returntest[1]]
#
# print(returntest)
# #print(foundPOSITIONoftheIMAGe)
# #Click_on_Image(f, 'left', 1)
# print(posx, posy)
#Click_on_Image_inside_region(test1, 680, 850, posxEND, posyEND, 1)

#TESTING Speed of
def a():
    imagesearcharea(test1, 680, 850, posxEND, posyEND)
    #Click_on_Image_inside_region(test1, 680, 850, posxEND, posyEND, 1)

def b():
    imagesearch_numLoop(test1, 0.5, 2)
    #Click_on_Image(test1, 'left', 1)

ChargeDuration = 2
Comboskill = 3
#Prioirity of skills  = >  waiting when skill is ready





# #Testing
# print("this is timeit A :")
# print(timeit.timeit((a), number=5))
#
# print("this is timeit B :")
# print(timeit.timeit((b), number=5))
#
# time.sleep(0.5)
# form.send_keystrokes('')
# win32api.SetCursorPos((foundPOSITIONoftheIMAGe[0], foundPOSITIONoftheIMAGe[1]))
# click(foundPOSITIONoftheIMAGe[0], foundPOSITIONoftheIMAGe[1], 'right')
# time.sleep(1)

#print("this is lol")
#print(returntest)


