import os
import random
import pydirectinput
import pyautogui
import time
import threading
from threading import Thread
import dill
import glob
import concurrent.futures
import keyboard
import signal
from multiprocessing.managers import NamespaceProxy, BaseManager
import multiprocessing
import inspect
from multiprocessing import Manager, Process, Pool

import logging

logging.basicConfig(level=logging.INFO)

from METHODS_OLD_BACKUP import imagesearch
from METHODS_OLD_BACKUP import Searchimage_return_position
from lookforLOSTARK import Click_on_Image
from METHODS_OLD_BACKUP import searchimageinarea
from METHODS_OLD_BACKUP import imagesearch_fast_area
from METHODS import image2text
from FINDWINDOW import WindowMgr

# images
ginteraction = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\Ginteraction.png"

# random numbers
randomnumber = random.randint(1, 5)  # Integer from 1 to 10, endpoints included
randomnumber1 = random.randint(1, 6)
randomfloat = random.uniform(0.2, 1)

attack = ['w', 'f']
defense = ['d', 'e']

randomjump = ['r', 'a']
randomATTACK = random.sample(attack, 1)
randomDEFENSE = random.sample(defense, 1)

HOLD = 2.3  # seconds
count = 0
combo = 0.4
combos = 0.5

Resolution = [2560, 1080]
playerMinimap = [Resolution[0] / 100 * 93.04,
                 Resolution[1] / 100 * 15.46]

# move to center
pydirectinput.moveTo(round(Resolution[0] / 100 * 50),
                     round(Resolution[1] / 100 * 50))

x1 = 100
y1 = 150

x2 = 50
y2 = 200

MiniMCOORD = [round(Resolution[0] / 100 * 87.25),
              round(Resolution[1] / 100 * 3.75),
              round(Resolution[0] / 8.7),
              round(Resolution[1] / 4.25)]

x = [x2 - x1, y2 - y1]

HorMin = Resolution[0] / 100 * 48
HorMax = Resolution[0] / 100 * 51

VerMin = Resolution[1] / 100 * 34
VerMax = Resolution[1] / 100 * 50

panchor = [round(Resolution[0] / 2),
           round(Resolution[1] / 2)]

movetodelay = 0.3

txtfiles = []
for file in glob.glob("*.bmp"):
    txtfiles.append(file)

Buttons = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\"

CDung = Buttons + "ChaosDungeon"
Dead = Buttons + "Dead"
passing = Buttons + "Passing"
ReENTER = Buttons + "ReENTER"
Portal_no_mini = Buttons + "PortalNoMinimap"
Minimap = Buttons + "Minimap"
stage_clear = Buttons + "CheckIFclear"

ChaosDung = [m for m in glob.glob(CDung + "**/*.png")]

checkIFDEAD = [m for m in glob.glob(Dead + "**/*.png")]
check_if_clear = [m for m in glob.glob(stage_clear + "/*.png")]

restart_chaos = [m for m in glob.glob(stage_clear + "\\Cleared" + "**/*.png")]

passingthrough = [m for m in glob.glob(passing + "**/*.png")]
ReENTERing = [m for m in glob.glob(ReENTER + "**/*.png")]
PortalNOMINI = [m for m in glob.glob(Portal_no_mini + "**/*.png")]
# SUPER NOTE "**/*.png" WILL CHECK DIRECTORIES AS WELL , But /*.png only checks inside specified one
minimap_dir = [m for m in glob.glob(Minimap + "/*.png")]
minimap_red = [m for m in glob.glob(Minimap + "\\Red" + "/*.png")]

global skills_dict
# SCRAPPER
skills_dict = {'s': 4,
               'w': 8,
               'a': 15,
               'q': 5,
               'e': 6,
               'f': 7,
               'd': 3,
               'r': 11}

# skills_dict = {'z': 9,
#                'f': 10,
#                'q': 15,
#                'r': 12,
#                'e': 8,
#                's': 14,
#                'd': 7,
#                'w': 6}

