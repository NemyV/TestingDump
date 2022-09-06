
import pydirectinput
from METHODS_OLD_BACKUP import imagesearch
from METHODS_OLD_BACKUP import searchimageinarea
from METHODS_OLD_BACKUP import imagesearch_fast_area
import time
import glob
import datetime

Buttons = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\"

FishingCATCH = Buttons + 'FISHING\\EXCLAMATION'
repair = Buttons + 'FISHING\\BrokenTool'
lifeskills = Buttons + 'FISHING\\OPENSkills'
energy = Buttons + 'FISHING\\Noenergy'
fishing_mini = Buttons + 'FISHING\\Minigame'

Fishing_minigame = [x for x in glob.glob(fishing_mini + "**/*.png")]
FINDFishingCATCH = [x for x in glob.glob(FishingCATCH + "**/*.png")]
repaircheck = [x for x in glob.glob(repair + "**/*.png")]
Lifeskillopen = [x for x in glob.glob(lifeskills + "**/*.png")]
Emptyenergy = [x for x in glob.glob(energy + "**/*.png")]

Resolution = [2560, 1080]

x1 = round(Resolution[0]*46.7/100)
y1 = round(Resolution[1]*38.9/100)

x2 = round(Resolution[0]*52.73/100)
y2 = round(Resolution[1]*57/100)
start = time.time()


def Statecheck():
    for f in repaircheck:
        print(f)
        pos = searchimageinarea(f, "fishingtest",
                                x1=round(Resolution[0]*74.2/100), y1=round(Resolution[0]*0.46/100),
                                x2=round(Resolution[0]*84.7/100), y2=round(Resolution[1]*14.9/100))
        time.sleep(0.7)
        print(pos)
        if pos != [-1, -1]:
            print("FOUND MARK")
            pydirectinput.press('8')
            time.sleep(40)
            pydirectinput.press('g')
            time.sleep(1)
            pydirectinput.click(round(Resolution[0]*50.94/100),
                                round(Resolution[1]*78.7/100))
            time.sleep(1)
            pydirectinput.click()
            time.sleep(1)
            pydirectinput.click(round(Resolution[0]*41/100),
                                round(Resolution[1]*76/100))
            time.sleep(1)
            pydirectinput.click(round(Resolution[0]*48.1/100),
                                round(Resolution[1]*58/100))
            time.sleep(1)
            pydirectinput.press('ESC')
            time.sleep(1)
            pydirectinput.press('9')
            time.sleep(20)

    for f in Lifeskillopen:
        print(f)
        time.sleep(2.5)
        pos = searchimageinarea(f, "fishing-test",
                                x1=x1-20, y1=900, x2=250, y2=50
                                , precision=0.5)
        print("Life skill bar pos: ", pos)
        while pos == [-1, -1]:
            print("Opening skills bar")
            time.sleep(2.5)
            pydirectinput.press('b')
            pos = searchimageinarea(f, "fishing-test", x1=x1-20, y1=900, x2=250, y2=50
                                    , precision=0.5)


def fishing():
    count_good = 0
    while True:
        Statecheck()

        for f in Emptyenergy:
            print(f)
            pos = searchimageinarea(f, "fishing-test", precision=0.9)
            time.sleep(0.7)
            print(pos)
            if pos != [-1, -1]:
                print("No energy! Quiting...")
                end = time.time()
                print(f"Runtime of the program is {end - start}")
                # after quiting reloging into the other account and doing the same thing....

                # pydirectinput.press('narakabladepoint10000')
                # pydirectinput.press('grimreaper0')

                # pydirectinput.press('jibrillev')
                # pydirectinput.press('Rally901121!')
                time.sleep(1)
                exit()
        # cast W at position START
        time.sleep(1)
        # # right side
        # pydirectinput.moveTo(round(Resolution[0]*58.5/100),
        #                      round(Resolution[1]*59.4/100))
        # left side
        print("moving the mouse")
        pydirectinput.moveTo(round(Resolution[0] * 32 / 100),
                             round(Resolution[1] * 55.5 / 100))
        time.sleep(1)
        # Casting fishing buff
        # pydirectinput.press('f')
        # time.sleep(2.4)
        # Check if you can cast NET/Possibly same as normal one with priority of finding net
        net = Buttons + 'Fishing\\Minigame\\Net_throwing.png'
        pos = imagesearch_fast_area(net, x1=x1-250, y1=y1+530, x2=300, y2=130,
                                    precision=0.7)
        print("Net throwing Postiong", pos)
        # pydirectinput.moveTo(int(pos[0]),int(pos[1]))
        if pos == [-1, -1]:
            pydirectinput.press('w')
            time.sleep(8.5)
        else:
            pydirectinput.press('r')
            time.sleep(4)
            perfect_mini = Buttons + 'Fishing\\Minigame\\Perfect2.png'
            start_time = time.time()
            for i in range(0, 60, 1):
                pos = imagesearch_fast_area(perfect_mini, precision=0.55, x1=415, y1=110, x2=690, y2=690)
                # pos = imagesearch(perfect_mini, 0.65)
                print(pos)
                if pos != [-1, -1]:
                    print("Playing mini game!!! pressed 3")
                    pydirectinput.press('SPACE', presses=3)
                    count_good = count_good+1
                # end_time = time.time()
                # result = end_time - start_time
                # if result >= 2:
                #     print("result is 2")
                #     pydirectinput.press('SPACE', presses=10, interval=0.2)
                #     start_time = time.time()
        # If you want to cast buffs
        # for f in FishingBUFFS:
        # search for exclamation mark
        for f in FINDFishingCATCH:
            # search for exclamation mark
            #time.sleep(5)
            print(f)
            # pos = imagesearch_loop(f, 0.1)
            #pos = imagesearch_region_loop(f, x1, y1, x2, y2, 0.5)
            pos = searchimageinarea(f, str(count_good), x1=x1, y1=y1, x2=x2-x1, y2=y2-y1, precision=0.8)
            time.sleep(0.5)
            print(pos)
            if pos != [-1, -1]:
                count_good = count_good + 1
                print("FOUND MARK")
                pydirectinput.press('w')
                time.sleep(6)
                break

        print("finished fishing loop")
    print("Had this many net games finished:", count_good)
