import threading
import pydirectinput
import METHODS
from Lifeskills import fishing
from datetime import datetime, timedelta
import numpy as np
import re
import pyautogui
import time
import glob
lock = threading.Lock()

# DAILY THINGS THAT CAN BE DONE
# Ghost ship , World boss , Chaos gate , ISLAND


def calculate_weekly(current_character):
    current_date = datetime.now()
    set_date = datetime(2022, 8, 3, 12, 0, 0)  # Setting hour and day of the week for weekly to calculate
    c = current_date - set_date
    current_week = int(c.days/7)
    # minutes = c.total_seconds() / 60
    # hours = minutes / 60
    # print("Number of days:", c.days)
    # print("Number of weeks:", int(hours/168)) # 7 days = 168 h
    try:
        last_week = METHODS.configparser.get(current_character, 'Last_week')
    except:
        METHODS.configparser.add_section(current_character)
        METHODS.configparser.set(current_character, 'Last_week', current_week)
        last_week = METHODS.configparser.get(current_character, 'Last_week')

    print(current_week, last_week)
    if current_week > int(last_week):
        # INSERT THINGS TO DO HERE
        # Accept weeklies ...
        accepting_quest("ALL", target="weekly")
        time.sleep(3)
        accepting_quest("ALL", target="guild_request")

        print("Accepting weeklies")
        METHODS.configparser.set(current_character, 'Last_week', current_week)
    METHODS.configparser.write()