# pydirectinput.moveTo(randomPOSITION)
# pyautogui.moveTo(randomPOSITION, movetodelay, pyautogui.easeOutQuad)
# pydirectinput.moveTo(randomPOSITION, 0.4)


# tasks = multiprocessing.JoinableQueue()
# result_q = multiprocessing.Queue()


# ULTRA IMPORTANT FOR DEBUGGING !!!!!!!!!!!
# def killthemall():
#     time.sleep(1)
#     print("killing all and these are normal:", normal_processes)
#     for process in all_processes:
#         process.terminate()
#         process.join()


# keyboard.add_hotkey('ctrl+shift+q', killthemall)


def h4h4():
    x = random.randrange(round(HorMin), round(HorMax), 7)
    y = random.randrange(round(VerMin), round(VerMax), 4)
    pydirectinput.moveTo(x, y, 0.1)


def combo_skill(keybind, numberofcombos, delay):
    for number in range(numberofcombos):
        pydirectinput.press(keybind)
        time.sleep(delay)


def no_combat():
    time.sleep(1)
    print("terminating COMBAT proc", combat_processes)
    for process in combat_processes:
        process.terminate()
        process.join()


def no_normal(*args):
    time.sleep(1)
    print("terminating NORMAL proc", normal_processes)
    for process in normal_processes:
        print(process)
        process.terminate()
        process.kill()
        process.join()


def reset(*args):
    # print("killing combat :", combat_processes)
    print("stopping combat")
    for process in combat_processes:
        # if process is not None:
        print(process)
        process.terminate()
        process.kill()
        process.join()


def kill_all(*args):
    print("KILLING ALL")
    time.sleep(1)
    for process in all_processes:
        process.terminate()
        process.kill()
        process.join()
    exit()
    os._exit(0)


def repair_and_enter():
    repair_gear = 'C:\\Users\\Ggjustice\\Pictures\\Buttons\\ChaosMisc\\Repair_gear.png'
    leave = 'C:\\Users\\Ggjustice\\Pictures\\Buttons\\ChaosMisc\\Leave.png'
    ok_button = 'C:\\Users\\Ggjustice\\Pictures\\Buttons\\ChaosMisc\\ok_button.png'
    repair_all = 'C:\\Users\\Ggjustice\\Pictures\\Buttons\\ChaosMisc\\Repair all.png'

    position = imagesearch_fast_area(repair_gear, precision=0.7)
    print("Checking stage status", position)
    if position != [-1, -1]:
        pydirectinput.press('/')
        time.sleep(4)
        Click_on_Image(leave, "left", 1, 1, offset=5)
        time.sleep(1)
        Click_on_Image(ok_button, "left", 1, 1, offset=5)
        time.sleep(40)  # loading screen
        pydirectinput.press('g')
        time.sleep(2)
        Click_on_Image(repair_all, "left", 1, 1, offset=5)
        time.sleep(1)
        pydirectinput.press('ESC')
        time.sleep(1)
        pydirectinput.keyDown('alt')
        time.sleep(0.3)
        pydirectinput.press('q')
        time.sleep(0.2)
        pydirectinput.keyUp('alt')
        time.sleep(1)
        pydirectinput.leftClick(1200, 290)
        time.sleep(1)
        pydirectinput.leftClick(1900, 860)
        time.sleep(1)
        pydirectinput.leftClick(1225, 605)
        time.sleep(1)


