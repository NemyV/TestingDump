import multiprocessing
from threading import Thread
import keyboard
import pydirectinput
from METHODS_OLD_BACKUP import searchimageinarea
from METHODS_OLD_BACKUP import Searchimage_return_position
from METHODS import im_search_until_found
from METHODS import im_search_in_area
from METHODS import search_click_image
from METHODS import focus_window
from METHODS import image2text
from METHODS import imagesearch_fast_area
from METHODS import casting_skills
from METHODS import im_search_until_found

from kivy.config import ConfigParser
import numpy as np
import re
import pyautogui

from multiprocessing import Manager, Process, Pool
from multiprocessing.managers import NamespaceProxy, BaseManager
import inspect  # part of multiprocessing stuff

import random
import time
import glob
import os
import sys
import signal
global loading_screen_time
loading_screen_time = 30

Resolution = [2560, 1080]
panchor = [round(Resolution[0] / 2),
           round(Resolution[1] / 2)]
playerMinimap = [Resolution[0] / 100 * 93.04,
                 Resolution[1] / 100 * 15.46]
MiniMCOORD = [round(Resolution[0] / 100 * 87.25),
              round(Resolution[1] / 100 * 3.75),
              round(Resolution[0] / 8.7),
              round(Resolution[1] / 4.25)]
configparser = ConfigParser()

Buttons = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\"
Daily = Buttons + 'Daily Quest\\'

# IMPORTANT MISC [ESC MENU]
esc_menu = Daily + "Misc\\Game_menu.png"

repair = Buttons + 'FISHING\\BrokenTool'
lifeskills = Buttons + 'FISHING\\OPENSkills'
energy = Buttons + 'FISHING\\Noenergy'
repaircheck = [x for x in glob.glob(repair + "**/*.png")]
Lifeskillopen = [x for x in glob.glob(lifeskills + "**/*.png")]
Emptyenergy = [x for x in glob.glob(energy + "**/*.png")]

DailySwampLoc = Daily + 'Walling Swamp'
DailySwamp = [x for x in glob.glob(DailySwampLoc + "**/*.png")]

feiton_fail_check = Daily + 'Misc\\Feiton door'
fail_proof_faiton = [x for x in glob.glob(feiton_fail_check + "**/*.png")]
feiton_fail_check_entrence = Daily + 'Misc\\Feiton inn'
fail_proof_entrence = [x for x in glob.glob(feiton_fail_check_entrence + "**/*.png")]

hope_fail_check = Daily + 'Misc\\Hope bricks'
fail_safe_hope = [x for x in glob.glob(feiton_fail_check + "**/*.png")]
class_check = Buttons + 'Class'
Class_checker = [x for x in glob.glob(class_check + "**/*.png")]

stronghold = Daily + "Stronghold"
chosen_missions = [x for x in glob.glob(stronghold + '\\Chosen Missions' + "**/*.png")]
pet_ranch = [x for x in glob.glob(stronghold + '\\Pet Ranch' + "**/*.png")]

Weekly = Daily + "\\Weeklies"
weekly_tasks = [x for x in glob.glob(Weekly + '\\Weekly tasks' + "**/*.png")]

CDung = Buttons + "ChaosDungeon"
Dead = Buttons + "Dead"
passing = Buttons + "Passing"
ReENTER = Buttons + "ReENTER"
Portal_no_mini = Buttons + "PortalNoMinimap"
Minimap = Buttons + "Minimap"
stage_clear = Buttons + "CheckIFclear"
stage_fail = Buttons + "CheckIFclear\\Failed"

ChaosDung = [m for m in glob.glob(CDung + "**/*.png")]

checkIFDEAD = [m for m in glob.glob(Dead + "**/*.png")]
check_if_clear = [m for m in glob.glob(stage_clear + "/*.png")]
check_if_failed = [m for m in glob.glob(stage_fail + "/*.png")]

restart_chaos = [m for m in glob.glob(stage_clear + "\\Cleared" + "**/*.png")]

passingthrough = [m for m in glob.glob(passing + "**/*.png")]
ReENTERing = [m for m in glob.glob(ReENTER + "**/*.png")]
PortalNOMINI = [m for m in glob.glob(Portal_no_mini + "**/*.png")]
# SUPER NOTE "**/*.png" WILL CHECK DIRECTORIES AS WELL , But /*.png only checks inside specified one
minimap_dir = [m for m in glob.glob(Minimap + "/*.png")]
minimap_red = [m for m in glob.glob(Minimap + "\\Red" + "/*.png")]

misc_dictionary = {"loading": "no"}
process_search_inc = 2
last_cords = [0, 0]
potions_used = 0

global combat
combat = ''
global list_of_workers
list_of_workers = []
# x1 = round(Resolution[0]*46.9/100)
# y1 = round(Resolution[1]*38.9/100)
#
# x2 = round(Resolution[0]*52.73/100)
# y2 = round(Resolution[1]*57/100)
# DAILY THINGS THAT CAN BE DONE
# Ghost ship , World boss , Chaos gate , ISLAND


def daily_state_check():
    # starting time MESURING
    start = time.time()

    # TASKS -> LOGIN -> CHECKLIST ->
    switch = 0
    finished_char = []
    configparser.read("myapp.ini")
    for name, value in configparser.items("Workers"):
        if value == "yes":
            list_of_workers.append(name.capitalize())
    for name, value in configparser.items("Finished_Characters"):
        if value == "yes":
            finished_char.append(name.capitalize())
    print("WORKERS", list_of_workers)
    print("FINISHED CHAR :", finished_char)
    # list_of_workers = [ # Huge error in all mouve movement/clicks not detected all the time
    #                     # "Ggsor",  # Error because Chat was open maybe i fixed it
    #                     "Sheeeshaa",
    #                     # "Ggwarlord",  # fails to get arthentine operational shit from lopang
    #
    #                     "Pureluck",
    #                     "Ggbard",
    #                     "Gladiatrix",
    #                     "Ggdin",
    #                     # # "Stringsy", # "Sttingsy",
    #
    #                     # "Speedpuncher",
    #                     # "Artstrike",
    #                    ]


    total_tasks = 0
    total_finished = 0
    for x in list_of_workers:
        total_tasks = total_tasks + 1

    # SWITCHING TO CHAOS BUILD WHILE DOING THINGS?
    focus_window('LOST ARK')
    time.sleep(1)

    # character list
    while switch == 0:
        # Closing chat
        minimzed = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\Daily Quest\\Misc\\Chat_minimized.png"
        pos = search_click_image(minimzed, action="left",
                                 x1=0, y1=500, x2=700, y2=500, precision=0.6)
        if pos == [-1, -1]:
            minimize_chat = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\Daily Quest\\Misc\\Minimize_chat.png"
            search_click_image(minimize_chat, action="left",
                               x1=0, y1=500, x2=700, y2=500, precision=0.6)
            print("Chat minimized")
        # Opening ESC Game menu
        pydirectinput.press('ESC')
        time.sleep(0.5)
        for i in range(1, 10, 1):
            ready = Searchimage_return_position(esc_menu, 1, precision=0.84)
            if ready != [-1, -1]:
                break
            else:
                time.sleep(0.7)
                i += 1
                pydirectinput.press('ESC')
        # IMPORTANT for using 2 methods/colors to find match with tesseract
        text = image2text(x1=630, y1=655, x2=200, y2=30, method=' --oem 3 --psm 7', colors="threshold")
        found_it = False
        for y in np.unique(list_of_workers):
            if y in text:
                found_it = True
                print("FOUND IT USING THRESHOLD")
                break
        if not found_it:
            text = image2text(x1=630, y1=655, x2=200, y2=30, method=' --oem 3 --psm 7')
            for y in np.unique(list_of_workers):
                if y in text:
                    print("FOUND IT USING rgb")
                    break
        # CLOSING ESC MENU
        pydirectinput.press('ESC')
        generator_expression = (x for x in np.unique(list_of_workers) if x in text)
        for x in generator_expression:
            print("Found ", x, "")
            if x not in finished_char:
                # WHAT CLASS AM I? checking image and then XXX
                for f in Class_checker:
                    # print(f)
                    global combat
                    # Tossing at Sentinel
                    what_class = Searchimage_return_position(f, 1, precision=0.85)
                    if what_class != [-1, -1]:
                        split_string = f.rsplit('\\')[6]
                        # print(split_string)
                        print("My CLASS is " + split_string)
                        if "Bard" in split_string:
                            combat = "Bard"
                            break
                        elif split_string == "Paladin.png":
                            combat = "Paladin"
                            break
                        elif split_string == "Arcana.png":
                            combat = "Arcana"
                            break
                        elif split_string == "Lance_master.png":
                            combat = "Lance master"
                            break
                        elif split_string == "Lance_master2.png":
                            pydirectinput.press('z')
                            combat = "Lance master"
                            break
                        elif split_string == "Gunlancer.png":
                            combat = "Gunlancer"
                            break
                        elif split_string == "Sorceress.png":
                            combat = "Sorceress"
                            break
                        elif split_string == "Deathblade.png":
                            combat = "Deathblade"
                            break
                        elif split_string == "Scrapper.png":
                            combat = "Scrapper"
                            break
                        elif split_string == "Soulfist.png":
                            combat = "Soulfist"
                            break
                        elif split_string == "Artillerist.png":
                            combat = "Artillerist"
                            break
                        elif split_string == "Striker.png":
                            combat = "Striker"
                            break
                        elif split_string == "Gunslinger.png":
                            combat = "Gunslinger"
                            break
                        else:
                            print("UNKNOWN CLASS")
                            exit()
                if combat == '':
                    print("COMBAT NOT DEFINED")
                    exit()
                for section_name in configparser.sections():
                    # option = configparser.options(section_name)
                    if x == section_name:
                        work_array = []
                        for name, value in configparser.items(section_name):
                            # config_name = name
                            # config_value = value
                            if value == "yes":
                                work_array.append(name)
                        print("WORK FOR ", x, " : ", work_array)
                        gen_expression = (x for x in work_array if "all_stronghold" in x)
                        for g in gen_expression:
                            stronghold_daily()
                        gen_expression = (x for x in work_array if "preset" in x)
                        for g in gen_expression:
                            found = re.findall(r'\d+', g)
                            print("PRESET is", found)
                            integrated_presets(int(found[0]))
                        gen_expression = (x for x in work_array if "guild_silver" in x)
                        # if "guild_silver" in name:
                        for g in gen_expression:
                            guild_daily()
                        gen_expression = (x for x in work_array if "all_silver" in x)
                        # if "all_silver" in name:
                        for g in gen_expression:
                            accepting_quest("ALL")
                            lopang_daily()
                        gen_expression = (x for x in work_array if "all_leapstone" in x)
                        for g in gen_expression:
                            accepting_quest("ALL")
                            hope_daily()
                            swamp_daily()
                            nameless_daily()
                        gen_expression = (x for x in work_array if "2_daily_chaos" in x)
                        for g in gen_expression:
                            ChaosDungeon().start(x, combat, work="2_daily_chaos")
                            switch = 1
                            break
                        # finished_char.append(x)
                        print("FINISHED THIS CHARACTER:", x)
                        configparser.set("Finished_Characters", x, "yes")
                        configparser.write()

                        """ PROBLEMS: mobs spawning BEFORE teleport
                        Code for reseting tasks on DAILY BASIS
                        start_date = datetime.datetime.utcnow()
                        end_date = datetime.datetime.utcnow()
                        my_date_days = start_date + datetime.timedelta(days=0)
    
                        result = start_date - my_date_days
                        if result.days != 0:
                            print("DAILIES RESET")
                        else:
                            print("this task is done")"""
        else:
            if switch == 1:
                break
            total_finished = len(np.unique(finished_char))
            print(total_finished, " = TOTAL FINISHED finished_char= " + str(finished_char)
                  + " / WORKER LIST len : ", len(np.unique(list_of_workers)))
            if total_finished >= len(np.unique(list_of_workers)):
                print("TURNING SWITCH OFF")
                switch = 1
                break
            print("Character not in worker list. Re-logging...")
            switching_char(finished_char, list_of_workers)

        # total_finished = len(np.unique(finished_char))
        # print(total_finished, " = TOTAL FINISHED finished_char= "
        #       + str(finished_char) + " / WORKER LIST len : ", len(list_of_workers))
        # if total_finished == 0 and finished_char == []:
        #     print("CHARACTER NOT ON LIST OF WORKERS")
        #     exit()

        # switching CHar
        # switching_char(finished_char, list_of_workers)
        # FINiSHED ALL IF statement

    print("Finished Daily maybe waiting for chaos...")
    # end = time.time()
    # print(f"Runtime of the program is {end - start}")