def daily_state_check():
    # starting time MESURING
    stopwatch_start = time.time()
    # TASKS -> LOGIN -> CHECKLIST ->
    switch = 0
    finished_char = []
    METHODS.configparser.read("myapp.ini")
    for name, value in METHODS.configparser.items("Workers"):
        if value == "yes":
            METHODS.list_of_workers.append(name.capitalize())
    for name, value in METHODS.configparser.items("Finished_Characters"):
        if value == "yes":
            finished_char.append(name.capitalize())
    print("WORKERS", METHODS.list_of_workers)
    print("FINISHED CHAR :", finished_char)
    # METHODS.list_of_workers = [ # Huge error in all mouve movement/clicks not detected all the time
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
    for x in METHODS.list_of_workers:
        total_tasks = total_tasks + 1

    # SWITCHING TO CHAOS BUILD WHILE DOING THINGS?
    METHODS.focus_window('LOST ARK')
    time.sleep(1)

    # character list
    while switch == 0:
        unmounting = METHODS.Buttons + "Daily Quest\\Misc\\Mounted_icon.png"
        pos = METHODS.im_search(unmounting, x1=round(METHODS.Resolution[0]/3), y1=630,
                                x2=607, y2=400, precision=0.8)
        if pos != [-1, -1]:
            pydirectinput.press("r")
            print("UNMOUNTED!")
        # 549 646
        # 747 672
        lifeskill_menu = METHODS.Buttons + "Fishing\\OPENSkills\\Lifeskill_backpack.png"
        pos = METHODS.im_search(lifeskill_menu,
                                x1=round(METHODS.Resolution[0]/3), y1=680, x2=607, y2=400, precision=0.5)
        time.sleep(1)
        if pos != [-1, -1]:
            pydirectinput.press("b")
            print("closed LIFESKILL menu!")
        # # Closing chat
        minimzed = METHODS.Buttons + "\\Daily Quest\\Misc\\Chat_minimized.png"
        pos = METHODS.search_click_image(minimzed, action="left",
                                 x1=0, y1=500, x2=700, y2=500, precision=0.6)
        if pos == [-1, -1]:
            minimize_chat = METHODS.Buttons + "\\Daily Quest\\Misc\\Minimize_chat.png"
            METHODS.search_click_image(minimize_chat, action="left",
                               x1=0, y1=500, x2=700, y2=500, precision=0.6)
            print("Chat minimized")
        # Opening ESC Game menu
        pydirectinput.press('ESC')
        time.sleep(1)
        for i in range(1, 10, 1):
            ready = METHODS.im_search(METHODS.esc_menu, precision=0.75)
            if ready != [-1, -1]:
                break
            else:
                time.sleep(1.5)
                i += 1
                pydirectinput.press('ESC')
        print(METHODS.Resolution)
        # button = METHODS.Daily + "Misc\\Switching\\switch_character.png"
        # switch_btn_pos = METHODS.im_search(button, x2=1800)
        # print(switch_btn_pos)
        # IMPORTANT for using 2 methods/colors to find match with tesseract
        if METHODS.Resolution == [2560, 1080]:
            there_is_no_hope_x = round(METHODS.Resolution[0]/100*24.6)  # 630 656
            there_is_no_hope_y = round(METHODS.Resolution[1]/100*60.7)
            print(there_is_no_hope_x, there_is_no_hope_y)
            no_hope_y2 = 25
        if METHODS.Resolution == [1874, 1080]:
            print("WAS HERE")
            there_is_no_hope_x = round(METHODS.Resolution[0]/100*24.6)  # 461 634
            there_is_no_hope_y = round(METHODS.Resolution[1]/100*58.7)
            print(there_is_no_hope_x, there_is_no_hope_y)
            no_hope_y2 = 21
        if METHODS.Resolution == [1372, 797]:
            # VERY HARD TO READ TEXT
            there_is_no_hope_x = round(METHODS.Resolution[0]/100*24.6)  # 461 634
            there_is_no_hope_y = round(METHODS.Resolution[1]/100*58.7)
            print(there_is_no_hope_x, there_is_no_hope_y)
            no_hope_y2 = 21
        if METHODS.Resolution == [1686, 1079]:
            # VERY HARD TO READ TEXT
            there_is_no_hope_x = round(METHODS.Resolution[0]/100*24.6)  # 415 623
            there_is_no_hope_y = round(METHODS.Resolution[1]/100*57.7)
            print(there_is_no_hope_x, there_is_no_hope_y)
            no_hope_y2 = 21

        text = METHODS.image2text(x1=there_is_no_hope_x, y1=there_is_no_hope_y,
                                  x2=200, y2=no_hope_y2, method=' --oem 3 --psm 7', colors="threshold")
        found_it = False
        
        for y in np.unique(METHODS.list_of_workers):
            if y in text:
                found_it = True
                print("FOUND IT USING THRESHOLD")
                break
        if not found_it:
            text = METHODS.image2text(x1=there_is_no_hope_x, y1=there_is_no_hope_y,
                                      x2=200, y2=no_hope_y2,
                                      method=' --oem 3 --psm 7')
            for y in np.unique(METHODS.list_of_workers):
                if y in text:
                    print("FOUND IT USING rgb")
                    break
        print("I was here ", text, METHODS.Resolution)
        # CLOSING ESC MENU
        pydirectinput.press('ESC')
        generator_expression = (x for x in np.unique(METHODS.list_of_workers) if x in text)
        for x in generator_expression:
            print("Found ", x, "")
            calculate_weekly(x)
            time.sleep(1)
            pet_status = "no"
            if x not in finished_char:
                # WHAT CLASS AM I? checking image and then XXX
                for f in METHODS.Class_checker:
                    # print(f)
                    # Tossing at Sentinel
                    what_class = METHODS.im_search(f, precision=0.8)
                    print(what_class)
                    if what_class != [-1, -1]:
                        split_string = f.rsplit('\\')[2]
                        print(split_string)
                        print("My CLASS is " + split_string)
                        if "Bard" in split_string:
                            METHODS.combat = "Bard"
                            break
                        elif split_string == "Paladin.png":
                            METHODS.combat = "Paladin"
                            break
                        elif split_string == "Arcana.png":
                            METHODS.combat = "Arcana"
                            break
                        elif split_string == "Lance_master.png":
                            METHODS.combat = "Lance master"
                            break
                        elif split_string == "Lance_master2.png":
                            pydirectinput.press('z')
                            METHODS.combat = "Lance master"
                            break
                        elif split_string == "Gunlancer.png":
                            METHODS.combat = "Gunlancer"
                            break
                        elif split_string == "Sorceress.png":
                            METHODS.combat = "Sorceress"
                            break
                        elif split_string == "Deathblade.png":
                            METHODS.combat = "Deathblade"
                            break
                        elif split_string == "Scrapper.png":
                            METHODS.combat = "Scrapper"
                            break
                        elif split_string == "Soulfist.png":
                            METHODS.combat = "Soulfist"
                            break
                        elif split_string == "Artillerist.png":
                            METHODS.combat = "Artillerist"
                            break
                        elif split_string == "Striker.png":
                            METHODS.combat = "Striker"
                            break
                        elif split_string == "Gunslinger.png":
                            METHODS.combat = "Gunslinger"
                            break
                        else:
                            print("UNKNOWN CLASS")
                            exit()
                if METHODS.combat == '':
                    print("COMBAT NOT DEFINED")
                    exit()
                for section_name in METHODS.configparser.sections():
                    # option = METHODS.configparser.options(section_name)
                    if x == section_name:
                        work_array = []
                        for name, value in METHODS.configparser.items(section_name):
                            # config_name = name
                            # config_value = value
                            if value == "yes":
                                work_array.append(name)
                        print("WORK FOR ", x, " : ", work_array)
                        gen_expression = (x for x in work_array if "all_stronghold" in x)
                        for g in gen_expression:
                            current_work = "Stronghold"
                            stronghold_daily()
                        gen_expression = (x for x in work_array if "pet_status" in x)
                        for g in gen_expression:
                            pet_status = "yes"
                        gen_expression = (x for x in work_array if "preset" in x)
                        for g in gen_expression:
                            current_work = "Changing preset"
                            found = re.findall(r'\d+', g)
                            integrated_presets(int(found[0]))
                        gen_expression = (x for x in work_array if "guild_silver" in x)
                        for g in gen_expression:
                            current_work = "Guild"
                            guild_daily()
                        gen_expression = (x for x in work_array if "all_silver" in x)
                        for g in gen_expression:
                            current_work = "Silver Dailies"
                            accepting_quest("ALL")
                            lopang_daily()
                        gen_expression = (x for x in work_array if "all_leapstone" in x)
                        for g in gen_expression:
                            current_work = "Leapstone Dalies"
                            accepting_quest("ALL")
                            hope_daily()
                            swamp_daily()
                            nameless_daily()
                        gen_expression = (x for x in work_array if "fishing" in x)
                        for g in gen_expression:
                            current_work = "Fishing"
                            fishing()
                        gen_expression = (x for x in work_array if "2_daily_chaos" in x)
                        for g in gen_expression:
                            current_work = "Chaos Dungeon"
                            import Battle_CD
                            Battle_CD.ChaosDungeon().start(x, METHODS.combat, work="2_daily_chaos")
                            # ChaosDungeon().start(x, METHODS.combat, work="2_daily_chaos")
                            switch = 1
                            break
                        # finished_char.append(x)
                        print("FINISHED THIS CHARACTER:", x)
                        METHODS.configparser.set("Finished_Characters", x, "yes")
                        METHODS.configparser.write()

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
                  + " / WORKER LIST len : ", len(np.unique(METHODS.list_of_workers)))
            if total_finished >= len(np.unique(METHODS.list_of_workers)):
                print("TURNING SWITCH OFF")
                switch = 1
                break
            print("Character not in worker list. Re-logging...")
            switching_char(finished_char)

        # total_finished = len(np.unique(finished_char))
        # print(total_finished, " = TOTAL FINISHED finished_char= "
        #       + str(finished_char) + " / WORKER LIST len : ", len(METHODS.list_of_workers))
        # if total_finished == 0 and finished_char == []:
        #     print("CHARACTER NOT ON LIST OF WORKERS")
        #     exit()

        # switching CHar
        # switching_char(finished_char)
        # FINiSHED ALL IF statement

    print("Finished METHODS.Daily maybe waiting for chaos...")
    METHODS.stop_count = "yes"
    # stopwatch_end = time.time()
    # global execution_time
    # execution_time = stopwatch_end - stopwatch_start
    # global total_time
    # total_time += execution_time
    # print(f"Runtime of the program is {execution_time} and TOTAL is {total_time}")