def state_check(normal_processes, combat_processes, switch):
    # print("i was here")
    while True:
        for y in check_if_clear:
            position = imagesearch_fast_area(y, precision=0.7)
            print("Checking stage status", position)
            if position != [-1, -1]:
                pydirectinput.press('/')
                time.sleep(2)
                pydirectinput.press(';')
                time.sleep(2)
                for u in restart_chaos:
                    time.sleep(2)
                    Click_on_Image(u, "left", 1, 1, offset=5)
                    time.sleep(0.5)
                switch.append("On")
                print("APPENDED switch to ", switch)
                # add loading screen function
                time.sleep(10)
        repair_and_enter()
        for x in checkIFDEAD:
            position = Click_on_Image(x, "left", 1, 1, offset=5)
            print("checked if dead", position)
            time.sleep(2)
            if position == [-1, -1]:
                time.sleep(10)
                print("still alive and switch is", switch)
            else:
                pydirectinput.press('/')
                time.sleep(2)
                Click_on_Image(x, "left", 1, 1, offset=5)
                switch.append("On")
                print("APPENDED switch to ", switch)
                time.sleep(1)
            for y in ReENTERing:
                position = Click_on_Image(y, "right", 1, 1, offset=5)
            # check if timer is 0 then enter chaos
            # CHeck if need to repair
    return "Unlucky"


def process_search(search):
    # found_at = [(MiniMCOORD[0] + search[0]),
    #             (MiniMCOORD[1] + search[1])]

    found_at = search
    distance = [found_at[0] - playerMinimap[0],
                found_at[1] - playerMinimap[1]]

    ps_x1 = round(panchor[0] + (distance[0])) * 1
    ps_y1 = round(panchor[1] + (distance[1])) * 1
    # print("Distance is :", distance)
    # print(ps_x1, ps_y1)
    return ps_x1, ps_y1


def minimap_detection(switch):
    count_occurrance = 0
    while True:
        print("DOING MINIMAP")
        # print("starting MINIMAP_detect and switch is:", switch)
        movementdelay = 0.4
        countingportattempt = 0
        for g in minimap_dir:
            if "Boss" in g:
                looking_for = "Boss"
            elif "Portal" in g:
                looking_for = "Portal"
            elif "Elite" in g:
                looking_for = "Elite"
            elif "Tower" in g:
                looking_for = "Tower"
            # Get last 10 character
            # last_chars = g[-20:]
            split_string = g.rsplit('\\')[6]
            # print(split_string)
            # print(g)
            count_occurrance = count_occurrance + 1
            occurances = str(count_occurrance) + str(split_string)
            # MINIMAP Searching
            search = searchimageinarea(g, occurances, looking_for,
                                       x1=MiniMCOORD[0], y1=MiniMCOORD[1],
                                       x2=MiniMCOORD[2], y2=MiniMCOORD[3], precision=0.65)
            # print(count_occurrance, search, g)

            if search == [-1, -1] or None:
                # print("NOT FOUND 0 " + split_string)
                pydirectinput.mouseDown(button="right")
                time.sleep(movementdelay)
                pydirectinput.mouseUp(button="right")
            else:
                # MINIMAP Processing
                x1, y1 = process_search(search)
                # print(x1, y1)
                if "Boss" in g:
                    print("found BOSS")
                    pydirectinput.mouseDown(x1, y1, button="right")
                    time.sleep(movementdelay)
                    pydirectinput.mouseUp(button="right")
                    time.sleep(movementdelay)
                    pydirectinput.press("SPACE")
                    time.sleep(0.1)
                    pydirectinput.press("SPACE")
                    time.sleep(0.1)
                    pydirectinput.press("v")
                    time.sleep(movementdelay)
                    pydirectinput.press("v")
                    # wait for image if image th
                    # press g
                if "Portal" in g:
                    print("PORTAL PART STARTED")
                    break_switch = 0
                    while break_switch != 1:
                        for p in passingthrough:
                            pydirectinput.press("/")  # stopping combat
                            # icount = 0
                            port_pos = Searchimage_return_position(p, precision=0.7)
                            # for u in PortalNOMINI:
                            #     port_pos = Searchimage_return_position(u, 0.2, 1)
                            # print(port_pos)
                            print("HERE I AM")
                            if port_pos != [-1, -1]:
                                print("Entering portal")
                                pydirectinput.mouseUp()
                                time.sleep(2)
                                pydirectinput.rightClick()
                                print("pressed G")
                                pydirectinput.press("g")
                                time.sleep(1)
                                # SWITCH TURNED ON
                                switch.append("On")
                                time.sleep(7)
                                break_switch = 1
                                break
                            for i in range(0, 2, 1):
                                # Counts attempts it tried to enter in portal
                                countingportattempt = countingportattempt + 1
                                fportal = (countingportattempt, " Found portal")
                                search = searchimageinarea(g, str(fportal), look_for=looking_for,
                                                           x1=MiniMCOORD[0], y1=MiniMCOORD[1],
                                                           x2=MiniMCOORD[2], y2=MiniMCOORD[3], precision=0.7)
                                print("Searching for portal", search)
                                # print(MiniMCOORD[0], MiniMCOORD[1])
                                if search != [-1, -1]:
                                    x1, y1 = process_search(search)
                                    print("Found portal on MINIMAP going in that direction: ", x1, y1)
                                    pydirectinput.press("SPACE")
                                    time.sleep(0.1)
                                    pydirectinput.press("SPACE")
                                    time.sleep(0.1)
                                    pydirectinput.mouseDown(x1, y1, button="right")
                                    time.sleep(0.1)
                                    pydirectinput.mouseDown(button="right")
                                    # pydirectinput.press("g")
                                    time.sleep(1)
                                    pydirectinput.mouseUp(button="right")
                                    pydirectinput.mouseUp(button="left")
                                if countingportattempt >= 2:
                                    print("Random movement", search)
                                    pydirectinput.mouseDown(x1, y1, button="right")
                                    time.sleep(movementdelay)
                                    pydirectinput.mouseUp(button="right")
                                if countingportattempt >= 14:
                                    break_switch = 1
                                    break

        for f in minimap_red:
            # print("Doing reds ", f)
            split_string = f.rsplit('\\')[6]
            count_occurrance = count_occurrance + 1
            occurances = str(count_occurrance) + str(split_string)

            search = searchimageinarea(f, occurances, look_for="Red",
                                       x1=MiniMCOORD[0], y1=MiniMCOORD[1],
                                       x2=MiniMCOORD[2], y2=MiniMCOORD[3], precision=0.6)

            if search != [-1, -1]:
                x1, y1 = process_search(search)
                print("Found red", x1, y1)
                pydirectinput.mouseDown(x1, y1, button="right")
                time.sleep(movementdelay)
                pydirectinput.mouseUp(button="right")
                break