def integrated_presets(chosen_preset=1):
    # SWITCHING TO SPECIFIC BUILD
    presets = Daily + "Misc\\integrated_preset.png"
    apply = Daily + "Misc\\apply_preset.png"
    for i in range(1, 10, 1):
        print("choosing preset")
        pydirectinput.keyDown('alt')
        time.sleep(0.3)
        pydirectinput.press('e')
        time.sleep(0.2)
        pydirectinput.keyUp('alt')

        ready = Searchimage_return_position(presets, 1, precision=0.84)
        if ready != [-1, -1]:
            if chosen_preset == 1:
                pydirectinput.click(ready[0] - 50,
                                    ready[1] + 57)
                time.sleep(1)
                apply_preset = Searchimage_return_position(apply, 1, precision=0.84)
                pydirectinput.click(apply_preset[0],
                                    apply_preset[1])
                break
            elif chosen_preset == 2:
                pydirectinput.click(ready[0],
                                    ready[1] + 57)
                time.sleep(1)
                apply_preset = Searchimage_return_position(apply, 1, precision=0.84)
                pydirectinput.click(apply_preset[0]+10,
                                    apply_preset[1]+3)
                break
        else:
            time.sleep(0.7)
            i += 1
            pydirectinput.keyDown('alt')
            time.sleep(0.3)
            pydirectinput.press('e')
            time.sleep(0.2)
            pydirectinput.keyUp('alt')
    # closing menu
    pydirectinput.keyDown('alt')
    time.sleep(0.3)
    pydirectinput.press('e')
    time.sleep(0.2)
    pydirectinput.keyUp('alt')


def swamp_daily():
    print("startin Swamp daily")
    # while True:
    focus_window('LOST ARK')
    # # BIFROST FUNCTIOn
    bifrost_teleportation("Wailling Swamp")
    waiting_for_loading_screen()
    # TESTING While loop for searching of the giant
    switch = 0
    while switch == 0:
        pydirectinput.moveTo(round(Resolution[0] / 2),
                             round(Resolution[1] / 4 * 3))
        pydirectinput.press('F5')
        time.sleep(0.7)
        pydirectinput.press('F5')
        complete_quest = Daily + "Walling Swamp\\Finished\\Completed_quest.png"
        complete = Searchimage_return_position(complete_quest, 1, precision=0.87)
        if complete != [-1, -1]:
            print("finished quest")
            switch = 1
            break
    # OLD METHOD
    # while switch == 0:
    #     pydirectinput.moveTo(Resolution[0]/2,
    #                          Resolution[1]/4*3)
    #     pydirectinput.press('F5')
    #     time.sleep(0.7)
    #     pydirectinput.press('F5')
    #
    #     for f in DailySwamp:
    #         # Tossing at Sentinel
    #         complete_quest = Daily + "Walling Swamp\\Finished\\Completed_quest.png"
    #         print(f)
    #         ready = imagesearch_fast_area(f, precision=0.65)
    #         complete = Searchimage_return_position(complete_quest, 1, precision=0.87)
    #         if ready != [-1, -1]:
    #             pydirectinput.moveTo(ready[0],
    #                                  ready[1])
    #             pydirectinput.press('F5')
    #             time.sleep(0.7)
    #             pydirectinput.press('F5')
    #         if complete != [-1, -1]:
    #             print("finished quest")
    #             switch = 1
    #             break
    # AFTER the quest is finished
    teleported = "no"
    while teleported != "yes":
        # teleporting
        print("completed quest")
        pydirectinput.press('m')
        time.sleep(0.7)
        pydirectinput.click(round(Resolution[0] / 2),
                            round(Resolution[1] / 2), button="right")
        time.sleep(0.7)
        turn_in = Daily + "Walling Swamp\\Navigation\\Kalaja.png"
        turning = Searchimage_return_position(turn_in, 1, precision=0.86)
        pydirectinput.click(turning[0],
                            turning[1])
        time.sleep(0.7)
        turn_in = Daily + "Walling Swamp\\Navigation\\Teleport.png"
        turning = Searchimage_return_position(turn_in, 1, precision=0.90)
        pydirectinput.click(turning[0] + 10,
                            turning[1] + 10)
        time.sleep(0.7)
        pydirectinput.press('ENTER')
        teleported = waiting_for_loading_screen()
    # Feiton Turning in
    pydirectinput.click(585,
                        786, button="right")
    time.sleep(1.4)
    pydirectinput.click(593,
                        1007, button="right")
    time.sleep(1.6)
    pydirectinput.click(455,
                        727, button="right")
    # FAIL SAFE
    success_log = open("success_log.txt", "a+")
    success_log.write("\r\n Good ones: \r\n")
    for k in fail_proof_faiton:
        position = search_click_image(k, "right", precision=0.68)
        time.sleep(0.9)
        if position != [-1, -1]:
            # ENTERING DATA INSIDE TEXT FILE
            success_log.write("\r\n position :" + str(position) + "\r\n" + str(k))
            success_log = open("success_log.txt", "a+")

    pydirectinput.click(799,
                        191, button="right")
    time.sleep(2)
    pydirectinput.click(633,
                        685, button="right")
    time.sleep(1.2)
    pydirectinput.click(1200,
                        878, button="right")
    time.sleep(1.2)
    pydirectinput.click(1239,
                        878, button="right")
    time.sleep(1.1)
    pydirectinput.click(1227,
                        909, button="right")
    time.sleep(1.1)
    pydirectinput.click(972,
                        934, button="right")
    time.sleep(1.1)
    pydirectinput.click(688,
                        343, button="right")
    pydirectinput.click(688,
                        343, button="right")
    time.sleep(2.2)
    pydirectinput.press('g')
    time.sleep(2)
    pydirectinput.press('g')
    time.sleep(1)
    pydirectinput.press('g')
    time.sleep(0.7)
    pydirectinput.press('g')
    time.sleep(0.7)
    pydirectinput.press('g')
    time.sleep(1)
    pydirectinput.press('g')
    time.sleep(1)


def hypnos_daily():
    focus_window('LOST ARK')
    pydirectinput.press('g')
    time.sleep(1)
    pydirectinput.press('g')
    time.sleep(1)
    pydirectinput.press('g')
    time.sleep(1)
    hypno_ready = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\Daily Quest\\Hypnos\\im_ready.png"
    ready = Searchimage_return_position(hypno_ready, 1, precision=0.9)
    pydirectinput.click(ready[0],
                        ready[1])
    pydirectinput.press('g')
    time.sleep(0.6)
    pydirectinput.press('g')
    time.sleep(3)
    # MANUAL MACRO
    pydirectinput.click(1520,
                        820, button="right")
    time.sleep(1.5)
    pydirectinput.click(1865,
                        864, button="right")
    time.sleep(3)
    pydirectinput.click(1448,
                        393, button="right")
    time.sleep(1.1)
    pydirectinput.click(1574,
                        918, button="right")
    time.sleep(1)
    pydirectinput.click(1962,
                        412, button="right")
    time.sleep(1.2)
    pydirectinput.click(2098,
                        514, button="right")
    time.sleep(1.6)
    pydirectinput.click(1579,
                        436, button="right")
    time.sleep(2)
    # STATE CHECK
    hypno_enter = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\Daily Quest\\Hypnos\\Enter.png"
    enter = Searchimage_return_position(hypno_enter, 1, precision=0.9)
    pydirectinput.click(enter[0],
                        enter[1])
    pydirectinput.press('ENTER')
    time.sleep(10)
    pydirectinput.click(1549,
                        508, button="right")
    time.sleep(1)
    pydirectinput.press('g')
    time.sleep(1)
    pydirectinput.press('g')
    time.sleep(0.7)
    pydirectinput.press('g')
    time.sleep(0.7)
    pydirectinput.press('g')
    # STATE CHECK
    hypno_accept = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\Daily Quest\\Hypnos\\Accept.png"
    accept = Searchimage_return_position(hypno_accept, 1, precision=0.9)
    pydirectinput.click(accept[0],
                        accept[1])
    time.sleep(2)
    pydirectinput.click(1795,
                        724, button="right")
    time.sleep(1.3)
    pydirectinput.click(1689,
                        542, button="right")
    time.sleep(1.1)
    pydirectinput.click(1699,

                        540, button="right")
    time.sleep(1)
    # CASTING EMOTE FOR THE QUEST
    pydirectinput.press('6')
    time.sleep(10)

    # COMBAT BEGINS MACRO HERE
    # After combat is done
    pydirectinput.click(856,
                        681, button="right")
    time.sleep(1.5)
    pydirectinput.click(575,
                        507, button="right")
    time.sleep(1.3)
    pydirectinput.click(504,
                        618, button="right")
    time.sleep(1.6)
    pydirectinput.click(1031,
                        240, button="right")
    time.sleep(1.7)
    pydirectinput.click(980,
                        598, button="right")
    time.sleep(1.3)
    pydirectinput.click(824,
                        231, button="right")
    time.sleep(2)
    pydirectinput.press('g')
    time.sleep(1)
    pydirectinput.press('g')
    time.sleep(1)
    pydirectinput.press('g')
    time.sleep(1)
    pydirectinput.press('g')
    time.sleep(2)