def integrated_presets(chosen_preset=1):
    # SWITCHING TO SPECIFIC BUILD
    presets = METHODS.Daily + "Misc\\integrated_preset.png"
    apply = METHODS.Daily + "Misc\\apply_preset.png"
    for i in range(1, 10, 1):
        print("choosing preset")
        pydirectinput.keyDown('alt')
        time.sleep(0.3)
        pydirectinput.press('e')
        time.sleep(0.2)
        pydirectinput.keyUp('alt')

        ready = METHODS.im_search(presets, 1, precision=0.84)
        if ready != [-1, -1]:
            if chosen_preset == 1:
                pydirectinput.click(ready[0] - 50,
                                    ready[1] + 57)
                time.sleep(1)
                apply_preset = METHODS.im_search(apply, 1, precision=0.84)
                pydirectinput.click(apply_preset[0],
                                    apply_preset[1])
                break
            elif chosen_preset == 2:
                pydirectinput.click(ready[0],
                                    ready[1] + 57)
                time.sleep(1)
                apply_preset = METHODS.im_search(apply, 1, precision=0.84)
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
    METHODS.focus_window('LOST ARK')
    # # BIFROST FUNCTIOn
    bifrost_teleportation("Wailling Swamp")
    waiting_for_loading_screen()
    # TESTING While loop for searching of the giant
    switch = 0
    while switch == 0:
        pydirectinput.moveTo(round(METHODS.Resolution[0] / 2),
                             round(METHODS.Resolution[1] / 4 * 3))
        pydirectinput.press('F5')
        time.sleep(0.7)
        pydirectinput.press('F5')
        complete_quest = METHODS.Daily + "Walling Swamp\\Finished\\Completed_quest.png"
        complete = METHODS.im_search(complete_quest, 1, precision=0.87)
        if complete != [-1, -1]:
            print("finished quest")
            switch = 1
            break
    # OLD METHOD
    # while switch == 0:
    #     pydirectinput.moveTo(METHODS.Resolution[0]/2,
    #                          METHODS.Resolution[1]/4*3)
    #     pydirectinput.press('F5')
    #     time.sleep(0.7)
    #     pydirectinput.press('F5')
    #
    #     for f in METHODS.DailySwamp:
    #         # Tossing at Sentinel
    #         complete_quest = METHODS.Daily + "Walling Swamp\\Finished\\Completed_quest.png"
    #         print(f)
    #         ready = METHODS.im_search(f, precision=0.65)
    #         complete = METHODS.im_search(complete_quest, 1, precision=0.87)
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
        time.sleep(1.5)
        pydirectinput.click(round(METHODS.Resolution[0] / 2),
                            round(METHODS.Resolution[1] / 2), button="right")
        time.sleep(0.7)
        turn_in = METHODS.Daily + "Walling Swamp\\Navigation\\Kalaja.png"
        turning = METHODS.im_search_until_found(turn_in, precision=0.83)
        pydirectinput.click(turning[0],
                            turning[1])
        time.sleep(0.7)
        turn_in = METHODS.Daily + "Walling Swamp\\Navigation\\Teleport.png"
        turning = METHODS.im_search_until_found(turn_in, precision=0.90)
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
    time.sleep(1)
    pydirectinput.click(700,
                        300, button="right")
    # FAIL SAFE
    fail_safe_faiton()

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
    METHODS.focus_window('LOST ARK')
    pydirectinput.press('g')
    time.sleep(1)
    pydirectinput.press('g')
    time.sleep(1)
    pydirectinput.press('g')
    time.sleep(1)
    hypno_ready = METHODS.Buttons + "\\Daily Quest\\Hypnos\\im_ready.png"
    ready = METHODS.im_search(hypno_ready, 1, precision=0.9)
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
    hypno_enter = METHODS.Buttons + "\\Daily Quest\\Hypnos\\Enter.png"
    enter = METHODS.im_search(hypno_enter, 1, precision=0.9)
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
    hypno_accept = METHODS.Buttons + "\\Daily Quest\\Hypnos\\Accept.png"
    accept = METHODS.im_search(hypno_accept, 1, precision=0.9)
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
    METHODS.focus_window('LOST ARK')
    time.sleep(1)
    pydirectinput.press('m')
    time.sleep(0.7)
    turn_in = METHODS.Daily + "Nameless Valley\\Navigation\\Teleport_nameless_valley.png"
    turning = METHODS.im_search(turn_in, 1, precision=0.90)
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
    step_1 = METHODS.Daily + "Nameless Valley\\Finished\\1_out_of_2.png"
    step = METHODS.im_search(step_1, 1, precision=0.90)
    while step == [-1, -1]:
        fight_mobs(METHODS.combat)
        time.sleep(1)
        pydirectinput.press('g')
        time.sleep(3.5)
        step = METHODS.im_search(step_1, 1, precision=0.90)
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
    step_2 = METHODS.Daily + "Nameless Valley\\Finished\\Finally_complete.png"
    step = METHODS.im_search(step_2, 1, precision=0.90)
    while step == [-1, -1]:
        fight_mobs(METHODS.combat)
        time.sleep(1)
        pydirectinput.press('g')
        time.sleep(3.7)
        step = METHODS.im_search(step_2, 1, precision=0.90)
    teleported = "no"
    while teleported != "yes":
        fight_mobs(METHODS.combat)
        time.sleep(1)
        # teleporting
        print("completed quest")
        pydirectinput.press('m')
        time.sleep(1.5)
        pydirectinput.click(round(METHODS.Resolution[0] / 2),
                            round(METHODS.Resolution[1] / 2), button="right")
        time.sleep(0.7)
        turn_in = METHODS.Daily + "Walling Swamp\\Navigation\\Kalaja.png"
        turning = METHODS.im_search_until_found(turn_in, precision=0.82)
        pydirectinput.click(turning[0],
                            turning[1])
        time.sleep(0.7)
        turn_in = METHODS.Daily + "Walling Swamp\\Navigation\\Teleport.png"
        turning = METHODS.im_search_until_found(turn_in, precision=0.90)
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
    time.sleep(1)
    pydirectinput.click(700,
                        300, button="right")
    # FAIL SAFE
    fail_safe_faiton()

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
    METHODS.focus_window('LOST ARK')
    time.sleep(1)
    # Closing CHAT !!! CAN POSSIBLY CLOSE MINIMAP
    chat = METHODS.Daily + "Misc\\Minimize_chat.png"
    # ERROR WITH FUNCTION WHEN INSERTING COSTUM region for searching!!!!!
    METHODS.search_click_image(chat, "left", x1=0, y1=710, x2=600, y2=1050)
    METHODS.search_click_image(chat, "left", x1=0, y1=710, x2=600, y2=1050)
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
    METHODS.focus_window('LOST ARK')
    time.sleep(1)
    pydirectinput.keyDown('alt')
    time.sleep(0.2)
    pydirectinput.press('u')
    time.sleep(0.2)
    pydirectinput.keyUp('alt')
    time.sleep(2)
    arrow_tab_left = METHODS.Daily + "Misc\\Guild_tabs_left.png"
    METHODS.search_click_image(arrow_tab_left, "left")
    time.sleep(0.2)
    METHODS.search_click_image(arrow_tab_left, "left")
    time.sleep(0.4)
    overview_tab = METHODS.Daily + "Misc\\Guild_overview.png"
    METHODS.search_click_image(overview_tab, "left")
    # Getting rid of first time notification
    first_login = METHODS.Daily + "Misc\\First_loging_guild.png"
    METHODS.search_click_image(first_login, "left")
    # Guild donations
    guild_donation = METHODS.Daily + "Guild\\Guild_donation.png"
    METHODS.search_click_image(guild_donation, "left")
    time.sleep(0.4)
    # Donating silver
    silver = METHODS.Buttons + "\\Daily Quest\\Guild\\Donate_silver.png"
    ready = METHODS.im_search(silver, 1, precision=0.82)
    if ready != [-1, -1]:
        pydirectinput.click(ready[0]+25,
                            ready[1]+150)
        time.sleep(0.4)
    small_close = METHODS.Daily + "Misc\\Guild_small_close.png"
    METHODS.search_click_image(small_close, "left", x1=METHODS.Resolution[0]/2, y1=150, x2=500, y2=200)
    time.sleep(0.4)
    # Research normal SUPPORT
    support_research = METHODS.Daily + "Guild\\Support_research.png"
    research = METHODS.Daily + "Guild\\Normal.png"
    ok = METHODS.Daily + "Guild\\ok.png"
    METHODS.search_click_image(support_research, "left")
    time.sleep(0.2)
    METHODS.search_click_image(research, "left")
    time.sleep(3.5)
    METHODS.search_click_image(ok, "left")
    time.sleep(0.2)
    pydirectinput.keyDown('alt')
    time.sleep(0.2)
    pydirectinput.press('u')
    time.sleep(0.2)
    pydirectinput.keyUp('alt')
    time.sleep(2)