def centeral_detection(switch):
    count_occurrance = 0
    movementdelay = 0.4
    while True:
        count_occurrance = 0
        movementdelay = 0.4
        for g in ChaosDung:
            # Get last 10 character
            # last_chars = g[-20:]
            split_string = g.rsplit('\\')[6]
            # print(split_string)
            startx = round(Resolution[0] / 100 * 16)
            starty = round(Resolution[1] / 100 * 1)
            count_occurrance = count_occurrance + 1
            occurances = str(count_occurrance) + str(split_string)
            # print(g)
            # RESOLUTION Searching
            search = searchimageinarea(g, occurances, look_for="HPbar", precision=0.86,
                                       x1=startx, y1=starty, y2=round(Resolution[1] / 100 * 83))  # - 180)

            if search == [-1, -1] or search is None:
                123
                # print("NOT FOUND 0 " + split_string)
                # pydirectinput.mouseDown(button="right")
                # time.sleep(movementdelay)
                # pydirectinput.mouseUp(button="right")
            else:
                # print("Found HPbar ", split_string)
                x1 = round(search[0])
                y1 = round(search[1])
                # print(x1, y1)
                pydirectinput.moveTo(x1, y1)
                time.sleep(0.4)

                if "PORT" in g:
                    countingportattempt = 0
                    break_switch = 0

                # if "BOSS" in g:
                #     print("found BOSS")
                #     pydirectinput.mouseDown(x1, y1, button="right")
                #     time.sleep(movementdelay)
                #     pydirectinput.mouseUp(button="right")
                #     time.sleep(movementdelay)
                #     pydirectinput.press("v")
                #     time.sleep(1)
                #     pydirectinput.press("v")
                #     # wait for image if image there
                #     # press g
                # else:
                #     # clicking in that direction
                #     # print("moving as USUAL")
                #     pydirectinput.moveTo(x1, y1)
                #     time.sleep(movementdelay)
                # pydirectinput.mouseUp(button="right")


