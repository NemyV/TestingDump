import multiprocessing
from threading import Thread
import keyboard
import pydirectinput
import pyautogui
import METHODS
from multiprocessing import Manager, Process, Pool
from multiprocessing.managers import NamespaceProxy, BaseManager
import inspect  # part of multiprocessing stuff
import random
import time
import glob
from DailyQuests import daily_state_check

# class ObjProxy(NamespaceProxy):
#     """Returns a proxy instance for any user defined data-type. The proxy instance will have the namespace and
#     functions of the data-type (except private/protected callables/attributes). Furthermore, the proxy will be
#     pickable and can its state can be shared among different processes. """
#
#     @classmethod
#     def populate_obj_attributes(cls, real_cls):
#         DISALLOWED = set(dir(cls))
#         ALLOWED = ['__sizeof__', '__eq__', '__ne__', '__le__', '__repr__', '__dict__', '__lt__',
#                    '__gt__']
#         DISALLOWED.add('__class__')
#         new_dict = {}
#         for (attr, value) in inspect.getmembers(real_cls, callable):
#             if attr not in DISALLOWED or attr in ALLOWED:
#                 new_dict[attr] = cls._proxy_wrap(attr)
#         return new_dict
#
#     @staticmethod
#     def _proxy_wrap(attr):
#         """ This method creates function that calls the proxified object's method."""
#
#         def f(self, *args, **kwargs):
#             return self._callmethod(attr, args, kwargs)
#
#         return f
#
#
# attributes = ObjProxy.populate_obj_attributes(Process)
# ProcessProxy = type("ProcessProxy", (ObjProxy,), attributes)