def payto_daily():
    METHODS.focus_window('LOST ARK')
    time.sleep(1)
    pydirectinput.click(1903,
                        544, button="right")
    time.sleep(10)
    pydirectinput.press('m')
    time.sleep(0.2)
    pydirectinput.click(1903,
                        544, button="right")
    time.sleep(1)
    rive_row = METHODS.Daily + "Peyto\\Rivelry_row.png"
    METHODS.search_click_image(rive_row, "left")
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
    turtle = METHODS.Daily + "Peyto\\Turtle.png"
    METHODS.search_click_image(turtle, "left")
    time.sleep(0.7)
    pydirectinput.keyDown('alt')
    time.sleep(0.2)
    pydirectinput.click(1452,
                        487, button="left")
    time.sleep(0.2)
    pydirectinput.keyUp('alt')
    time.sleep(150)
    sea_anchor = METHODS.Daily + "Peyto\\Anchor.png"
    METHODS.search_click_image(sea_anchor, "right")
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
    tortoy = METHODS.Daily + "Peyto\\Tortoy.png"
    METHODS.search_click_image(tortoy, "left")
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
    ongoing = METHODS.Daily + "Peyto\\Ongoing_quest.png"
    METHODS.search_click_image(ongoing, "left")
    complete = METHODS.Daily + "Peyto\\Complete.png"
    METHODS.search_click_image(complete, "left")