def skills(key):
    pydirectinput.press('F1')
    minutes = 5
    numbofskills = round(minutes * 60 / skills_dict[key])
    pydirectinput.mouseDown()
    for i in range(0, numbofskills, 1):
        # time.sleep(0.4)
        # logging.debug(("Skill cast:" + key))
        pydirectinput.mouseUp()
        pydirectinput.press('' + key)
        time.sleep(0.2)
        pydirectinput.press('' + key)
        time.sleep(skills_dict[key])
        pydirectinput.mouseDown()


def combat(np, cp, manager):
    # print(self.Skillsdict)
    print("starting combat")
    for key in skills_dict:
        # print("finished ", key)
        print(key)
        process1 = manager.Process(target=skills, args=key)
        process1.start()
        combat_processes.append(process1)
        time.sleep(1)
        all_processes.append(process1)
    # print("printing ALL", all_processes)


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


if __name__ == '__main__':
    keyboard.add_hotkey('ctrl+shift+q', kill_all)
    keyboard.add_hotkey('ctrl+shift+w', reset)
    keyboard.add_hotkey('ctrl+shift+e', no_normal)

    focus_window('LOST ARK')
    listmanager = Manager()
    normal_processes = listmanager.list()
    combat_processes = listmanager.list()
    all_processes = listmanager.list()
    switch = listmanager.list()
    repair_switch = listmanager.list()

    BaseManager.register('Process', Process, ProcessProxy, exposed=tuple(dir(ProcessProxy)))
    manager = BaseManager()
    manager.start()

    proc_state_check = manager.Process(target=state_check,
                                       args=(normal_processes, combat_processes, switch))
    central_detectors = manager.Process(target=centeral_detection,
                                        args=(repair_switch, ))
    minimap_detections = manager.Process(target=minimap_detection,
                                         args=(repair_switch,))

    # APPENDING
    all_processes.append(proc_state_check)

    combat_processes.append(central_detectors)
    all_processes.append(central_detectors)

    normal_processes.append(minimap_detections)
    all_processes.append(minimap_detections)
    print(switch)

    central_detectors.start()
    minimap_detections.start()

    for key in skills_dict:
        # print("finished ", key)
        print(key)
        process1 = manager.Process(target=skills, args=key)
        process1.start()
        combat_processes.append(process1)
        time.sleep(1)
        all_processes.append(process1)
    # START/JOIN
    time.sleep(4)
    proc_state_check.start()
    # proc_state_check.join()
    # proc_move.join()

    while True:
        # print("Switch is :", switch)
        time.sleep(3)
        if 'On' in switch:
            print("SWITCH IS", switch, "RESTARTING COMBAT and HPbars", normal_processes)
            for key in skills_dict:
                # print("finished ", key)
                print(key)
                process1 = manager.Process(target=skills, args=key)
                process1.start()
                combat_processes.append(process1)
                time.sleep(1)
                all_processes.append(process1)

            central_detectors = manager.Process(target=centeral_detection,
                                                args=(switch,))
            central_detectors.start()
            combat_processes.append(central_detectors)
            all_processes.append(central_detectors)

            switch[:] = []

    # keyboard.add_hotkey('*', nonormalplz)
    # combat_processes = Manager().list()
    # N O T E S
    # https://stackoverflow.com/questions/25620211/multiprocessing-passing-an-array-of-dicts-through-shared-memory
    # all_processes, combat_processes, normal_processes = cproc = p.combat()

    # print("normal processes : ", normal_processes)
    # print("combat processes : ", combat_processes)
    # print("all processes : ", all_processes)