def nameless_daily():
    # SELF NOTE everything done exept for killing mobs part
    focus_window('LOST ARK')
    time.sleep(1)
    pydirectinput.press('m')
    time.sleep(0.7)
    turn_in = Daily + "Nameless Valley\\Navigation\\Teleport_nameless_valley.png"
    turning = Searchimage_return_position(turn_in, 1, precision=0.90)
    pydirectinput.click(turning[0] + 15,
                        turning[1] + 15)
    time.sleep(0.7)
    # First teleport movement
    pydirectinput.press('ENTER')
    time.sleep(10)
    pydirectinput.rightClick(711,
                             790, duration=0.3)
    time.sleep(1.4)
    pydirectinput.click(1918,
                        990, button="right")
    time.sleep(1.4)
    pydirectinput.click(1980,
                        950, button="right")
    time.sleep(1.5)
    pydirectinput.click(1966,
                        903, button="right")
    time.sleep(1.4)
    pydirectinput.click(1916,
                        875, button="right")
    time.sleep(1.3)
    pydirectinput.click(1479,
                        896, button="right")
    time.sleep(1.3)
    pydirectinput.click(1390,
                        824, button="right")
    time.sleep(1.2)
    pydirectinput.click(1390,
                        850, button="right")
    time.sleep(1.2)
    pydirectinput.click(1390,
                        850, button="right")
    time.sleep(1.2)
    pydirectinput.click(1825,
                        934, button="right")
    waiting_for_loading_screen(50)
    # Entering new area
    pydirectinput.click(1365,
                        923, button="right")
    time.sleep(1.2)
    pydirectinput.click(1480,
                        806, button="right")
    time.sleep(1.2)
    # Killing mobs
    step_1 = Daily + "Nameless Valley\\Finished\\1_out_of_2.png"
    step = Searchimage_return_position(step_1, 1, precision=0.90)
    while step == [-1, -1]:
        fight_mobs(combat)
        time.sleep(1)
        pydirectinput.press('g')
        time.sleep(3)
        step = Searchimage_return_position(step_1, 1, precision=0.90)
    pydirectinput.click(1733,
                        913, button="right")
    time.sleep(1.2)
    pydirectinput.click(1661,
                        942, button="right")
    time.sleep(1.2)
    pydirectinput.click(1425,
                        628, button="right")
    time.sleep(1.2)
    pydirectinput.click(1425,
                        628, button="right")
    time.sleep(1.2)
    # Killing mobs
    step_2 = Daily + "Nameless Valley\\Finished\\Finally_complete.png"
    step = Searchimage_return_position(step_2, 1, precision=0.90)
    while step == [-1, -1]:
        fight_mobs(combat)
        time.sleep(1)
        pydirectinput.press('g')
        time.sleep(3)
        step = Searchimage_return_position(step_2, 1, precision=0.90)
    teleported = "no"
    while teleported != "yes":
        fight_mobs(combat)
        time.sleep(1)
        # teleporting
        print("completed quest")
        pydirectinput.press('m')
        time.sleep(0.7)
        pydirectinput.click(round(Resolution[0] / 2),
                            round(Resolution[1] / 2), button="right")
        time.sleep(0.7)
        turn_in = Daily + "Walling Swamp\\Navigation\\Kalaja.png"
        turning = Searchimage_return_position(turn_in, 1, precision=0.86)
        pydirectinput.click(turning[0],
                            turning[1])
        time.sleep(0.7)
        turn_in = Daily + "Walling Swamp\\Navigation\\Teleport.png"
        turning = Searchimage_return_position(turn_in, 1, precision=0.90)
        pydirectinput.click(turning[0] + 10,
                            turning[1] + 10)
        time.sleep(0.7)
        pydirectinput.press('ENTER')
        teleported = waiting_for_loading_screen()
    # Walking from teleport to the quest turn in
    pydirectinput.click(585,
                        786, button="right")
    time.sleep(1.4)
    pydirectinput.click(593,
                        1007, button="right")
    time.sleep(1.6)
    pydirectinput.click(455,
                        727, button="right")
    # FAIL SAFE
    success_log = open("success_log.txt", "a+")
    success_log.write("\r\n Good ones: \r\n")
    for k in fail_proof_faiton:
        position = search_click_image(k, "right", precision=0.68)
        time.sleep(0.9)
        if position != [-1, -1]:
            # ENTERING DATA INSIDE TEXT FILE
            success_log.write("\r\n position :" + str(position) + "\r\n" + str(k))
            success_log = open("success_log.txt", "a+")

    time.sleep(6)
    pydirectinput.click(840,
                        202, button="right")
    time.sleep(1.5)
    pydirectinput.click(910,
                        273, button="right")
    time.sleep(1.3)
    pydirectinput.click(857,
                        192, button="right")
    time.sleep(1.4)
    pydirectinput.click(1074,
                        365, button="right")
    time.sleep(1.2)
    pydirectinput.press('g')
    time.sleep(3)

    pydirectinput.press('g')
    time.sleep(0.5)
    pydirectinput.press('g')
    time.sleep(0.5)
    pydirectinput.press('g')
    time.sleep(0.5)
    pydirectinput.press('g')
    time.sleep(0.5)
    pydirectinput.press('g')
    time.sleep(0.5)
    pydirectinput.press('g')
    time.sleep(0.5)
    pydirectinput.press('g')
    time.sleep(0.5)
    pydirectinput.press('g')
    time.sleep(0.5)
    pydirectinput.press('g')
    time.sleep(0.5)
    pydirectinput.press('g')
    time.sleep(0.5)


def lopang_daily():
    focus_window('LOST ARK')
    time.sleep(1)
    # Closing CHAT !!! CAN POSSIBLY CLOSE MINIMAP
    chat = Daily + "Misc\\Minimize_chat.png"
    # ERROR WITH FUNCTION WHEN INSERTING COSTUM region for searching!!!!!
    search_click_image(chat, "left", x1=0, y1=710, x2=600, y2=1050)
    search_click_image(chat, "left", x1=0, y1=710, x2=600, y2=1050)
    print("closed chat")
    # Teleporting to Lopang
    bifrost_teleportation("lopang")
    # Shushire,Vern,Arthentine
    waiting_for_loading_screen()
    pydirectinput.press('g')
    time.sleep(1)
    # Some kind of problem with registering the right click after teleporting to the location???
    pydirectinput.click(565,
                        454, button="right")
    time.sleep(0.1)
    # repeating above click
    pydirectinput.click(565,
                        454, button="right")
    time.sleep(1.5)
    pydirectinput.click(416,
                        781, button="right")
    time.sleep(1.5)
    pydirectinput.click(886,
                        98, button="right")
    time.sleep(1.5)
    pydirectinput.click(1819,
                        23, button="right")
    time.sleep(2.5)
    pydirectinput.click(1737,
                        159, button="right")
    time.sleep(2.2)
    pydirectinput.click(1679,
                        343, button="right")
    time.sleep(2.2)
    pydirectinput.press('g')
    time.sleep(0.2)
    pydirectinput.click(238,
                        982, button="right")
    pydirectinput.click(238,
                        982, button="right")
    time.sleep(2)
    pydirectinput.click(349,
                        989, button="right")
    time.sleep(2)
    pydirectinput.click(195,
                        229, button="right")
    time.sleep(3.1)
    pydirectinput.click(826,
                        188, button="right")
    time.sleep(1.5)
    pydirectinput.click(1117,
                        417, button="right")
    time.sleep(1)
    pydirectinput.press('g')
    time.sleep(0.2)
    # Teleporting and completing quests
    bifrost_teleportation("lopang_arthentine")
    waiting_for_loading_screen()
    pydirectinput.press('g')
    time.sleep(0.4)
    pydirectinput.press('g')
    time.sleep(0.4)
    pydirectinput.press('g')
    time.sleep(0.4)
    pydirectinput.press('g')
    time.sleep(0.4)
    pydirectinput.press('g')
    time.sleep(3)

    bifrost_teleportation("lopang_vern")
    waiting_for_loading_screen()
    pydirectinput.press('g')
    time.sleep(0.4)
    pydirectinput.press('g')
    time.sleep(0.4)
    pydirectinput.press('g')
    time.sleep(0.4)
    pydirectinput.press('g')
    time.sleep(0.4)
    pydirectinput.press('g')
    time.sleep(3)

    bifrost_teleportation("lopang_shushire")
    waiting_for_loading_screen()
    pydirectinput.press('g')
    time.sleep(0.4)
    pydirectinput.press('g')
    time.sleep(0.4)
    pydirectinput.press('g')
    time.sleep(0.4)
    pydirectinput.press('g')
    time.sleep(0.4)
    pydirectinput.press('g')
    time.sleep(3)