def hope_daily():
    METHODS.focus_window('LOST ARK')
    time.sleep(1)
    # Teleporting to the place
    bifrost_teleportation("Hope island")
    waiting_for_loading_screen()
    # Fighting spiders until quest complete
    switch = 0
    while switch == 0:
        for f in METHODS.DailySwamp:
            # Tossing at Sentinel
            complete_quest = METHODS.Daily + "Hope Island\\Finished\\Hope_complete.png"
            complete = METHODS.im_search(complete_quest, 1, precision=0.90)
            fight_mobs(METHODS.combat)
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
    for k in METHODS.fail_safe_hope:
        METHODS.search_click_image(k, "right", precision=0.77)
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
    # quest_giver = METHODS.Daily + "Hope Island\\Finished\\quest_giver.png"
    # # METHODS.search_click_image(quest_giver, "right", precision=0.6)
    # ready = METHODS.im_search(quest_giver, 1, precision=0.9)
    # if ready != [-1, -1]:
    #     # ready = METHODS.im_search(quest_giver, 1, precision=0.8)
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
    METHODS.focus_window('LOST ARK')
    time.sleep(1)
    pydirectinput.keyDown('alt')
    time.sleep(0.2)
    pydirectinput.press('j')
    time.sleep(0.2)
    pydirectinput.keyUp('alt')
    time.sleep(1.5)
    if target == "daily":
        daily_button = METHODS.Daily + "Misc\\Daily_button.png"
        METHODS.search_click_image(daily_button, "left")
        time.sleep(1)
        menu = METHODS.Daily + "Misc\\menu.png"
        METHODS.search_click_image(menu, "left")

        favorites = METHODS.Daily + "Misc\\Favorites.png"
        METHODS.search_click_image(favorites, "left")
        if name == "ALL":
            accept_all = METHODS.Daily + "Misc\\Accept_quest.png"
            METHODS.im_search(accept_all, action="left", click="all")

        if name == "Wailling Swamp":
            swamp = METHODS.Daily + "Walling Swamp\\Accepting\\Accepting_swamp.png"
            ready = METHODS.im_search(swamp, precision=0.82)
            if ready != [-1, -1]:
                pydirectinput.click(ready[0] + 855,
                                    ready[1] + 18)
        elif name == "Nameless Valley":
            nameless = METHODS.Daily + "Nameless Valley\\Accepting\\Accepting_nameless.png"
            ready = METHODS.im_search(nameless, precision=0.82)
            if ready != [-1, -1]:
                pydirectinput.click(ready[0] + 855,
                                    ready[1] + 18)
        elif name == "Hope Island":
            hope = METHODS.Daily + "Hope Island\\Accepting\\Accepting_Hope.png"
            ready = METHODS.im_search(hope, precision=0.82)
            if ready != [-1, -1]:
                pydirectinput.click(ready[0] + 855,
                                    ready[1] + 18)
    if target == "weekly":
        daily_button = METHODS.Daily + "Misc\\Weekly_button.png"
        METHODS.im_search(daily_button, action="left", click="yes")
        time.sleep(0.1)
        daily_button = METHODS.Daily + "Misc\\Weekly_button2.png"
        METHODS.im_search(daily_button, action="left", click="yes")
        time.sleep(1)
        menu = METHODS.Daily + "Misc\\menu.png"
        METHODS.im_search(menu, action="left", click="yes")

        favorites = METHODS.Daily + "Misc\\Favorites.png"
        METHODS.im_search(favorites, action="left", click="yes")
        if name == "ALL":
            accept_all = METHODS.Daily + "Misc\\Accept_quest.png"
            METHODS.im_search(accept_all, action="left", click="all")

    if target == "guild_request":
        guild_request_button = METHODS.Daily + "Misc\\Guild_request_button.png"
        METHODS.im_search(guild_request_button, action="left", click="yes")
        time.sleep(0.1)
        guild_request_button = METHODS.Daily + "Misc\\Guild_request_button2.png"
        METHODS.im_search(guild_request_button, action="left", click="yes")
        # could be difficult to do
        for w in METHODS.weekly_tasks:
            guild_req_right = METHODS.Daily + "Misc\\Guild_request_far_right.png"
            METHODS.im_search(guild_req_right, action="left", click="yes", precision=0.8)
            position = METHODS.im_search(w, precision=0.90)
            if position != [-1, -1]:
                pydirectinput.leftClick(position[0] + 550,
                                        position[1] + 10)
                time.sleep(2)
                break
        for x in range(0, 2, 1):
            for w in METHODS.weekly_tasks:
                guild_req_left = METHODS.Daily + "Misc\\Guild_request_far_left.png"
                METHODS.im_search(guild_req_left, action="left", click="yes")
                position = METHODS.im_search(w, precision=0.90)
                if position != [-1, -1]:
                    pydirectinput.leftClick(position[0] + 550,
                                            position[1] + 10)
                    time.sleep(2)
                    break
    time.sleep(1)
    pydirectinput.keyDown('alt')
    time.sleep(0.2)
    pydirectinput.press('j')
    time.sleep(0.2)
    pydirectinput.keyUp('alt')
    # STOP TRACKING THE QEUSTS
    if target == "guild_request" or target == "weekly":
        time.sleep(1)
        pydirectinput.press('j')
        stop_tracking = METHODS.Daily + "Misc\\Weekly_Stop_tracking.png"
        METHODS.im_search(stop_tracking, action="left", click="all", precision=0.8)
        time.sleep(0.5)
        pydirectinput.press('j')


