import pydirectinput
import METHODS
import time


def Statecheck():
    for f in METHODS.repaircheck:
        print(f)
        pos = METHODS.im_processing(f,
                                    x1=round(METHODS.Resolution[0] * 74.2 / 100),
                                    y1=round(METHODS.Resolution[0] * 0.46 / 100),
                                    x2=round(METHODS.Resolution[0] * 84.7 / 100),
                                    y2=round(METHODS.Resolution[1] * 14.9 / 100))
        time.sleep(0.7)
        print(pos)
        if pos != [-1, -1]:
            print("FOUND MARK")
            pydirectinput.press('8')
            time.sleep(40)
            pydirectinput.press('g')
            time.sleep(1)
            pydirectinput.click(round(METHODS.Resolution[0] * 50.94 / 100),
                                round(METHODS.Resolution[1] * 78.7 / 100))
            time.sleep(1)
            pydirectinput.click()
            time.sleep(1)
            pydirectinput.click(round(METHODS.Resolution[0] * 41 / 100),
                                round(METHODS.Resolution[1] * 76 / 100))
            time.sleep(1)
            pydirectinput.click(round(METHODS.Resolution[0] * 48.1 / 100),
                                round(METHODS.Resolution[1] * 58 / 100))
            time.sleep(1)
            pydirectinput.press('ESC')
            time.sleep(1)
            pydirectinput.press('9')
            time.sleep(20)
    while pos == [-1, -1]:
        for f in METHODS.Lifeskillopen:
            print(f)
            METHODS.focus_window('LOST ARK')
            time.sleep(2.5)
            pos = METHODS.im_search(f, x1=round(METHODS.Resolution[0] * 44 / 100),
                                    y1=round(METHODS.Resolution[1] * 83.5 / 100),
                                    x2=round(METHODS.Resolution[0] * 11 / 100),
                                    y2=round(METHODS.Resolution[0] * 7 / 100), precision=0.5)
            if pos != [-1, -1]:
                break
            print("Opening skills bar")
            pydirectinput.press('b')
            print("Life skill bar pos: ", pos)


def fishing():
    count_good = 0
    switch = 0
    x1 = round(METHODS.Resolution[0] * 45.7 / 100)
    y1 = round(METHODS.Resolution[1] * 37.7 / 100)

    x2 = round(METHODS.Resolution[0] * 52.73 / 100)
    y2 = round(METHODS.Resolution[1] * 57 / 100)
    start = time.time()
    while switch == 0:
        Statecheck()

        for f in METHODS.Emptyenergy:
            print(f)
            pos = METHODS.im_search(f, precision=0.9)
            time.sleep(0.7)
            print(pos)
            if pos != [-1, -1]:
                print("No energy! Quiting...")
                # after quiting reloging into the other account and doing the same thing....
                switch = 1
                # exit()
        # cast W at position START
        time.sleep(1)
        # # right side
        # pydirectinput.moveTo(round(METHODS.Resolution[0]*58.5/100),
        #                      round(METHODS.Resolution[1]*59.4/100))
        # left side
        print("moving the mouse")
        pydirectinput.moveTo(round(METHODS.Resolution[0] * 32 / 100),
                             round(METHODS.Resolution[1] * 55.5 / 100))
        time.sleep(1)
        # Casting fishing buff
        # pydirectinput.press('f')
        # time.sleep(2.4)
        # Check if you can cast NET/Possibly same as normal one with priority of finding net
        net = METHODS.Buttons + 'Fishing\\Minigame\\Net_throwing.png'
        pos = METHODS.im_search(net, x1=x1 - 250, y1=y1 + 530, x2=300, y2=130, precision=0.7)
        print("Net throwing Postiong", pos)
        # pydirectinput.moveTo(int(pos[0]),int(pos[1]))
        if pos == [-1, -1]:
            pydirectinput.press('w')
            time.sleep(7.8)
        else:
            pydirectinput.press('r')
            time.sleep(4)
            perfect_mini = METHODS.Buttons + 'Fishing\\Minigame\\Perfect2.png'
            start_time = time.time()
            for i in range(0, 60, 1):
                pos = METHODS.im_search(perfect_mini, precision=0.55, x1=415, y1=110, x2=690, y2=690)
                print(pos)
                if pos != [-1, -1]:
                    print("Playing mini game!!! pressed 7")
                    pydirectinput.press('SPACE', presses=9)
                    count_good = count_good + 1
                # end_time = time.time()
                # result = end_time - start_time
                # if result >= 2:
                #     print("result is 2")
                #     pydirectinput.press('SPACE', presses=10, interval=0.2)
                #     start_time = time.time()
        # If you want to cast buffs
        # for f in FishingBUFFS:
        # search for exclamation mark
        found = False
        for x in range(1, 9, 1):
            for f in METHODS.FINDFishingCATCH:
                # print(METHODS.Resolution)
                # search for exclamation mark
                pos = METHODS.im_search(f, x1=x1, y1=y1, x2=250, y2=300, precision=0.75)
                time.sleep(0.13)
                print(pos)
                if pos != [-1, -1]:
                    count_good = count_good + 1
                    print("FOUND MARK using:", f)
                    pydirectinput.press('w')
                    time.sleep(7)
                    found = True
                    break
            if found:
                break
        print("finished fishing loop")
    print("Had this many net games finished:", count_good)

# fishing()