def guild_daily():
    focus_window('LOST ARK')
    time.sleep(1)
    pydirectinput.keyDown('alt')
    time.sleep(0.2)
    pydirectinput.press('u')
    time.sleep(0.2)
    pydirectinput.keyUp('alt')
    time.sleep(2)
    arrow_tab_left = Daily + "Misc\\Guild_tabs_left.png"
    search_click_image(arrow_tab_left, "left")
    search_click_image(arrow_tab_left, "left")
    overview_tab = Daily + "Misc\\Guild_overview.png"
    search_click_image(overview_tab, "left")
    # Getting rid of first time notification
    first_login = Daily + "Misc\\First_loging_guild.png"
    search_click_image(first_login, "left")
    # Guild donations
    guild_donation = Daily + "Guild\\Guild_donation.png"
    search_click_image(guild_donation, "left")
    time.sleep(0.2)
    # Donating silver
    silver = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\Daily Quest\\Guild\\Donate_silver.png"
    ready = Searchimage_return_position(silver, 1, precision=0.82)
    if ready != [-1, -1]:
        pydirectinput.click(ready[0]+25,
                            ready[1]+150)
        time.sleep(0.4)
        small_close = Daily + "Misc\\Guild_small_close.png"
        search_click_image(small_close, "left")
    time.sleep(0.2)
    # Research normal SUPPORT
    support_research = Daily + "Guild\\Support_research.png"
    research = Daily + "Guild\\Normal.png"
    ok = Daily + "Guild\\ok.png"
    search_click_image(support_research, "left")
    search_click_image(research, "left")
    search_click_image(ok, "left")
    time.sleep(0.2)
    pydirectinput.keyDown('alt')
    time.sleep(0.2)
    pydirectinput.press('u')
    time.sleep(0.2)
    pydirectinput.keyUp('alt')
    time.sleep(2)


def payto_daily():
    focus_window('LOST ARK')
    time.sleep(1)
    pydirectinput.click(1903,
                        544, button="right")
    time.sleep(10)
    pydirectinput.press('m')
    time.sleep(0.2)
    pydirectinput.click(1903,
                        544, button="right")
    time.sleep(1)
    rive_row = Daily + "Peyto\\Rivelry_row.png"
    search_click_image(rive_row, "left")
    time.sleep(0.7)
    pydirectinput.keyDown('alt')
    time.sleep(0.2)
    pydirectinput.click(1366,
                        777, button="left")
    time.sleep(0.2)
    pydirectinput.keyUp('alt')
    time.sleep(150)
    pydirectinput.press('g')
    time.sleep(10)
    pydirectinput.click(900,
                        281, button="right")
    time.sleep(3)
    pydirectinput.press('9')
    time.sleep(15)
    pydirectinput.press('m')
    time.sleep(0.5)
    pydirectinput.click(1903,
                        544, button="right")
    time.sleep(1)
    turtle = Daily + "Peyto\\Turtle.png"
    search_click_image(turtle, "left")
    time.sleep(0.7)
    pydirectinput.keyDown('alt')
    time.sleep(0.2)
    pydirectinput.click(1452,
                        487, button="left")
    time.sleep(0.2)
    pydirectinput.keyUp('alt')
    time.sleep(150)
    sea_anchor = Daily + "Peyto\\Anchor.png"
    search_click_image(sea_anchor, "right")
    time.sleep(10)
    pydirectinput.click(1832,
                        471, button="right")
    time.sleep(3)
    pydirectinput.press('9')
    time.sleep(15)
    pydirectinput.press('m')
    time.sleep(0.5)
    pydirectinput.click(1903,
                        544, button="right")
    time.sleep(1)
    tortoy = Daily + "Peyto\\Tortoy.png"
    search_click_image(tortoy, "left")
    time.sleep(0.7)
    pydirectinput.keyDown('alt')
    time.sleep(0.2)
    pydirectinput.click(1312,
                        265, button="left")
    time.sleep(0.2)
    pydirectinput.keyUp('alt')
    time.sleep(120)
    # Docking
    pydirectinput.press('z')
    time.sleep(0.5)
    pydirectinput.click(2261,
                        1035, button="left")
    time.sleep(10)
    pydirectinput.click(1875,
                        361, button="left")
    time.sleep(3)
    # Complete quest
    ongoing = Daily + "Peyto\\Ongoing_quest.png"
    search_click_image(ongoing, "left")
    complete = Daily + "Peyto\\Complete.png"
    search_click_image(complete, "left")


def hope_daily():
    focus_window('LOST ARK')
    time.sleep(1)
    # Teleporting to the place
    bifrost_teleportation("Hope island")
    waiting_for_loading_screen()
    # Fighting spiders until quest complete
    switch = 0
    while switch == 0:
        for f in DailySwamp:
            # Tossing at Sentinel
            complete_quest = Daily + "Hope Island\\Finished\\Hope_complete.png"
            complete = Searchimage_return_position(complete_quest, 1, precision=0.90)
            fight_mobs(combat)
            if complete != [-1, -1]:
                print("finished quest")
                switch = 1
                break
    time.sleep(1)
    # Moving to turn in the quest
    time.sleep(0.5)
    pydirectinput.click(2124,
                        167, button="right")
    pydirectinput.click(2124,
                        167, button="right")
    time.sleep(3.5)
    pydirectinput.click(1852,
                        1011, button="right")
    time.sleep(1.4)
    pydirectinput.click(1852,
                        1011, button="right")
    time.sleep(0.9)
    pydirectinput.click(1852,
                        1011, button="right")
    time.sleep(0.9)
    pydirectinput.click(1852,
                        1011, button="right")
    # FAIL SAFE
    for k in fail_safe_hope:
        search_click_image(k, "right", precision=0.77)
    time.sleep(0.9)
    pydirectinput.press('g')
    time.sleep(12)
    pydirectinput.click(1818,
                        970, button="right")
    time.sleep(1.3)
    pydirectinput.click(837,
                        1046, button="right")
    time.sleep(1.4)
    pydirectinput.click(774,
                        1036, button="right")
    time.sleep(1.3)
    pydirectinput.click(1191,
                        870, button="right")
    time.sleep(1.3)
    pydirectinput.click(1910,
                        1008, button="right")
    time.sleep(1.7)
    pydirectinput.click(2178,
                        435, button="right")
    time.sleep(2)
    pydirectinput.click(2034,
                        334, button="right")
    pydirectinput.click(2034,
                        334, button="right")
    # quest_giver = Daily + "Hope Island\\Finished\\quest_giver.png"
    # # search_click_image(quest_giver, "right", precision=0.6)
    # ready = Searchimage_return_position(quest_giver, 1, precision=0.9)
    # if ready != [-1, -1]:
    #     # ready = Searchimage_return_position(quest_giver, 1, precision=0.8)
    #     # print(quest_giver)
    #     pydirectinput.rightClick(ready[0],
    #                              ready[1])
    time.sleep(0.4)
    time.sleep(2)
    pydirectinput.press('g')
    time.sleep(3)
    pydirectinput.press('g')
    time.sleep(1)
    pydirectinput.press('g')
    time.sleep(1)


def accepting_quest(name, target="daily"):
    focus_window('LOST ARK')
    time.sleep(1)
    pydirectinput.keyDown('alt')
    time.sleep(0.2)
    pydirectinput.press('j')
    time.sleep(0.2)
    pydirectinput.keyUp('alt')
    if target == "daily":
        daily_button = Daily + "Misc\\Daily_button.png"
        search_click_image(daily_button, "left")
        time.sleep(1)
        menu = Daily + "Misc\\menu.png"
        search_click_image(menu, "left")

        favorites = Daily + "Misc\\Favorites.png"
        search_click_image(favorites, "left")
        if name == "ALL":
            accept_all = Daily + "Misc\\Accept_quest.png"
            search_click_image(accept_all, "left", click_all="yes")

        if name == "Wailling Swamp":
            swamp = Daily + "Walling Swamp\\Accepting\\Accepting_swamp.png"
            ready = Searchimage_return_position(swamp, 1, precision=0.82)
            if ready != [-1, -1]:
                pydirectinput.click(ready[0] + 855,
                                    ready[1] + 18)
        elif name == "Nameless Valley":
            nameless = Daily + "Nameless Valley\\Accepting\\Accepting_nameless.png"
            ready = Searchimage_return_position(nameless, 1, precision=0.82)
            if ready != [-1, -1]:
                pydirectinput.click(ready[0] + 855,
                                    ready[1] + 18)
        elif name == "Hope Island":
            hope = Daily + "Hope Island\\Accepting\\Accepting_Hope.png"
            ready = Searchimage_return_position(hope, 1, precision=0.82)
            if ready != [-1, -1]:
                pydirectinput.click(ready[0] + 855,
                                    ready[1] + 18)
    elif target == "weekly":
        for x in weekly_tasks:
            weekly_task_pos = Searchimage_return_position(x, 1, precision=0.95)
            weekly_task_pos[0]
        daily_button = Daily + "Misc\\Weekly_button.png"
        search_click_image(daily_button, "left")
        time.sleep(1)
        menu = Daily + "Misc\\menu.png"
        search_click_image(menu, "left")

        favorites = Daily + "Misc\\Favorites.png"
        search_click_image(favorites, "left")

        if name == "ALL":
            accept_all = Daily + "Misc\\Accept_quest.png"
            search_click_image(accept_all, "left", click_all="yes")

    elif target == "guild_request":
        guild_request_button = Daily + "Misc\\Guild_request_button.png"
        search_click_image(guild_request_button, "left")
        # could be difficult to do
        for x in range(0, 2, 1):
            for w in weekly_tasks:
                guild_req_right = Daily + "Misc\\Guild_request_far_right.png"
                search_click_image(guild_req_right, "left")
                position = Searchimage_return_position(w, 1, precision=0.90)
                if position != [-1, -1]:
                    pydirectinput.leftClick(position[0] + 550,
                                            position[1] + 10)
                    time.sleep(1)
                    break
        for w in weekly_tasks:
            guild_req_left = Daily + "Misc\\Guild_request_far_left.png"
            search_click_image(guild_req_left, "left")
            position = Searchimage_return_position(w, 1, precision=0.90)
            if position != [-1, -1]:
                pydirectinput.leftClick(position[0] + 550,
                                        position[1] + 10)
                time.sleep(1)
                break

    time.sleep(1)
    pydirectinput.keyDown('alt')
    time.sleep(0.2)
    pydirectinput.press('j')
    time.sleep(0.2)
    pydirectinput.keyUp('alt')