def bifrost_teleportation(name):
    time.sleep(1)
    # Looks for Bifrost button
    bifrost = METHODS.Daily + "Misc\\BIFROST.png"
    bifrost_pos = METHODS.im_search(bifrost, 1, precision=0.87)
    if bifrost_pos != [-1, -1]:
        pydirectinput.click(bifrost_pos[0],
                            bifrost_pos[1])
    else:
        print("cannot find BIFROST button")
        exit()
    precision = 0.90
    time.sleep(1)
    # Looks for name of map of Bifrost
    if name == "Wailling Swamp":
        swamp = METHODS.Daily + "Walling Swamp\\Bifrost\\Swamp.png"
        ready = METHODS.im_search(swamp, 1, precision=precision)
        if ready != [-1, -1]:
            # Clicking position to the right of it where Move button is
            pydirectinput.click(ready[0] + 400,
                                ready[1])
    elif name == "Hope island":
        hope = METHODS.Daily + "Hope island\\Bifrost\\BIFROST_hope.png"
        ready = METHODS.im_search(hope, 1, precision=precision)
        if ready != [-1, -1]:
            # Clicking position to the right of it where Move button is
            pydirectinput.click(ready[0] + 400,
                                ready[1])
    elif name == "lopang":
        lopang = METHODS.Daily + "Lopang\\Bifrost\\BIFROST_lopang.png"
        ready = METHODS.im_search(lopang, 1, precision=0.91)  # 95 HAD SOME ERRORS teleporting to wrong
        if ready != [-1, -1]:
            # Clicking position to the right of it where Move button is
            pydirectinput.click(ready[0] + 400,
                                ready[1])
    elif name == "lopang_arthentine":
        lopang_art = METHODS.Daily + "Lopang\\Bifrost\\BIFROST_Arthentine.png"
        ready = METHODS.im_search(lopang_art, 1, precision=precision)
        if ready != [-1, -1]:
            # Clicking position to the right of it where Move button is
            pydirectinput.click(ready[0] + 400,
                                ready[1])
    elif name == "lopang_vern":
        lopang_vern = METHODS.Daily + "Lopang\\Bifrost\\BIFROST_Vern.png"
        ready = METHODS.im_search(lopang_vern, 1, precision=precision)
        if ready != [-1, -1]:
            # Clicking position to the right of it where Move button is
            pydirectinput.click(ready[0] + 400,
                                ready[1])
    elif name == "lopang_shushire":
        lopang_shushire = METHODS.Daily + "Lopang\\Bifrost\\BIFROST_Shushire.png"
        ready = METHODS.im_search(lopang_shushire, 1, precision=precision)
        if ready != [-1, -1]:
            # Clicking position to the right of it where Move button is
            pydirectinput.click(ready[0] + 400,
                                ready[1])
    else:
        print("ERROR: Unknown BIFROST location")

    # checking if its asking for crystals to teleport TIME SLEEP NEEDED
    time.sleep(1)
    crystalcheck = METHODS.Daily + "Misc\\Cost_for_BIFROST.png"
    pos_crystal = METHODS.im_search(crystalcheck, precision=precision)
    time.sleep(1)
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
        pydirectinput.moveTo(round(METHODS.Resolution[0] / 2),
                             round(METHODS.Resolution[1] / 2))
        time.sleep(1)
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
        pydirectinput.moveTo(round(METHODS.Resolution[0]/2),
                             round(METHODS.Resolution[1]/2))
        pydirectinput.press('w')
        time.sleep(0.3)
        pydirectinput.press('w')
        time.sleep(0.5)
        pydirectinput.press('e')
        time.sleep(0.3)
        pydirectinput.press('e')
        time.sleep(2)
    if class_name == "Arcana":
        pydirectinput.moveTo(round(METHODS.Resolution[0] / 2),
                             round(METHODS.Resolution[1] / 2))
        pydirectinput.press('s')
        time.sleep(1)
        pydirectinput.press('f')
        time.sleep(0.3)
        pydirectinput.press('f')
        time.sleep(2)
    if class_name == "Deathblade":
        pydirectinput.moveTo(round(METHODS.Resolution[0] / 2),
                             round(METHODS.Resolution[1] / 2))
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


