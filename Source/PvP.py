import multiprocessing
import keyboard
from threading import Thread
from METHODS import im_search_until_found
from METHODS import search_click_image

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

    def cleaning_inventory(self):
        123

    def dimensional_cube(self, search, process_search_inc):
        123
        #BIFROST TO the boss rush/cube spot?
        # ACcepting quests?
        # press G
        # matchmaking or enter?
        # WAIT FOR THE QUE !CAN TAKE LOONG TIME!
        # Press ok Button
        # Loading screen
        # Walking upstairs to the light!
        # Casting skills while positioning to the middle!

    def boss_rush(self, search, process_search_inc):
        123
        #BIFROST TO the boss rush/cube spot?
        # Accepting quests?
        # press G
        # matchmaking or enter?
        # WAIT FOR THE QUE !CAN TAKE LOONG TIME!
        # Press ok Button
        # Loading screen
        # Walking upstairs to the light!
        # Casting skills while positioning to the middle!

    def do_pvp(self):
        order = "3rd"
        PVP_type = 3
        # Enter PVP\
        image = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\Daily Quest\\Misc\\PVP_icon.png"
        search_click_image(image, "left")
        # Type of match
        if PVP_type == 3:
            type_match = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\Daily Quest\\Misc\\Team_elimination.png"
        if PVP_type == 2:
            type_match = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\Daily Quest\\Misc\\PVP_deathmatch.png"
        if PVP_type == 1:
            type_match = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\Daily Quest\\Misc\\PVP_TEAM_deathmatch.png"
        im_search_until_found(type_match, click="left", precision=0.6)
        # Que for match
        que_for_match = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\Daily Quest\\Misc\\Queue_for_Match.png"
        search_click_image(que_for_match, "left")
        # WAIT FOR THE QUE !CAN TAKE LOONG TIME!
        ok_button = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\Daily Quest\\Misc\\Accept_PVP_match.png"
        im_search_until_found(ok_button, click="left")
        # Pick order?
        if PVP_type == 3:
            if order == "3rd":
                pick_order = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\Daily Quest\\Misc\\PVP_3rd.png"
            im_search_until_found(pick_order, click="left")
        # # Detect HP bar from PVP Use skills
        # char_name, my_class, work = "something", "Paladin", "123"
        # self.start(char_name, my_class, work)

        leave_button = "C:\\Users\\Ggjustice\\Pictures\\Buttons\\Daily Quest\\Misc\\Pvp_leave.png"
        im_search_until_found(leave_button, click="left")
        # loading screen
        # Re enter PVP

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
                else:
                    print("Found HPbar ", split_string)
                    x1 = round(search[0])
                    y1 = round(search[1])
                    y1 = y1 + 50  # distance under red HP bar
                    x1, y1 = self.stay_within(x1,y1)
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
                                port_pos = im_search_until_found(p, max_samples=1, time_sample=0.1, precision=0.7)
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

                        sim_x1 = abs(x1 - last_cords[0])
                        sim_y1 = abs(y1 - last_cords[1])
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


if __name__ == '__main__':
    ChaosDungeon().do_pvp()