def bifrost_teleportation(name):
    time.sleep(1)
    # Looks for Bifrost button
    bifrost = Daily + "Misc\\BIFROST.png"
    bifrost_pos = Searchimage_return_position(bifrost, 1, precision=0.95)
    if bifrost_pos != [-1, -1]:
        pydirectinput.click(bifrost_pos[0],
                            bifrost_pos[1])
    else:
        print("cannot find BIFROST button")
        exit()
    precision = 0.90
    # Looks for name of map of Bifrost
    if name == "Wailling Swamp":
        swamp = Daily + "Walling Swamp\\Bifrost\\Swamp.png"
        ready = Searchimage_return_position(swamp, 1, precision=precision)
        if ready != [-1, -1]:
            # Clicking position to the right of it where Move button is
            pydirectinput.click(ready[0] + 400,
                                ready[1])
    elif name == "Hope island":
        hope = Daily + "Hope island\\Bifrost\\BIFROST_hope.png"
        ready = Searchimage_return_position(hope, 1, precision=precision)
        if ready != [-1, -1]:
            # Clicking position to the right of it where Move button is
            pydirectinput.click(ready[0] + 400,
                                ready[1])
    elif name == "lopang":
        lopang = Daily + "Lopang\\Bifrost\\BIFROST_lopang.png"
        ready = Searchimage_return_position(lopang, 1, precision=0.95)  # 95 HAD SOME ERRORS teleporting to wrong
        if ready != [-1, -1]:
            # Clicking position to the right of it where Move button is
            pydirectinput.click(ready[0] + 400,
                                ready[1])
    elif name == "lopang_arthentine":
        lopang_art = Daily + "Lopang\\Bifrost\\BIFROST_Arthentine.png"
        ready = Searchimage_return_position(lopang_art, 1, precision=precision)
        if ready != [-1, -1]:
            # Clicking position to the right of it where Move button is
            pydirectinput.click(ready[0] + 400,
                                ready[1])
    elif name == "lopang_vern":
        lopang_vern = Daily + "Lopang\\Bifrost\\BIFROST_Vern.png"
        ready = Searchimage_return_position(lopang_vern, 1, precision=precision)
        if ready != [-1, -1]:
            # Clicking position to the right of it where Move button is
            pydirectinput.click(ready[0] + 400,
                                ready[1])
    elif name == "lopang_shushire":
        lopang_shushire = Daily + "Lopang\\Bifrost\\BIFROST_Shushire.png"
        ready = Searchimage_return_position(lopang_shushire, 1, precision=precision)
        if ready != [-1, -1]:
            # Clicking position to the right of it where Move button is
            pydirectinput.click(ready[0] + 400,
                                ready[1])
    else:
        print("ERROR: Unknown BIFROST location")

    # checking if its asking for crystals to teleport
    crystalcheck = Daily + "Misc\\Cost_for_BIFROST.png"
    pos_crystal = Searchimage_return_position(crystalcheck, 1, precision=precision)
    time.sleep(0.7)
    # print(pos_crystal)
    if pos_crystal == [-1, -1]:
        print("Teleporting...")
        pydirectinput.press('ENTER')
    else:
        print("I Dont wanna spend crystals")
        exit()


def fight_mobs(class_name):
    print("Starting COMBAT")
    if class_name == "Bard":
        pydirectinput.press('e')
        time.sleep(1)
        pydirectinput.press('d')
        time.sleep(1)
        pydirectinput.press('r')
        time.sleep(1)
        pydirectinput.press('s')
        time.sleep(1)
    if class_name == "Lance master":
        pydirectinput.moveTo(round(Resolution[0] / 2),
                             round(Resolution[1] / 2))
        time.sleep(1)
        # pydirectinput.press('w')
        # time.sleep(0.3)
        # pydirectinput.press('w')
        # time.sleep(0.6)
        # pydirectinput.press('e')
        # time.sleep(1)
        pydirectinput.press('q')
        time.sleep(1)
        pydirectinput.press('f')
        time.sleep(1)
        pydirectinput.press('d')
        time.sleep(1)
    # Needs fixing Paladin combat for SWAMp daily
    if class_name == "Paladin":
        pydirectinput.press('d')
        time.sleep(1)
        # Move mouse to center of screen for double taping skills
        pydirectinput.moveTo(round(Resolution[0]/2),
                             round(Resolution[1]/2))
        pydirectinput.press('w')
        time.sleep(0.3)
        pydirectinput.press('w')
        time.sleep(0.5)
        pydirectinput.press('e')
        time.sleep(0.3)
        pydirectinput.press('e')
        time.sleep(2)
    if class_name == "Arcana":
        pydirectinput.moveTo(round(Resolution[0] / 2),
                             round(Resolution[1] / 2))
        pydirectinput.press('s')
        time.sleep(1)
        pydirectinput.press('d')
        time.sleep(0.3)
        pydirectinput.press('d')
        time.sleep(0.3)
        pydirectinput.press('f')
        time.sleep(0.3)
        pydirectinput.press('f')
        time.sleep(2)
    if class_name == "Deathblade":
        pydirectinput.moveTo(round(Resolution[0] / 2),
                             round(Resolution[1] / 2))
        pydirectinput.press('q')
        time.sleep(1)
        pydirectinput.press('e')
        time.sleep(2)
        pydirectinput.press('w')
        time.sleep(0.5)
        pydirectinput.press('r')
        time.sleep(2)
    else:
        print("Kek ", class_name, "has no combat for quests atm")


def switching_char(finished_char, list_of_workers):
    # maybe use dictionary ??
    count = 0

    char_loop = 9

    switch_stepx = 258
    switch_stepy = 117

    first_x = 692
    first_y = 400

    box_size_x = 165
    box_size_y = 23
    # entering switch char menu
    for i in range(1, 10, 1):
        ready = Searchimage_return_position(esc_menu, 1, precision=0.84)
        if ready != [-1, -1]:
            break
        else:
            time.sleep(0.7)
            i += 1
            pydirectinput.press('ESC')

    button = Daily + "Misc\\Switching\\switch_character.png"
    search_click_image(button, "left", x2=1800)
    went_down = 0
    went_up = 0
    while went_up == 0:
        button = Daily + "Misc\\Switching\\button_down.png"
        search_click_image(button, "left", x2=1800)

        if went_down == 1:
            button = Daily + "Misc\\Switching\\button_up.png"
            search_click_image(button, "left")
            first_x = 692
            first_y = 400
        # formula for going through all 9 characters
        for i in range(0, char_loop, 1):
            count = count + 1
            # print(count)
            # print(char_loop)
            # count devideable by 3
            first_x = first_x + switch_stepx
            text = image2text(x1=first_x, y1=first_y,
                              x2=box_size_x, y2=box_size_y)
            print(text)

            generator_expression = (x for x in list_of_workers if x not in finished_char)
            # for u in generator_expression2:
            #     print("PRINTING X ", u)
            #     if u in text:
            #         123
            # generator_expression = (x for x in finished_char if x not in text)
            for g in generator_expression:
                if g in text:
                    time.sleep(0.7)
                    pydirectinput.click(first_x,
                                        first_y, button="left")
                    time.sleep(1)
                    pydirectinput.click(1371,
                                        736, button="left")
                    time.sleep(1)
                    pydirectinput.press('ENTER')
                    print("LOGING in...", text)
                    waiting_for_loading_screen(100)
                    time.sleep(3)
                    went_up = 1
                    went_down = 1
                    break
            if went_up == 1:
                break
            if count % 3 == 0:
                print("count is DEVIDABLE", count)
                first_y = first_y + switch_stepy
                first_x = 945 - switch_stepx
        if went_down == 1:
            went_up = 1
        went_down = 1
    # return text, first_x, first_y


def waiting_for_loading_screen(tries=100):
    count_loading = 0
    for i in range(0, tries, 1):
        print("looking for black")
        count_loading = count_loading + 1
        im = pyautogui.screenshot(region=(1652, 168, 240, 210))
        r, g, b = im.getpixel((1772 - 1652, 272 - 168))
        if r == 0 and g == 0 and b == 0:
            break
        time.sleep(0.15)
    if count_loading == tries:
        print("Loading screen not found")
    else:
        print("Loading screen found")
        # looking for light
        for i in range(0, 20, 1):
            print("looking for ARROW")
            loading_arrow = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\Daily Quest\\Misc\\Loading_screen_arrow.png"
            position = searchimageinarea(loading_arrow, "TESTING.png", precision=0.85)
            if position != [-1, -1]:
                break
            time.sleep(0.3)
        teleport = "yes"
        for i in range(0, 700, 1):
            print("looking for black")
            im = pyautogui.screenshot(region=(1652, 168, 240, 210))
            r, g, b = im.getpixel((1772 - 1652, 272 - 168))
            if r == 0 and g == 0 and b == 0:
                print("finished loading screen")
                break
            time.sleep(0.15)
        time.sleep(4)
        return teleport


