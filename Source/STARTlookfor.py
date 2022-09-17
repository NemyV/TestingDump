
import sys
sys.path.insert(0, 'E:\Hello wolrd Python\LOSTARKB')

from Testing.LostARKFOCUS import checkIFDEAD
from Testing.LostARKFOCUS import checklist
from Testing.LostARKFOCUS import focus_window
from Testing.LostARKFOCUS import Skills_no_movement

GlobalLabel= ''
# t1 = threading.Thread(target=self.Loadbuttons)
#         t2 = threading.Thread(target=self.my_callback)
#         t1.start()
#         t2.start()
#         t1.join()
#         t2.join()
# def startlookfor(randomarg):
restart = 0
count = 0
#     randomarg
#     GlobalLabel=''

LA = "LOST ARK"
def startlookfor():
    restart = 0
    count = 0
    while (count < 9):
        for m in checkIFDEAD:
            # focus_window('LOST ARK')
            restart += 1
            print("program finished loop for " + str(restart) + "th time")
            for f in checklist:
                focus_window('LOST ARK ')
                # show_rand_app()
                # pyautogui.dragTo(1280, 436,0.6, button='left')
                # focus_window('LOST ARK')
                # Application().connect(LA)
                print('finished')
                # imagesearch_numLoop(f, 0.5, 2, 0.9)
                # t1 = threading.Thread(target=Skills_no_movement(23))
                # t1.start()
                # t1.join()
                # x.start()
                #StateCHECKimg(1)
                # ENTERstage()
                # Fishing()
                # Click_on_Image(f, 'left', 2, 1)
                # Midlescreen_Circle_rightclick()
                Skills_no_movement(23)
                # DismantleBalls()
                # DO NOT FORGET TO DEBUG CHANGING KEYBOARD TO RUSSIAN FUKS the program
                # Grabimage_text()
                # pos = imagesearch_numLoop(m, 0.1, 1, 0.9)
                # #print(m)r
                # #print(path.basename(f)[0])
                # if pos[0] != -1:
                #      pyautogui.press('g')
                #     #
                #     # PressKey_image(f)
                #     # pyautogui.press('f1'

#startlookfor()
# app = Application().connect(LA)
# dlg = app['Untitled - Notepad']
# dlg.print_control_identifiers()
#
# while (count < 9):
#     for m in checkIFDEAD:
#         # focus_window('LOST ARK')
#         restart += 1
#         GlobalLabel = ("program finished loop for " + str(restart) + "th time")
#         for f in checklist:
#             focus_window('LOST ARK ')
#             #show_rand_app()
#             # pyautogui.dragTo(1280, 436,0.6, button='left')
#             # focus_window('LOST ARK')
#             #Application().connect(LA)
#             print('finished')
#             # imagesearch_numLoop(f, 0.5, 2, 0.9)
#             # t1 = threading.Thread(target=Skills_no_movement(23))
#             # t1.start()
#             # t1.join()
#             # x.start()
#             StateCHECKimg(1)
#             # ENTERstage()
#             # Fishing()
#             # Click_on_Image(f, 'left', 2, 1)
#             # Midlescreen_Circle_rightclick()
#             #Skills_no_movement(23)
#             # DismantleBalls()
#             # DO NOT FORGET TO DEBUG CHANGING KEYBOARD TO RUSSIAN FUKS the program
#             # Grabimage_text()
#             # pos = imagesearch_numLoop(m, 0.1, 1, 0.9)
#             # #print(m)r
#             # #print(path.basename(f)[0])
#             # if pos[0] != -1:
#             #      pyautogui.press('g')
#             #     #
#             #     # PressKey_image(f)
#             #     # pyautogui.press('f1'