def switching_char(finished_char):
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
        ready = METHODS.im_search(METHODS.esc_menu, 1, precision=0.84)
        if ready != [-1, -1]:
            break
        else:
            i += 1
            pydirectinput.press('ESC')
            time.sleep(1)

    button = METHODS.Daily + "Misc\\Switching\\switch_character.png"
    METHODS.search_click_image(button, "left", x2=1800)
    went_down = 0
    went_up = 0
    while went_up == 0:
        button = METHODS.Daily + "Misc\\Switching\\button_down.png"
        METHODS.search_click_image(button, "left", x2=1800)

        if went_down == 1:
            button = METHODS.Daily + "Misc\\Switching\\button_up.png"
            METHODS.search_click_image(button, "left")
            first_x = 692
            first_y = 400
        # formula for going through all 9 characters
        for i in range(0, char_loop, 1):
            count = count + 1
            # print(count)
            # print(char_loop)
            # count devideable by 3
            first_x = first_x + switch_stepx
            text = METHODS.image2text(x1=first_x, y1=first_y,
                                      x2=box_size_x, y2=box_size_y)
            print(text)

            generator_expression = (x for x in METHODS.list_of_workers if x not in finished_char)
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
    teleport = "no"
    for i in range(0, tries, 1):
        print("looking for black")
        count_loading = count_loading + 1
        im = pyautogui.screenshot(region=(1652, 168, 240, 210))
        r, g, b = im.getpixel((1772 - 1652, 272 - 168))
        if r == 0 and g == 0 and b == 0:
            break
        time.sleep(0.07)
    # if count_loading == tries:
    #     print("Loading screen not found")
    # else:
    # print("Loading screen found")
    # looking for light
    for i in range(0, 20, 1):
        print("looking for ARROW")
        loading_arrow = METHODS.Buttons + "\\Daily Quest\\Misc\\Loading_screen_arrow.png"
        position = METHODS.im_search(loading_arrow, precision=0.85)
        if position != [-1, -1]:
            teleport = "yes"
            break
        time.sleep(0.3)
    if teleport == "yes":
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
    METHODS.focus_window('LOST ARK')
    time.sleep(0.5)
    pydirectinput.press('F2')
    time.sleep(0.5)
    song = METHODS.Daily + "Stronghold\\stronghold_song.png"
    METHODS.search_click_image(song, "left")
    play_song = METHODS.Daily + "Misc\\song_play.png"
    METHODS.search_click_image(play_song, "left")
    # song cast + loading screen
    waiting_for_loading_screen()
    # to avoid talking bich on start time sleep or input
    time.sleep(3)
    pydirectinput.leftClick(round(METHODS.Resolution[0]/2),
                            round(METHODS.Resolution[1]/2)+200)

    pydirectinput.keyDown('ctrl')
    time.sleep(0.3)
    pydirectinput.press('1')
    time.sleep(0.2)
    pydirectinput.keyUp('ctrl')
    time.sleep(1)
    gold_anchor = METHODS.Daily + "Stronghold\\Gold_anchor.png"
    METHODS.search_click_image(gold_anchor, "left")
    for i in range(0, 4, 1):
        time.sleep(1)
        mission_complete = METHODS.Daily + "Stronghold\\mission_complete.png"
        METHODS.search_click_image(mission_complete, "left", precision=0.77)
        time.sleep(1)
        mission_results = METHODS.Daily + "Stronghold\\Mission_result.png"
        METHODS.search_click_image(mission_results, "left", precision=0.8)
        time.sleep(2)
        ok_button = METHODS.Daily + "Stronghold\\ok_button.png"
        METHODS.search_click_image(ok_button, "left", precision=0.8)
    time.sleep(1)
    # Needs clicking on missions part
    for c in METHODS.chosen_missions:
        # clicking on mission
        print(c)
        METHODS.search_click_image(c, "left")
        repair = METHODS.Daily + "Stronghold\\Repair.png"
        METHODS.search_click_image(repair, "left", precision=0.8)
        print("trying to click repair")
        time.sleep(1)
        btn_ship_repair = METHODS.Daily + "Stronghold\\button_ship_repair.png"
        METHODS.search_click_image(btn_ship_repair, "left", precision=0.8)
        print("trying to click SHIP repair")
        time.sleep(1)
        auto_formation = METHODS.Daily + "Stronghold\\auto_formation.png"
        METHODS.search_click_image(auto_formation, "left")
        time.sleep(1)
        mission_start = METHODS.Daily + "Stronghold\\mission_start.png"
        METHODS.search_click_image(mission_start, "left")
        time.sleep(1)
        ok_button = METHODS.Daily + "Stronghold\\mission_start.png"
        METHODS.search_click_image(ok_button, "left")
        time.sleep(1)
        pydirectinput.press('ENTER')
    # Special missions
    time.sleep(1)
    special_mission = METHODS.Daily + "Stronghold\\Special_Mission.png"
    METHODS.search_click_image(special_mission, "left")
    # Completing missions
    for k in range(0, 2, 1):
        time.sleep(1)
        mission_complete = METHODS.Daily + "Stronghold\\mission_complete.png"
        pos = METHODS.im_search(mission_complete)
        if pos != [-1, -1]:
            METHODS.search_click_image(mission_complete, "left")
            time.sleep(1)
            mission_results = METHODS.Daily + "Stronghold\\Mission_result.png"
            METHODS.search_click_image(mission_results, "left")
            time.sleep(4)
            ok_button = METHODS.Daily + "Stronghold\\ok_button.png"
            METHODS.search_click_image(ok_button, "left")
        else:
            break
    # Sending on new ones
    for i in range(0, 2, 1):
        time.sleep(1)
        stronghold_yoho = METHODS.Daily + "Stronghold\\stronghold_yoho.png"
        METHODS.search_click_image(stronghold_yoho, "left")
        time.sleep(1)
        repair = METHODS.Daily + "Stronghold\\Repair.png"
        METHODS.search_click_image(repair, "left", precision=0.8)
        print("trying to click repair")
        time.sleep(1)
        btn_ship_repair = METHODS.Daily + "Stronghold\\button_ship_repair.png"
        METHODS.search_click_image(btn_ship_repair, "left", precision=0.8)
        print("trying to click SHIP repair")
        time.sleep(1)
        auto_formation = METHODS.Daily + "Stronghold\\auto_formation.png"
        METHODS.search_click_image(auto_formation, "left")
        mission_start = METHODS.Daily + "Stronghold\\mission_start.png"
        METHODS.search_click_image(mission_start, "left")
        time.sleep(1)
        ok_button = METHODS.Daily + "Stronghold\\mission_start.png"
        METHODS.search_click_image(ok_button, "left")
        pydirectinput.press('ENTER')

    # Harvest Farm
    time.sleep(1)
    farm_button = METHODS.Daily + "Stronghold\\Farm.png"
    METHODS.search_click_image(farm_button, "left")
    time.sleep(1)
    harvest_all = METHODS.Daily + "Stronghold\\Harvest_all.png"
    METHODS.search_click_image(harvest_all, "left", precision=0.8)
    time.sleep(1)
    check_ok = METHODS.Daily + "Stronghold\\check_ok.png"
    METHODS.search_click_image(check_ok, "left", precision=0.8)
    time.sleep(1)
    ok_button = METHODS.Daily + "Stronghold\\ok_button.png"
    METHODS.search_click_image(ok_button, "left", precision=0.8)
    time.sleep(4)
    # Repairing tools
    if METHODS.pet_status == "yes":
        pydirectinput.keyDown('alt')
        time.sleep(0.3)
        pydirectinput.press('p')
        time.sleep(0.2)
        pydirectinput.keyUp('alt')
        repair_tools = [x for x in glob.glob(METHODS.stronghold + '\\Repairing_tools' + "**/*.png")]
        for j in repair_tools:
            METHODS.search_click_image(j, "left")
            time.sleep(1)
        time.sleep(1)
        pydirectinput.press('ESC')
        time.sleep(0.7)
        pydirectinput.press('ESC')
    # Pet farm
    for c in METHODS.pet_ranch:
        METHODS.search_click_image(c, "left", precision=0.8)
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


def fail_safe_faiton():
    # FAIL SAFE
    success_log = open("success_log.txt", "a+")
    success_log.write("\r\n Good ones: \r\n")
    for k in METHODS.fail_proof_faiton:
        position = METHODS.search_click_image(k, "right", precision=0.68)
        time.sleep(0.9)
        if position != [-1, -1]:
            # ENTERING DATA INSIDE TEXT FILE
            success_log.write("\r\n position :" + str(position) + "\r\n" + str(k))
            success_log = open("success_log.txt", "a+")


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
    # ChaosDungeon().start_combat()
    # waiting_for_loading_screen()
    # accepting_quest(name="ALL", target="guild_request")
    # accepting_quest(name="ALL", target="weekly")

    # METHODS.list_of_workers = ["Sheeeshaa", "Ggwarlord", "Ggsorc"]
    # finished_char = []
    # switching_char(finished_char)

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