def stronghold_daily():
    focus_window('LOST ARK')
    time.sleep(0.5)
    pydirectinput.press('F2')
    time.sleep(0.5)
    song = Daily + "Stronghold\\stronghold_song.png"
    search_click_image(song, "left")
    play_song = Daily + "Misc\\song_play.png"
    search_click_image(play_song, "left")
    # song cast + loading screen
    waiting_for_loading_screen()
    # to avoid talking bich on start time sleep or input
    time.sleep(3)
    pydirectinput.leftClick(round(Resolution[0]/2),
                            round(Resolution[1]/2)+200)

    pydirectinput.keyDown('ctrl')
    time.sleep(0.3)
    pydirectinput.press('1')
    time.sleep(0.2)
    pydirectinput.keyUp('ctrl')
    time.sleep(1)
    Gold_anchor = Daily + "Stronghold\\Gold_anchor.png"
    search_click_image(Gold_anchor, "left")
    for i in range(0, 4, 1):
        time.sleep(1)
        mission_complete = Daily + "Stronghold\\mission_complete.png"
        search_click_image(mission_complete, "left", precision=0.8)
        time.sleep(1)
        mission_results = Daily + "Stronghold\\Mission_result.png"
        search_click_image(mission_results, "left", precision=0.8)
        time.sleep(2)
        ok_button = Daily + "Stronghold\\ok_button.png"
        search_click_image(ok_button, "left", precision=0.8)
    time.sleep(1)
    # Needs clicking on missions part
    for c in chosen_missions:
        # clicking on mission
        print(c)
        search_click_image(c, "left")
        repair = Daily + "Stronghold\\Repair.png"
        search_click_image(repair, "left", precision=0.8)
        print("trying to click repair")
        time.sleep(1)
        btn_ship_repair = Daily + "Stronghold\\button_ship_repair.png"
        search_click_image(btn_ship_repair, "left", precision=0.8)
        print("trying to click SHIP repair")
        time.sleep(1)
        auto_formation = Daily + "Stronghold\\auto_formation.png"
        search_click_image(auto_formation, "left")
        time.sleep(1)
        mission_start = Daily + "Stronghold\\mission_start.png"
        search_click_image(mission_start, "left")
        time.sleep(1)
        ok_button = Daily + "Stronghold\\mission_start.png"
        search_click_image(ok_button, "left")
        time.sleep(1)
        pydirectinput.press('ENTER')
    # Special missions
    time.sleep(1)
    special_mission = Daily + "Stronghold\\Special_Mission.png"
    search_click_image(special_mission, "left")
    # Completing missions
    for k in range(0, 2, 1):
        time.sleep(1)
        mission_complete = Daily + "Stronghold\\mission_complete.png"
        pos = Searchimage_return_position(mission_complete)
        if pos != [-1, -1]:
            search_click_image(mission_complete, "left")
            time.sleep(1)
            mission_results = Daily + "Stronghold\\Mission_result.png"
            search_click_image(mission_results, "left")
            time.sleep(4)
            ok_button = Daily + "Stronghold\\ok_button.png"
            search_click_image(ok_button, "left")
        else:
            break
    # Sending on new ones
    for i in range(0, 2, 1):
        time.sleep(1)
        stronghold_yoho = Daily + "Stronghold\\stronghold_yoho.png"
        search_click_image(stronghold_yoho, "left")
        time.sleep(1)
        repair = Daily + "Stronghold\\Repair.png"
        search_click_image(repair, "left", precision=0.8)
        print("trying to click repair")
        time.sleep(1)
        btn_ship_repair = Daily + "Stronghold\\button_ship_repair.png"
        search_click_image(btn_ship_repair, "left", precision=0.8)
        print("trying to click SHIP repair")
        time.sleep(1)
        auto_formation = Daily + "Stronghold\\auto_formation.png"
        search_click_image(auto_formation, "left")
        mission_start = Daily + "Stronghold\\mission_start.png"
        search_click_image(mission_start, "left")
        time.sleep(1)
        ok_button = Daily + "Stronghold\\mission_start.png"
        search_click_image(ok_button, "left")
        pydirectinput.press('ENTER')

    # Harvest Farm
    time.sleep(1)
    farm_button = Daily + "Stronghold\\Farm.png"
    search_click_image(farm_button, "left")
    time.sleep(1)
    harvest_all = Daily + "Stronghold\\Harvest_all.png"
    search_click_image(harvest_all, "left", precision=0.8)
    time.sleep(1)
    check_ok = Daily + "Stronghold\\check_ok.png"
    search_click_image(check_ok, "left", precision=0.8)
    time.sleep(1)
    ok_button = Daily + "Stronghold\\ok_button.png"
    search_click_image(ok_button, "left", precision=0.8)
    time.sleep(4)

    # Pet farm
    for c in pet_ranch:
        search_click_image(c, "left")
        time.sleep(1)

    # Closing menus
    time.sleep(1)
    pydirectinput.press('ESC')
    time.sleep(0.7)
    pydirectinput.press('ESC')
    time.sleep(1)
    pydirectinput.press('9')
    time.sleep(6.2)
    waiting_for_loading_screen()
    # normal mission cast(priority Major missions else 540 300 195 90 rewards)


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