class ChaosDungeon:

    def __init__(self):
        self.skills_dict = []
        self.all_event = multiprocessing.Event()
        self.two_chaos = multiprocessing.Event()
        self.combat_event = multiprocessing.Event()
        self.normal_event = multiprocessing.Event()
        self.current_class = ""
        self.current_work = ""
        self.process_search_inc = 2
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
        # found_at = [(METHODS.MiniMCOORD[0] + search[0]),
        #             (METHODS.MiniMCOORD[1] + search[1])]

        found_at = search
        distance = [found_at[0] - METHODS.playerMinimap[0],
                    found_at[1] - METHODS.playerMinimap[1]]
        # distance = [round(distance[0]) * self.process_search_inc,
        #             round(distance[1]) * self.process_search_inc]
        # # distance[1] = round(distance[1]) * self.process_search_inc
        # print(METHODS.player_anchor,distance)
        # result = numpy.array(METHODS.player_anchor) - numpy.array(distance)
        # print(result)
        ps_x1 = round(METHODS.player_anchor[0] + round(distance[0]) * process_search_inc)
        ps_y1 = round(METHODS.player_anchor[1] + round(distance[1]) * process_search_inc)

        ps_x1, ps_y1 = self.stay_within(ps_x1, ps_y1)
        # print("Distance is :", distance)
        # print(ps_x1, ps_y1)
        return ps_x1, ps_y1

    def stay_within(self, x_cord, y_cord):
        if x_cord > round(METHODS.Resolution[0] / 100 * 87):
            x_cord = round(METHODS.Resolution[0] / 100 * 87)
        if x_cord < round(METHODS.Resolution[0] / 100 * 15):
            x_cord = round(METHODS.Resolution[0] / 100 * 15)

        if y_cord > round(METHODS.Resolution[1] / 100 * 72):
            y_cord = round(METHODS.Resolution[1] / 100 * 72)
        if y_cord < round(METHODS.Resolution[1] / 100 * 10):
            y_cord = round(METHODS.Resolution[1] / 100 * 10)
        return x_cord, y_cord

    def drinking_potions(self):
        search = METHODS.image2text(x1=947, y1=954, x2=225, y2=20,
                                    method='--psm 7 --oem 3 -c tessedit_char_whitelist=/0123456789')
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
                # print(round(result, 2))
            except:
                123
                # print("Error with HP potion number")
            if 0.70 >= result > 0:
                METHODS.potions_used += 1
                pydirectinput.press('F1')
                print("USING HP POTION", METHODS.potions_used)
            else:
                123

    def centeral_detection(self):
        print("Central / HPbars")
        while not self.combat_event.is_set():
            count_occurrance = 0
            movementdelay = 0.4
            self.drinking_potions()
            for g in METHODS.ChaosDung:
                # Get last 10 character
                # last_chars = g[-20:]
                split_string = g.rsplit('\\')[2]
                # print(split_string)
                startx = round(METHODS.Resolution[0] / 100 * 16)
                starty = round(METHODS.Resolution[1] / 100 * 1)
                count_occurrance = count_occurrance + 1
                occurances = str(count_occurrance) + str(split_string)
                # print(g)
                # METHODS.Resolution Searching
                search = METHODS.im_processing(g, count=occurances, look_for="HPbar", precision=0.86,
                                       x1=startx, y1=starty, y2=round(METHODS.Resolution[1] / 100 * 83))  # - 180)
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
            movementdelay = 0.4
            countingportattempt = 0
            for g in METHODS.minimap_dir:
                if "Boss" in g:
                    looking_for = "Boss"
                elif "Portal" in g:
                    looking_for = "Portal"
                elif "Elite" in g:
                    looking_for = "Elite"
                elif "Tower" in g:
                    looking_for = "Tower"
                # Get last 10 character
                split_string = g.rsplit('\\')[2]
                # print(split_string)
                # print(g)
                count_occurrance = count_occurrance + 1
                occurances = str(count_occurrance) + str(split_string)
                # MINIMAP Searching
                search = METHODS.im_processing(g, count=occurances, look_for=looking_for,
                                       x1=METHODS.MiniMCOORD[0], y1=METHODS.MiniMCOORD[1],
                                       x2=METHODS.MiniMCOORD[2], y2=METHODS.MiniMCOORD[3], precision=0.65)
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
                    x1, y1 = self.process_search(search, self.process_search_inc)
                    pydirectinput.moveTo(x1, y1)

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
                            self.process_search_inc = 10
                            Thread(target=self.stop_combat).start()
                            Thread(target=self.waiting_for_black).start()
                            for p in METHODS.passingthrough:
                                # pydirectinput.press('-')  # stopping combat
                                # print("PRINTING THIS SHIT ", METHODS.misc_dictionary["loading"])
                                if METHODS.misc_dictionary["loading"] == "yes":
                                    end_time = time.time()
                                    result_time = end_time - start_time
                                    print("FOUND LOADING FROM PORTAL")
                                    success_log = open("Chaos_logs.txt", "a+")
                                    success_log.write("\r\n Time to enter PORTAL in seconds:" + str(result_time))
                                    success_log = open("Chaos_logs.txt", "a+")
                                    METHODS.misc_dictionary["loading"] = "no"
                                    # Thread(target=self.start_combat).start()
                                    self.restating_stopped(countingportattempt)
                                    break_switch = 1
                                    break
                                port_pos = METHODS.im_search_until_found(p, time_sample=0.1, max_samples=2, precision=0.7)
                                print("PORTAL POSITION", port_pos)
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
                                    search = METHODS.im_processing(g, count=countingportattempt, look_for=looking_for,
                                                                   x1=METHODS.MiniMCOORD[0], y1=METHODS.MiniMCOORD[1],
                                                                   x2=METHODS.MiniMCOORD[2], y2=METHODS.MiniMCOORD[3], precision=0.7)
                                    print("Searching for portal", search)
                                    # print(METHODS.MiniMCOORD[0], METHODS.MiniMCOORD[1])
                                    if search != [-1, -1]:
                                        x1, y1 = self.process_search(search, self.process_search_inc)
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
                                        self.process_search_inc = 2
                                        break_switch = 1
                                        break
                        self.process_search_inc = 2
                    if "Tower" in g:
                        # MAYBE COMEPLETE NEW APROACH TO FINDING TOWER
                        print("found Tower ", search)
                        print("last_cords ", METHODS.last_cords)
                        self.process_search_inc = 20
                        x1_tower, y1_tower = self.process_search(search, self.process_search_inc)

                        sim_x1 = abs(x1_tower - METHODS.last_cords[0])
                        sim_y1 = abs(y1_tower - METHODS.last_cords[1])
                        print("SIMILARITIES", sim_y1, sim_y1)
                        if sim_x1 < 25 and sim_y1 < 25:
                            # if [x1, y1] == METHODS.last_cords:
                            print("LAST CORD IS SIMILAR. Similarities : ", sim_x1, sim_y1)
                            x1_tower = random.randint(700, 2000)
                            y1_tower = random.randint(300, 700)
                            pydirectinput.moveTo(x1_tower, y1_tower)
                            # pydirectinput.mouseDown(x1, y1, button="right")
                            time.sleep(movementdelay)
                            self.process_search_inc = 2
                        else:
                            print("Current last_cords ", METHODS.last_cords)
                            # THERE WAS AN ERROR WHERE y1 here was larger than 90% of screen should be impossible
                            METHODS.last_cords = [x1_tower, y1_tower]
                            if x1_tower < 380:
                                print("ERROR WITH COORDINATES X")
                                exit()
                            if y1_tower > 800:
                                print("ERROR WITH COORDINATES Y")
                                exit()
                            print("MOVING TO", x1_tower, y1_tower)
                            pydirectinput.moveTo(x1_tower, y1_tower)
                            # pydirectinput.mouseDown(x1, y1, button="right")
                            time.sleep(movementdelay)
                            self.process_search_inc = 2
                            break

            count_occurrance = 0
            for f in METHODS.minimap_red:
                # print("Doing reds ", f)
                split_string = f.rsplit('\\')[2]
                count_occurrance = count_occurrance + 1
                occurances = str(count_occurrance) + str(split_string)

                search = METHODS.im_processing(f, count=occurances, look_for="Red",
                                               x1=METHODS.MiniMCOORD[0], y1=METHODS.MiniMCOORD[1],
                                               x2=METHODS.MiniMCOORD[2], y2=METHODS.MiniMCOORD[3], precision=0.6)

                if search != [-1, -1]:
                    x1, y1 = self.process_search(search, self.process_search_inc)
                    print("Found red", x1, y1)
                    # x1, y1 = self.stay_within(x1,y1)
                    pydirectinput.moveTo(x1, y1)
                    # pydirectinput.mouseDown(x1, y1, button="right")
                    time.sleep(movementdelay)
                    # pydirectinput.mouseUp(button="right")
                    break

    def repair_and_enter(self, counting):
        repair_gear = METHODS.Buttons + "\\ChaosMisc\\Repair_gear.png"
        leave = METHODS.Buttons + '\\ChaosMisc\\Leave.png'
        ok_button = METHODS.Buttons + '\\ChaosMisc\\ok_button.png'
        repair_all = METHODS.Buttons + '\\ChaosMisc\\Repair all.png'

        position = METHODS.im_search(repair_gear, precision=0.7)
        print("Repairing stuff", position)
        if position != [-1, -1]:
            print("REPAIRING")
            Thread(target=self.stop_normal).start()
            time.sleep(1)
            Thread(target=self.stop_combat).start()
            time.sleep(4)
            METHODS.search_click_image(leave, "left")
            time.sleep(1)
            METHODS.search_click_image(ok_button, "left")
            time.sleep(40)  # loading screen
            pydirectinput.press('g')
            time.sleep(2)
            METHODS.search_click_image(repair_all, "left")
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
        # METHODS.pet_status = "no"
        repair_all = METHODS.Buttons + '\\ChaosMisc\\Repair all.png'
        repair_icon = METHODS.Buttons + "\\Daily Quest\\Misc\\Pet_repairing.png"
        if METHODS.pet_status == "yes":
            pydirectinput.keyDown('alt')
            time.sleep(0.3)
            pydirectinput.press('p')
            time.sleep(0.2)
            pydirectinput.keyUp('alt')
            METHODS.search_click_image(repair_icon, "left")
            time.sleep(0.5)
            METHODS.search_click_image(repair_all, "left")
            time.sleep(1)
            pydirectinput.press('ESC')
            time.sleep(1)
            pydirectinput.press('ESC')
        else:
            123

    def state_check(self, current_worker, *args):
        print(*args)
        print("i was here", current_worker)
        # Misc
        counting_state = 0
        count_death = 0
        count_stage_clear = 0
        count_stage_fail = 0
        success_log = open("success_log.txt", "a+")
        METHODS.focus_window('LOST ARK')
        # Begining on the program REPAIRING
        self.repairing()
        time.sleep(0.3)
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
            for y in METHODS.check_if_clear:
                counting_state += 1
                position = METHODS.im_search(y, precision=0.7)
                if position != [-1, -1]:
                    try:
                        self.stop_combat()
                        self.stop_normal()
                    except:
                        print("Error stopping combat in state_check chaos dungeon")
                    # checking for % in top left corner
                    stage_percent = METHODS.image2text(x1=107, y1=186, x2=55, y2=19,
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
                    print("CURRENT TOTAL POTS USED ", METHODS.potions_used)
                    success_log.write("\r\n Potions :" + str(METHODS.potions_used))
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
                            METHODS.configparser.set("Finished_Characters", current_worker, "yes")
                            METHODS.configparser.write()
                            daily_state_check()
                            self.stop_all()
                            # os._exit(1)
                    else:
                        print("INFINITE CHAOS CONTINUES")
                    for u in METHODS.restart_chaos:
                        print("RESTARTING CHAOS")
                        time.sleep(0.7)
                        METHODS.search_click_image(u, "left")
                    # print("APPENDED switch to ", switch)
                    # add loading screen function
                    time.sleep(5)
                    self.restating_stopped(counting_state)
            # turn on for INFINITE chaos
            # self.repair_and_enter(counting_state)
            for x in METHODS.checkIFDEAD:
                position = METHODS.search_click_image(x, "left")
                time.sleep(2)
                if position == [-1, -1]:
                    time.sleep(5)
                    # print("still alive and switch is", switch)
                else:
                    count_death += 1
                    print("DEATH COUNTER:", count_death)
                    pydirectinput.press('-')
                    time.sleep(2)
                    METHODS.search_click_image(x, "left")
                    # switch.append("On")
                    self.restating_stopped(counting_state)
                    # print("APPENDED switch to ", switch)
                    time.sleep(1)
                for y in METHODS.ReENTERing:
                    position = METHODS.search_click_image(y, "left")
                # check if timer is 0 then enter chaos
                # CHeck if need to repair

    def restating_stopped(self, count):
        restarting_dict = {"name": "thread"}
        self.combat_event.set()
        if self.combat_event.is_set():
            print("RESTARTING COMBAT and HPbars ", count)
            self.stop_combat()
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
            self.stop_normal()
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
                METHODS.misc_dictionary["loading"] = 'yes'
                time.sleep(0.1)
                break

    def start(self, char_name, my_class, work):
        # DISMANTLE GEAR level 4 = Legendary equipment
        self.dismantle(4)
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
                                'a': "normal", 's': "normal", 'd': "normal", 'f': "holding"}
        if self.current_class == "Gunlancer":
            self.skills_dict = {'q': "normal", 'w': "combo", 'e': "normal", 'r': "normal",  # Gunlancer image casting
                                'a': "combo", 's': "holding", 'd': "combo", 'f': "holding"}
        if self.current_class == "Lance master":
            self.skills_dict = {'q': "normal", 'w': "combo", 'e': "normal", 'r': "combo",  # Lance master image casting
                                'a': "normal", 's': "normal", 'd': "normal", 'f': "normal"}
        if self.current_class == "Gunslinger":
            self.skills_dict = {'q': "normal", 'w': "none", 'e': "none", 'r': "none",  # Gunslinger image casting
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
            METHODS.casting_skills(self.skills_dict, self.current_class)

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

    def dismantle(self, dismantle_level):
        pydirectinput.press("i")
        dismantle_icon = METHODS.Buttons + "\\Daily Quest\\Misc\\Dismantle_icon.png"
        METHODS.search_click_image(dismantle_icon, action="left")
        dismantle_dir = METHODS.Buttons + "Daily Quest\\Misc\\Dismantling"
        dismantle_this = [m for m in glob.glob(dismantle_dir + "**/*.png")]
        count = 0
        for x in dismantle_this:
            if count == dismantle_level:
                break
            else:
                METHODS.search_click_image(x, action="left")
            count += 1
        # for x in range(0, dismantle_level, 1):
        #     pydirectinput.leftClick(basex, basey)
        #     basex += 107
        #     print(basex)
        dismantle_button = METHODS.Buttons + "\\Daily Quest\\Misc\\Dismantle_button.png"
        METHODS.im_search_until_found(dismantle_button, max_samples=5, precision=0.75)
        # ok = METHODS.Buttons + "\\Daily Quest\\Misc\\First_loging_guild.png"
        # METHODS.search_click_image(ok, action="left", precision=0.7)
        time.sleep(0.2)
        dismantle_button = METHODS.Buttons + "\\Daily Quest\\Misc\\OK_button.png"
        METHODS.im_search_until_found(dismantle_button, max_samples=5, precision=0.8)
        time.sleep(0.3)
        pydirectinput.press("i")
        print("gear dismantled")

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

    # ChaosDungeon().start("Speedpuncher", "Scrapper", work="2_daily_chaos")
    # stronghold_daily()
    # daily_state_check()
    # METHODS.ChaosDungeon().minimap_detection()
    # METHODS.ChaosDungeon().centeral_detection()
    # ChaosDungeon().start_combat()
    # waiting_for_loading_screen()
    # accepting_quest(name="ALL", target="guild_request")
    # accepting_quest(name="ALL", target="weekly")

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