class ChaosDungeon:

    def __init__(self):
        self.skills_dict = []
        self.all_event = multiprocessing.Event()
        self.two_chaos = multiprocessing.Event()
        self.combat_event = multiprocessing.Event()
        self.normal_event = multiprocessing.Event()
        self.current_class = ""
        self.current_work = ""
        keyboard.add_hotkey('-', self.stop_combat)
        keyboard.add_hotkey('=', self.stop_normal)
        # MAKE HIGH PRIORITY ON STAGGER IMMUNE SKILLS NEEDS REWORKING ON SKILL USAGE

        self.all_processes = [Thread(target=self.state_check)]
        self.normal_processes = [Thread(target=self.minimap_detection)]
                                 # multiprocessing.Process(target=self.centeral_detection),
                                 # multiprocessing.Process(target=self.minimap_detection)]
        self.combat_processes = [Thread(target=self.centeral_detection),
                                 Thread(target=self.combat)
                                 # multiprocessing.Process(target=self.combat)
                                 ]
        self.skill_processes = []
        # for _ in range(multiprocessing.cpu_count())]

    def process_search(self, search, process_search_inc):
        # found_at = [(MiniMCOORD[0] + search[0]),
        #             (MiniMCOORD[1] + search[1])]

        found_at = search
        distance = [found_at[0] - playerMinimap[0],
                    found_at[1] - playerMinimap[1]]
        print(process_search_inc)
        # distance = [round(distance[0]) * process_search_inc,
        #             round(distance[1]) * process_search_inc]
        # # distance[1] = round(distance[1]) * process_search_inc
        # print(panchor,distance)
        # result = numpy.array(panchor) - numpy.array(distance)
        # print(result)
        ps_x1 = round(panchor[0] + round(distance[0]) * process_search_inc)
        ps_y1 = round(panchor[1] + round(distance[1]) * process_search_inc)

        if ps_x1 > round(Resolution[0]/100*90):
            ps_x1 = round(Resolution[0]/100*90)
        if ps_x1 < round(Resolution[0]/100*15):
            ps_x1 = round(Resolution[0]/100*15)

        if ps_y1 > round(Resolution[1]/100*72):
            ps_y1 = round(Resolution[1]/100*72)
        if ps_y1 < round(Resolution[1]/100*10):
            ps_y1 = round(Resolution[1]/100*10)
        # print("Distance is :", distance)
        # print(ps_x1, ps_y1)
        return ps_x1, ps_y1

    def stay_within(self, x_cord, y_cord):
        if x_cord > round(Resolution[0] / 100 * 90):
            x_cord = round(Resolution[0] / 100 * 90)
        if x_cord < round(Resolution[0] / 100 * 15):
            x_cord = round(Resolution[0] / 100 * 15)

        if y_cord > round(Resolution[1] / 100 * 72):
            y_cord = round(Resolution[1] / 100 * 72)
        if y_cord < round(Resolution[1] / 100 * 10):
            y_cord = round(Resolution[1] / 100 * 10)
        return x_cord , y_cord

    def drinking_potions(self):
        search = image2text(x1=947, y1=954, x2=225, y2=20,
                            method='--psm 7 --oem 3 -c tessedit_char_whitelist=/0123456789')
        print(search)
        first, second = 1, 1
        try:
            first, second = search.rsplit('/', 1)
        except:
            print("Error with split string")
        # print(first, second)
        # print(search)
        result = 1
        if first != '' and second != '':
            first = str(first).replace(' /', '')
            second = str(second).replace(' /', '')
            try:
                result = int(first) / int(second)
                print(round(result, 2))
            except:
                print("Error with HP potion number")
            if result <= 0.70:
                global potions_used
                potions_used += 1
                pydirectinput.press('F1')
                print("USING HP POTION", potions_used)
            else:
                123

    def centeral_detection(self):
        print("Central / HPbars")
        while not self.combat_event.is_set():
            count_occurrance = 0
            movementdelay = 0.4
            self.drinking_potions()
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
                search = im_search_in_area(g, occurances, look_for="HPbar", precision=0.86,
                                           x1=startx, y1=starty, y2=round(Resolution[1] / 100 * 83))  # - 180)
                if search == [-1, -1]:
                    123
                elif search is None:
                    print("SEARCH IS NONE", search)
                else:
                    print("Found HPbar ", split_string)
                    x1 = round(search[0])
                    y1 = round(search[1])
                    y1 = y1 + 50  # distance under red HP bar
                    x1, y1 = self.stay_within(x1, y1)
                    pydirectinput.moveTo(x1, y1)
                    time.sleep(0.4)

    def minimap_detection(self):
        while not self.normal_event.is_set():
            count_occurrance = 0
            print("DOING MINIMAP")
            # print("starting MINIMAP_detect and switch is:", switch)
            global process_search_inc
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
                split_string = g.rsplit('\\')[6]
                # print(split_string)
                # print(g)
                count_occurrance = count_occurrance + 1
                occurances = str(count_occurrance) + str(split_string)
                # MINIMAP Searching
                search = im_search_in_area(g, occurances, looking_for,
                                           x1=MiniMCOORD[0], y1=MiniMCOORD[1],
                                           x2=MiniMCOORD[2], y2=MiniMCOORD[3], precision=0.65)
                # print(count_occurrance, search, g)
                if search == [-1, -1] or None:
                    123
                    # print("NOT FOUND 0 " + split_string)
                    # pydirectinput.mouseDown(button="right")
                    # time.sleep(movementdelay)
                    # pydirectinput.mouseUp(button="right")
                else:
                    # MINIMAP Processing
                    print("Found ", split_string, search)
                    x1, y1 = self.process_search(search, process_search_inc)
                    pydirectinput.moveTo(x1,y1)

                    # pydirectinput.mouseDown(x1, y1, button="right")
                    # time.sleep(movementdelay)
                    # pydirectinput.mouseUp(button="right")
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
                        time.sleep(0.2)
                        pydirectinput.press("v")
                        break
                        # wait for image if image th
                        # press g
                    if "Portal" in g:
                        print("PORTAL PART STARTED")
                        start_time = time.time()
                        break_switch = 0
                        while break_switch != 1:
                            process_search_inc = 10
                            Thread(target=self.stop_combat).start()
                            Thread(target=self.waiting_for_black).start()
                            for p in passingthrough:
                                # pydirectinput.press('-')  # stopping combat
                                # print("PRINTING THIS SHIT ", misc_dictionary["loading"])
                                if misc_dictionary["loading"] == "yes":
                                    end_time = time.time()
                                    result_time = end_time - start_time
                                    print("FOUND LOADING FROM PORTAL")
                                    success_log = open("Chaos_logs.txt", "a+")
                                    success_log.write("\r\n Time to enter PORTAL in seconds:" + str(result_time))
                                    success_log = open("Chaos_logs.txt", "a+")
                                    misc_dictionary["loading"] = "no"
                                    # Thread(target=self.start_combat).start()
                                    self.restating_stopped(countingportattempt)
                                    break_switch = 1
                                    break
                                port_pos = im_search_until_found(p, time_sample=0.1, precision=0.7)
                                if port_pos != [-1, -1]:
                                    print("Entering portal")
                                    pydirectinput.rightClick()
                                    print("pressed G")
                                    pydirectinput.press("g")
                                    # SWITCH TURNED ON
                                    self.restating_stopped(countingportattempt)
                                    # switch.append("On")
                                    break_switch = 1
                                    break
                                else:
                                    # Counts attempts it tried to enter in portal
                                    countingportattempt = countingportattempt + 1
                                    fportal = (countingportattempt, " Found portal")
                                    search = im_search_in_area(g, str(fportal), look_for=looking_for,
                                                               x1=MiniMCOORD[0], y1=MiniMCOORD[1],
                                                               x2=MiniMCOORD[2], y2=MiniMCOORD[3], precision=0.7)
                                    print("Searching for portal", search)
                                    # print(MiniMCOORD[0], MiniMCOORD[1])
                                    if search != [-1, -1]:
                                        x1, y1 = self.process_search(search,process_search_inc)
                                        print("Found portal on MINIMAP going in that direction: ", x1, y1)
                                        pydirectinput.press("SPACE")
                                        time.sleep(0.1)
                                        pydirectinput.mouseDown(x1, y1 - 15, button="right")
                                        time.sleep(0.1)
                                        pydirectinput.mouseDown(button="right")
                                        # pydirectinput.press("g")
                                        # time.sleep(1)
                                        # pydirectinput.mouseUp(button="right")
                                        # pydirectinput.mouseUp(button="left")
                                    if countingportattempt >= 2:
                                        print("Random movement", search)
                                        pydirectinput.mouseDown(x1, y1, button="right")
                                        time.sleep(movementdelay)
                                        pydirectinput.mouseUp(button="right")
                                    if countingportattempt >= 14:
                                        process_search_inc = 2
                                        break_switch = 1
                                        break
                        process_search_inc = 2
                    if "Tower" in g:
                        # MAYBE COMEPLETE NEW APROACH TO FINDING TOWER
                        print("found Tower ", search)
                        global last_cords
                        print("last_cords ", last_cords)
                        process_search_inc = 20
                        x1_tower, y1_tower = self.process_search(search, process_search_inc)

                        sim_x1 = abs(x1_tower - last_cords[0])
                        sim_y1 = abs(y1_tower - last_cords[1])
                        print("SIMILARITIES", sim_y1, sim_y1)
                        if sim_x1 < 25 and sim_y1 < 25:
                        # if [x1, y1] == last_cords:
                            print("LAST CORD IS SIMILAR. Similarities : ", sim_x1, sim_y1)
                            x1_tower = random.randint(700, 2000)
                            y1_tower = random.randint(300, 700)
                            pydirectinput.moveTo(x1_tower, y1_tower)
                            # pydirectinput.mouseDown(x1, y1, button="right")
                            time.sleep(movementdelay)
                            process_search_inc = 2
                        else:
                            print("Current last_cords ", last_cords)
                            # THERE WAS AN ERROR WHERE y1 here was larger than 90% of screen should be impossible
                            last_cords = [x1_tower, y1_tower]
                            if x1_tower < 380:
                                print("ERROR WITH COORDINATES X")
                                exit()
                            if y1_tower > 800:
                                print("ERROR WITH COORDINATES Y")
                                exit()
                            pydirectinput.moveTo(x1_tower, y1_tower)
                            # pydirectinput.mouseDown(x1, y1, button="right")
                            time.sleep(movementdelay)
                            process_search_inc = 2
                            break

            count_occurrance = 0
            for f in minimap_red:
                # print("Doing reds ", f)
                split_string = f.rsplit('\\')[6]
                count_occurrance = count_occurrance + 1
                occurances = str(count_occurrance) + str(split_string)

                search = im_search_in_area(f, occurances, look_for="Red",
                                           x1=MiniMCOORD[0], y1=MiniMCOORD[1],
                                           x2=MiniMCOORD[2], y2=MiniMCOORD[3], precision=0.6)

                if search != [-1, -1]:
                    x1, y1 = self.process_search(search, process_search_inc)
                    print("Found red", x1, y1)
                    pydirectinput.moveTo(x1, y1)
                    # pydirectinput.mouseDown(x1, y1, button="right")
                    time.sleep(movementdelay)
                    # pydirectinput.mouseUp(button="right")
                    break

    def repair_and_enter(self, counting):
        repair_gear = 'C:\\Users\\Ggjustice\\Pictures\\Buttons\\ChaosMisc\\Repair_gear.png'
        leave = 'C:\\Users\\Ggjustice\\Pictures\\Buttons\\ChaosMisc\\Leave.png'
        ok_button = 'C:\\Users\\Ggjustice\\Pictures\\Buttons\\ChaosMisc\\ok_button.png'
        repair_all = 'C:\\Users\\Ggjustice\\Pictures\\Buttons\\ChaosMisc\\Repair all.png'

        position = imagesearch_fast_area(repair_gear, precision=0.7)
        print("Repairing stuff", position)
        if position != [-1, -1]:
            print("REPAIRING")
            Thread(target=self.stop_normal).start()
            time.sleep(1)
            Thread(target=self.stop_combat).start()
            time.sleep(4)
            search_click_image(leave, "left")
            time.sleep(1)
            search_click_image(ok_button, "left")
            time.sleep(40)  # loading screen
            pydirectinput.press('g')
            time.sleep(2)
            search_click_image(repair_all, "left")
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
            self.restating_stopped(counting)

    def repairing(self):
        pet_status = "yes"
        repair_all = 'C:\\Users\\Ggjustice\\Pictures\\Buttons\\ChaosMisc\\Repair all.png'
        repair_icon = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\Daily Quest\\Misc\\Pet_repairing.png"
        if pet_status == "yes":
            pydirectinput.keyDown('alt')
            time.sleep(0.3)
            pydirectinput.press('p')
            time.sleep(0.2)
            pydirectinput.keyUp('alt')
            search_click_image(repair_icon, "left")
            time.sleep(0.5)
            search_click_image(repair_all, "left")
            time.sleep(1)
            pydirectinput.press('ESC')
            time.sleep(1)
            pydirectinput.press('ESC')
        else:
            123

    def state_check(self, current_worker, *args):
        print(*args)
        print("i was here", current_worker)
        #Misc
        counting_state = 0
        count_death = 0
        count_stage_clear = 0
        count_stage_fail = 0
        success_log = open("success_log.txt", "a+")
        focus_window('LOST ARK')
        # Begining on the program REPAIRING
        self.repairing()
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
        self.start_combat()
        # after repairing
        while not self.all_event.is_set():
            for y in check_if_clear:
                counting_state += 1
                position = imagesearch_fast_area(y, precision=0.7)
                if position != [-1, -1]:
                    # checking for % in top left corner
                    stage_percent = image2text(x1=107, y1=186, x2=55, y2=19,
                                               method='--psm 7 --oem 3 -c tessedit_char_whitelist=%0123456789')

                    stage_percent = str(stage_percent).replace('\n', '')
                    stage_percent = str(stage_percent).replace(' ', '')
                    if stage_percent == "100%":
                        print("SUCCESS")
                        count_stage_clear += 1
                    else:
                        print("STAGE FAIL", stage_percent)
                        count_stage_fail += 1
                    success_log = open("Chaos_logs.txt", "a+")
                    success_log.write("\r\n WORKER name :" + str(current_worker))
                    success_log.write("\r\n Deaths :" + str(count_death))
                    success_log.write("\r\n Clears :" + str(count_stage_clear))
                    global potions_used
                    print("CURRENT TOTAL POTS USED ", potions_used)
                    success_log.write("\r\n Potions :" + str(potions_used))
                    success_log.write("\r\n Failed stages :" + str(count_stage_fail))
                    success_log = open("Chaos_logs.txt", "a+")
                    print(count_stage_fail, count_stage_clear)
                    result = count_stage_fail + count_stage_clear
                    if self.two_chaos.is_set():
                        if int(result) >= 2:
                            # Save Shadowplay
                            # pydirectinput.keyDown('alt')
                            # time.sleep(0.1)
                            # pydirectinput.press('F10')
                            # time.sleep(0.1)
                            # pydirectinput.keyUp('alt')
                            self.stop_normal()
                            self.stop_combat()
                            print("FINISHED 2 RUNS of CHAOS")
                            configparser.set("Finished_Characters", current_worker, "yes")
                            configparser.write()
                            daily_state_check()
                            self.stop_all()
                            # os._exit(1)
                    else:
                        print("INFINITE CHAOS CONTINUES")
                    for u in restart_chaos:
                        time.sleep(0.7)
                        search_click_image(u, "left")
                    # print("APPENDED switch to ", switch)
                    # add loading screen function
                    time.sleep(10)
                    self.restating_stopped(counting_state)
            # turn on for INFINITE chaos
            # self.repair_and_enter(counting_state)
            for x in checkIFDEAD:
                position = search_click_image(x, "left")
                time.sleep(2)
                if position == [-1, -1]:
                    time.sleep(5)
                    # print("still alive and switch is", switch)
                else:
                    count_death += 1
                    print("DEATH COUNTER:", count_death)
                    pydirectinput.press('-')
                    time.sleep(2)
                    search_click_image(x, "left")
                    # switch.append("On")
                    self.restating_stopped(counting_state)
                    # print("APPENDED switch to ", switch)
                    time.sleep(1)
                for y in ReENTERing:
                    position = search_click_image(y, "left")
                # check if timer is 0 then enter chaos
                # CHeck if need to repair
        return "Unlucky"

    def restating_stopped(self, count):
        restarting_dict = {"name": "thread"}
        self.combat_event.set()
        if self.combat_event.is_set():
            print("RESTARTING COMBAT and HPbars ", count)
            pydirectinput.press('-')  # Stopping combat
            self.combat_event.clear()
            # NEW APROACH COMBAT
            name = str(count)
            restarting_dict[name] = Thread(target=self.skills)
            self.skill_processes.append(restarting_dict[name])
            print(restarting_dict[name])
            restarting_dict[name].start()

            # # OLD APROACH COBMAT
            # for key in self.skills_dict:
            #     print(key)
            #     # self.skill_processes.append(
            #     #     Thread(target=self.skills, args=key)
            #     #     # multiprocessing.Process(target=self.skills, args=key)
            #     # )
            #     name = str(count)
            #     restarting_dict[name] = Thread(target=self.skills, args=key)
            #     self.skill_processes.append(restarting_dict[name])
            #     restarting_dict[name].start()
        # if self.combat_event.is_set():
            count = count + 1
            name = str(count)
            restarting_dict[name] = Thread(target=self.centeral_detection)
            self.combat_processes.append(restarting_dict[name])
            restarting_dict[name].start()
            # central_detection = Thread(target=self.centeral_detection)
            # central_detection.start()

        if self.normal_event.is_set():
            print("RESTARTING NORMAL")
            pydirectinput.press('=')  # Stopping normal
            self.normal_event.clear()
            count = count + 1
            name = str(count)
            restarting_dict[name] = Thread(target=self.minimap_detection)
            self.normal_processes.append(restarting_dict[name])
            restarting_dict[name].start()
            # minimap = Thread(target=self.minimap_detection)
            # minimap.start()

        time.sleep(10)

    def waiting_for_black(self):
        while True:
            # print("looking for loading screen")
            pydirectinput.press("g")
            im = pyautogui.screenshot(region=(1652, 168, 240, 210))
            r, g, b = im.getpixel((1772 - 1652, 272 - 168))
            if r == 0 and g == 0 and b == 0:
                print("FOUND LOADING SCREEN")
                misc_dictionary["loading"] = 'yes'
                time.sleep(0.1)
                break

    def start(self, char_name, my_class, work):
        self.current_class = my_class
        self.current_work = work
        print("VARIABLES ARE : ", char_name, my_class, work)
        if self.current_class == "Bard":
            self.skills_dict = {'q': "normal", 'w': "normal", 'e': "normal", 'r': "normal",  # Bard NO COOLDOWNS
                                'a': "combo", 's': "normal", 'd': "normal", 'f': "combo"}
        if self.current_class == "Paladin":
            self.skills_dict = {'q': "normal", 'w': "combo", 'e': "combo", 'r': "combo",  # Paladin NO COOLDOWNS
                                'a': "normal", 's': "normal", 'd': "normal", 'f': "combo"}
        if self.current_class == "Soulfist":
            self.skills_dict = {'q': "normal", 'w': "normal", 'e': "normal", 'r': "normal",  # Soulfist image casting
                                'a': "combo", 's': "holding", 'd': "holding", 'f': "combo"}
        if self.current_class == "Striker":
            self.skills_dict = {'q': "normal", 'w': "normal", 'e': "combo", 'r': "holding",  # Striker image casting
                                'a': "combo", 's': "normal", 'd': "holding", 'f': "holding"}
        if self.current_class == "Deathblade":
            self.skills_dict = {'q': "normal", 'w': "combo", 'e': "normal", 'r': "normal",  # Deathblade image casting
                                'a': "combo", 's': "normal", 'd': "holding", 'f': "holding"}
        if self.current_class == "Sorceress":
            self.skills_dict = {'q': "normal", 'w': "combo", 'e': "normal", 'r': "normal",  # Sorceress image casting
                                'a': "normal", 's': "normal", 'd': "normal", 'f': "normal"}
        if self.current_class == "Gunlancer":
            self.skills_dict = {'q': "normal", 'w': "combo", 'e': "normal", 'r': "normal",  # Gunlancer image casting
                                'a': "combo", 's': "holding", 'd': "combo", 'f': "holding"}
        if self.current_class == "Lance master":
            self.skills_dict = {'q': "normal", 'w': "combo", 'e': "normal", 'r': "combo",  # Lance master image casting
                                'a': "normal", 's': "normal", 'd': "normal", 'f': "normal"}
        if self.current_class == "Gunslinger":
            self.skills_dict = {'q': "normal", 'w': "none", 'e': "none", 'r': "none",     # Gunslinger image casting
                                'a': "holding", 's': "combo", 'd': "normal", 'f': "combo"}
        if self.current_class == "Scrapper":
            self.skills_dict = {'q': "normal", 'w': "combo", 'e': "combo", 'r': "normal",  # Scrapper image casting
                                'a': "normal", 's': "normal", 'd': "normal", 'f': "normal"}
        if self.current_class == "Arcana":
            self.skills_dict = {'q': "combo", 'w': "normal", 'e': "normal", 'r': "Holding",  # Arcana image casting
                                'a': "combo", 's': "normal", 'd': "combo", 'f': "combo"}
        if self.current_class == "Artillerist":
            self.skills_dict = {'q': "normal", 'w': "combo", 'e': "normal", 'r': "normal",  # Artillerist image casting
                                'a': "holding", 's': "normal", 'd': "normal", 'f': "normal"}

        if self.current_work == "2_daily_chaos":
            self.two_chaos.set()
        else:
            self.two_chaos.clear()

        print("startin COMBAT")
        print(char_name)
        process = Thread(target=self.state_check, args=(char_name,))
        process.start()

    def combat(self):
        # NEW WAY OF CASTING SKILS
        self.skill_processes.append(
            Thread(target=self.skills)
            # multiprocessing.Process(target=self.skills, args=key)
             )
        # # print(self.Skillsdict)
        # for key in self.skills_dict:
        #     print(key)
        #     self.skill_processes.append(
        #         Thread(target=self.skills, args=key)
        #         # multiprocessing.Process(target=self.skills, args=key)
        #     )
        for process in self.skill_processes:
            print('starting combat')
            process.start()

    def start_combat(self):
        for process in self.combat_processes:
            print('START combat')
            process.start()
        for process in self.normal_processes:
            print('START normal', process)
            process.start()

    def stop_all(self):
        self.all_event.set()
        self.combat_event.set()
        self.normal_event.set()
        for process in self.all_processes:
            process.join()
        for process in self.combat_processes:
            process.join()
        for process in self.skill_processes:
            process.join()
        for process in self.normal_processes:
            process.join()

    def stop_combat(self):
        print("STOPING COMBAT")
        self.combat_event.set()
        for process in self.combat_processes:
            process.join()
        for process in self.skill_processes:
            process.join()

    def stop_normal(self):
        print("STOPING NORMAL")
        self.normal_event.set()
        for process in self.normal_processes:
            process.join()

    def skills(self):
        minutes = 5
        # numbofskills = round(minutes * 60 / self.skills_dict[key])
        # NEW APROACHes
        while not self.combat_event.is_set():
            print("STARTED COMBAT SKILLS")
            casting_skills(self.skills_dict, self.current_class)

        # while not self.combat_event.is_set():
        # # for i in range(0, numbofskills, 1):
        #     pydirectinput.press('' + key)
        #     time.sleep(0.15)
        #     pydirectinput.press('' + key)
        #     time.sleep(self.skills_dict[key])
        #     # this IF makes no sense but need it
        #     # if not self.combat_event.is_set():
        #     #     print("CLICKING LEFT ", key, self.combat_event.is_set())
        #     #     pydirectinput.leftClick()

    def __getstate__(self):
        state = {}
        for key, value in vars(self).items():
            if key != '_processes':
                state[key] = value
        return state


class skills(object):
    def __init__(self, hotkey, skill_type, priority=None, cooldown=None):
        self.hotkey = hotkey
        self.skill_type = skill_type
        self.priority = priority or {}
        self.cooldown = cooldown or {}

    def setGrade(self, hotkey, cooldown):
        self.grades[hotkey] = cooldown

    def getGrade(self, hotkey):
        return self.grades[hotkey]

    def getGPA(self):
        return list(self.cooldown.keys())[0]
# Define some students
# skill_1 = skills("q", "holding", "high", {"math":3.3})
# skill_2 = skills("Jane", 12, "female", 6, {"math": 3.5})


if __name__ == '__main__':
    """Weekly quests??? Abyssal dungeons , SENDING DISPATCH?
    RELOGING from character 2 character-> maybe just lopangs into ALT accounts?
    CHECKLIST WHAT TASK IS COMPLETE
    COMPLETELY finished functions: LOPANG ,  
    DEVELOP SOFTWARE THAT RECORDS MACROS PERFECTLY!
    ERRORS: Swamp keeps finding complete quest and instantly starts teleporting"""

    # stronghold_daily()
    # daily_state_check()
    # ChaosDungeon().minimap_detection()
    # ChaosDungeon().centeral_detection()

    # waiting_for_loading_screen()
    # accepting_quest(name="ALL", target="guild_request")

    # list_of_workers = ["Sheeeshaa", "Ggwarlord", "Ggsorc"]
    # finished_char = []
    # switching_char(finished_char, list_of_workers)

    # listmanager = Manager()
    # normal_processes = listmanager.list()
    # combat_processes = listmanager.list()
    # all_processes = listmanager.list()
    # # THIS IS NOT WORKING
    #
    # n_processes, c_processes, xzy = \
    #     processing_task(daily_state_check, normal_processes, combat_processes, all_processes)
    # print("PRINTING THSI SHIT and sleeping", all_processes)
    # print("PRINTING THSI SHIT and sleeping", n_processes, c_processes, xzy)
    #
    # keyboard.add_hotkey('ctrl+shift+q', kill_all(a_processes=xzy))

    # kill_all(all_processes)


    # for i in range(1,10,1):
    #     time.sleep(1)
    #     print(i)
    # try:
    #     processing_task(daily_state_check)
    # except keyboard.is_pressed('p'):
    #     os._exit(0)

        # print("closing...")
    # daily_state_check()
    # switching_char()
    # guild_daily()
    # print(combat)
    # bifrost_teleportation("Wailling Swamp")
    # Executing  the program
    # hope_daily()
    # swamp_daily()
    # nameless_daily()
    # hypnos_daily()
    # lopang_daily()
    # payto_daily()
