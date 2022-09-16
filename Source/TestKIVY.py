import sys

sys.path.insert(0, 'E:\Hello wolrd Python\LOSTARKB')
import threading
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.config import ConfigParser
from KivyOnTop import register_topmost, unregister_topmost
from kivy.clock import Clock, mainthread
from kivy.properties import StringProperty
from kivy.uix.checkbox import CheckBox
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from pynput.keyboard import Key, Listener
import numpy as np
import keyboard
import os
from kivy.base import runTouchApp
import psutil
import time
from kivy.uix.dropdown import DropDown
from threading import Thread
from multiprocessing import Process

# IMPORTS FROM LOOKFOR
from LostARKFOCUS import GlobalLabel
from STARTlookfor import startlookfor
from Lifeskills import fishing
from STATEcheck import debugging
from METHODS import focus_window
from DailyQuests import daily_state_check

# Imports from DailyQuests
from DailyQuests import lopang_daily
from DailyQuests import nameless_daily
from DailyQuests import swamp_daily

# CHARACTER SLECTION
global selected_character
selected_character = ""
global roster_list
roster_list = []
global worker_list
worker_list = []
global roster_array
roster_array = np.array(roster_list)

# Overwatch
global Enemies
Enemies = 'enemies imported'
GlobalLabel = '123'
GlobalLabel2 = 'GlobalLabel2'

global start_time
start_time = 0


PirateCoins = 20200
CoinOfCourage = 42760
Bloodstones = 11000
CurrentCoins = 0
NumberofChar = 0
PirateGold = 0
sm = ScreenManager()
LoAImages = 'Buttons\\'
Source = 'D:\\BLostArk\\LOSTARKB\\Source\\'

# These changes need to be present !!!!BEFORE you import Window!!!!

configparser = ConfigParser()
configparser.read("myapp.ini")
string = configparser.get("Settings", "resolution")

Resolution = [int(string.split("x")[0]),
              int(string.split("x")[1])]

# if Config.getint('graphics', 'borderless') == 0:
#     Config.write()

from kivy.core.window import Window

energy = 100
hours = 4

core_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
core_num = 8

battery_state = "Charging"
battery_capacity = "100"

stop_threads = False
# Resolution = [2560, 1080]


def callbackTo2(instance):
    Window.size = (Resolution[0], Resolution[1]/7)
    Window.top = Resolution[1]/7*6.1  # 930
    Window.left = 0
    sm.current = "MainMenu"


def callbackTo1(instance):
    Window.size = (Resolution[0]*8/10, Resolution[1]*2/4)
    Window.top = Resolution[1]*2/10
    Window.left = Resolution[0]/10
    sm.current = "Settings"


def callbackTo3(instance):
    Window.size = (760, 250 * 1 / 2)
    Window.top = 955
    Window.left = 1800
    sm.current = "Debugging"


def callbackTo4(instance):
    Window.size = (Resolution[0] / 1.2, Resolution[1] / 1.2)
    Window.left = Resolution[0] / 10.5
    Window.top = Resolution[1] / 9
    sm.current = "Skills"
    123


def callbackTo5(instance):
    Window.size = (Resolution[0] / 4, Resolution[1] / 10)
    Window.left = 0
    Window.top = 930
    sm.current = "Lifeskills"


def callbackTo6(instance):
    Window.size = (Resolution[0] / 1.2, Resolution[1] / 1.2)
    Window.left = Resolution[0] / 10.5
    Window.top = Resolution[1] / 9
    sm.current = "DailyQuests"


def callbackTo7(*args):
    Window.size = (Resolution[0]/8, Resolution[1] / 10)
    Window.left = Resolution[0]/9*4.8
    Window.top = Resolution[1] / 10*9
    sm.current = "Minimalistic"
    # reading config file and what has be done this week or something like that
    # reading stats from screen like buffs on character?


def startfishing(instance):
    focus_window('LOST ARK')
    startla = Thread(target=fishing)
    startla.daemon = True
    startla.start()


def start_work(instance):
    callbackTo7()
    focus_window('LOST ARK')
    global start_time
    start_time = time.time()
    startla = Thread(target=daily_state_check)
    startla.daemon = True
    startla.start()


def startxxx(instance):
    startla = Thread(target=startlookfor)
    startla.daemon = True
    startla.start()


def startTracking(instance):
    startdebug = Thread(target=debugging)
    startdebug.daemon = True
    startdebug.start()


class SubGrids(GridLayout):
    def __init__(self):
        GridLayout.__init__(self, cols=3, rows=3);
        self.add_widget(Label(text='1st'));
        self.add_widget(Label(text='123'));
        self.add_widget(Label(text='2nd'));
        self.add_widget(Label(text='456'));
        self.add_widget(Label(text='3rd'));
        self.add_widget(Label(text='3232'));
        self.add_widget(Label(text='4th'));
        self.add_widget(Label(text='3232'));
        self.add_widget(Label(text='5th'));


class MainMenu(Screen):
    # @mainthread
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        super(MainMenu, self).__init__(name='MainMenu')
        Window.bind(on_keyboard=self.on_keyboard)  # bind our handler
        Window.size = (Resolution[0], Resolution[1] / 7)
        Window.top = Resolution[1] / 7 * 6.1  # 930
        Window.left = 0

        # Main Buttons
        ButtonY = 0.5
        SizeH = 0.5
        SizeW = 0.33
        PosX = .65

        self.lbl_stat = Label(text=GlobalLabel2, pos_hint={'x': -.45, 'y': -0.45})

        self.add_widget(self.lbl_stat)

        # t1= threading.Thread(target=startlookfor).start()

        self.inventory_button = Button(background_normal=LoAImages + 'Blue.jpg',
                                       border=(0, 0, 0, 0),
                                       text="Exit Prog",
                                       size_hint=(SizeW, SizeH),
                                       pos_hint={'x': .67, 'y': ButtonY},
                                       on_press=lambda b: app.stop())
        self.add_widget(self.inventory_button)

        self.food_button = Button(background_normal=LoAImages + 'Blue.jpg',
                                  border=(0, 0, 0, 0),
                                  text="Settings", size_hint=(SizeW, SizeH), pos_hint={'x': .335, 'y': ButtonY}
                                  , on_press=callbackTo1)
        self.add_widget(self.food_button)

        self.walk_button = Button(background_normal=LoAImages + 'Blue.jpg',
                                  border=(0, 0, 0, 0),
                                  text="Debugging", size_hint=(SizeW, SizeH), pos_hint={'x': .0, 'y': ButtonY}
                                  , on_press=callbackTo3)
        self.add_widget(self.walk_button)
        self.help_button = Button(background_normal=LoAImages + 'Blue.jpg',
                                  border=(0, 0, 0, 0),
                                  text="Life_skills", size_hint=(SizeW, SizeH), pos_hint={'x': .67, 'y': 0}
                                  , on_press=callbackTo5)
        self.add_widget(self.help_button)
        self.go_button = Button(background_normal=LoAImages + 'Blue.jpg',
                                border=(0, 0, 0, 0), text="Minimalistic",
                                size_hint=(SizeW, SizeH), pos_hint={'x': .335, 'y': 0},
                                on_press=callbackTo7)
        self.add_widget(self.go_button)

        self.craft_button = Label(text=GlobalLabel, size_hint=(SizeW, SizeH), pos_hint={'x': -.45, 'y': -0.45})
        Clock.schedule_interval(self.update, 0.3)
        # Canvas
        # with self.canvas:
        #    Rectangle(source=LoAImages+'Lostark Wallpaper.png', pos=self.pos, size=(555,820))

        self.add_widget(self.craft_button)
        # self.add_widget(self.name_label)
        self.current_text = "Default"
        # Background
        # self.add_widget(self.background)

    def on_keyboard(self, window, key, scancode, codepoint, modifier, *args):
        global GlobalLabel2
        GlobalLabel2 = modifier, codepoint
        # print(' - modifiers are %r', modifier)
        # print('The key', codepoint, 'have been pressed')
        if modifier == ['ctrl', 'numlock'] and codepoint == 'q':
            global stop_threads
            stop_threads = True
            self.stop()
            print("pressed CTRL + Q")

    def update(self, *args):
        from LostARKFOCUS import GlobalLabel
        self.craft_button.text = str(GlobalLabel)
        self.lbl_stat.text = str(GlobalLabel2)
        # print("this is global labe", GlobalLabel, "test")


class Lifeskills(Screen):
    # @mainthread
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        super(Lifeskills, self).__init__(name='Lifeskills')

        # Main Buttons
        ButtonY = 0.5
        SizeH = 0.5
        SizeW = 0.33
        PosX = -0.04

        ##GRID LAYOUT
        self.layoutImage = GridLayout(pos_hint={'x': PosX, 'y': .0}, cols=5, size_hint=(1, 1),
                                      row_force_default=True, row_default_height=120, col_default_width=120)
        self.add_widget(self.layoutImage)
        self.layoutCheckbox = GridLayout(pos_hint={'x': PosX, 'y': 0.45}, cols=5, size_hint=(0.01, 0.01),
                                         row_force_default=True, row_default_height=77, col_default_width=150)
        self.add_widget(self.layoutCheckbox)

        # Adding Labels
        self.layoutCheckbox.lbl_statEnemy = Label()
        self.layoutCheckbox.add_widget(self.layoutCheckbox.lbl_statEnemy)

        # Adding IMAGES
        self.layoutImage.Enemy = Image(source=Source + '1 Enemy count.png')
        self.layoutImage.add_widget(self.layoutImage.Enemy)

        # Buttons
        self.Return = Button(background_normal=LoAImages + 'Yellow.jpg', border=(0, 0, 0, 0),
                             text="Return",
                             size_hint=(SizeW, SizeH / 3), pos_hint={'x': .55, 'y': 0.50},
                             on_press=callbackTo2)
        self.add_widget(self.Return)

        self.Return = Button(background_normal=LoAImages + 'Yellow.jpg', border=(0, 0, 0, 0),
                             text="Fishing",
                             size_hint=(SizeW, SizeH / 5), pos_hint={'x': .75, 'y': 0.45},
                             on_press=startfishing)
        self.add_widget(self.Return)
        # Misc
        Clock.schedule_interval(self.update, 2)
        self.on_start()

    def on_start(self, *args):
        # ALWAYS ON TOP DEF
        TITLE = 'ScreenPlay'  # name of the window
        Window.set_title(TITLE)

        # Register top-most
        register_topmost(Window, TITLE)
        # Unregister top-most (not necessary, only an example)
        self.bind(on_stop=lambda *args, w=Window, t=TITLE: unregister_topmost(w, t))

    def on_keyboard(self, window, key, scancode, codepoint, modifier, *args):
        global Enemies
        Enemies = modifier, codepoint
        # print(' - modifiers are %r', modifier)
        # print('The key', codepoint, 'have been pressed')
        if modifier == ['ctrl', 'numlock'] and codepoint == 'q':
            global stop_threads
            stop_threads = True
            self.stop()
            print("pressed CTRL + Q")

    def update(self, *args):
        123

        # self.lbl_stat.text = str(GlobalLabel2)
        # print("this is global labe", GlobalLabel, "test")


class Minimalistic(Screen):
    # @mainthread
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        super(Minimalistic, self).__init__(name='Minimalistic')

        # Main Buttons
        ButtonY = 0.5
        SizeH = 0.5
        SizeW = 0.33
        PosX = -0.04

        # INFO GRID
        self.info_grid = GridLayout(pos_hint={'x': 0, 'y': 0}, rows=4, cols=2,
                                    # size_hint=(0.01, 0.01),
                                    row_force_default=True, row_default_height=30, col_default_width=60)
        self.add_widget(self.info_grid)

        self.run_time = Label(text='Work time will be displayed here')
        self.info_grid.add_widget(self.run_time)
        self.Return = Button(background_normal=LoAImages + 'Pink.png', border=(0, 0, 0, 0),
                             background_down=LoAImages + 'Pressed_Button.png',
                             text="Return",
                             on_press=callbackTo2)
        self.info_grid.add_widget(self.Return)
        self.current_working = Label(text='Work work...')
        self.info_grid.add_widget(self.current_working)
        self.start_work = Button(background_normal=LoAImages + 'Pink.png', border=(0, 0, 0, 0),
                                 background_down=LoAImages + 'Pressed_Button.png',
                                 text="start_work", on_press=start_work)
        self.info_grid.add_widget(self.start_work)

        # self.Return = Button(background_normal=LoAImages + 'Yellow.jpg', border=(0, 0, 0, 0),
        #                      text="Return",
        #                      size_hint=(SizeW, SizeH / 3), pos_hint={'x': .75, 'y': 0.7},
        #                      on_press=callbackTo2)
        # self.add_widget(self.Return)
        #
        # self.start_work = Button(background_normal=LoAImages + 'Yellow.jpg', border=(0, 0, 0, 0),
        #                          text="start_work",
        #                          size_hint=(SizeW, SizeH / 2), pos_hint={'x': .45, 'y': 0.60},
        #                          on_press=start_work)
        # self.add_widget(self.start_work)
        # self.chaos_image = Image(source=LoAImages + 'Chaos_dungeon.png', size_hint=(0.5, 0.5),
        #                          pos_hint={'x': 0, 'y': +0.70})
        # self.info_grid.add_widget(self.chaos_image)

        # Checkbox
        # self.info_grid.Infinite_Chaos = Label(text='Infinite Chaos')
        # self.info_grid.add_widget(self.info_grid.Infinite_Chaos)

        # Adding IMAGES
        # self.layoutImage.Enemy = Image(source=Source + '1 Enemy count.png')
        # self.layoutImage.add_widget(self.layoutImage.Enemy)

        # Misc/AUTOMATED THINGS TO START
        Clock.schedule_interval(self.update, 0.1)
        self.on_start()

    def on_start(self, *args):
        # ALWAYS ON TOP DEF
        TITLE = 'ScreenPlay'  # name of the window
        Window.set_title(TITLE)

        # Register top-most
        register_topmost(Window, TITLE)
        # Unregister top-most (not necessary, only an example)
        self.bind(on_stop=lambda *args, w=Window, t=TITLE: unregister_topmost(w, t))

    def on_keyboard(self, window, key, scancode, codepoint, modifier, *args):
        global Enemies
        Enemies = modifier, codepoint
        # print(' - modifiers are %r', modifier)
        # print('The key', codepoint, 'have been pressed')
        if modifier == ['ctrl', 'numlock'] and codepoint == 'q':
            global stop_threads
            stop_threads = True
            self.stop()
            print("pressed CTRL + Q")

    def update(self, *args):
        global Enemies
        global Portals
        global Elites
        global Bosses
        global Towers
        global execution_time
        global current_work
        # TURN DEBUGING ON IF YOU WANT TO CHECK STUFF ON SCREEN
        # debugging()
        # self.layoutImage.Enemy.reload()
        # self.layoutCheckbox.lbl_statBoss.text = "Bosses :" + str(Bosses)
        # self.layoutCheckbox.lbl_statEnemy.text = "Enemies :" + str(Enemies)
        # self.layoutCheckbox.lbl_statPort.text = "Portals :" + str(Portals)
        # self.layoutCheckbox.lbl_statElite.text = "Elites :" + str(Elites)
        # self.lbl_stat.text = str(GlobalLabel2)
        # print("this is global labe", GlobalLabel, "test")

        global start_time
        from DailyQuests import current_work
        from DailyQuests import stop_count
        if stop_count != "yes":
            end_time = time.time()
            time_lapsed = end_time - start_time
            self.run_time.text = str(self.time_convert(time_lapsed))

        self.current_working.text = str(current_work)

    def time_convert(self, sec):
        mins = sec // 60
        sec = sec % 60
        hours = mins // 60
        mins = mins % 60
        # print("Time Lapsed = {0}:{1}:{2}".format(int(hours), int(mins), sec))
        return_value = "Time Lapsed = {0}:{1}:{2}".format(int(hours), int(mins), round(sec, 1))
        return return_value

class Debugging(Screen):
    # @mainthread
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        super(Debugging, self).__init__(name='Debugging')

        # Main Buttons
        ButtonY = 0.5
        SizeH = 0.5
        SizeW = 0.33
        PosX = -0.04

        ##GRID LAYOUT
        self.layoutImage = GridLayout(pos_hint={'x': PosX, 'y': .0}, cols=5, size_hint=(1, 1),
                                      row_force_default=True, row_default_height=120, col_default_width=120)
        self.add_widget(self.layoutImage)
        self.layoutCheckbox = GridLayout(pos_hint={'x': PosX, 'y': 0.45}, cols=5, size_hint=(0.01, 0.01),
                                         row_force_default=True, row_default_height=77, col_default_width=150)
        self.add_widget(self.layoutCheckbox)

        # Adding Labels
        self.layoutCheckbox.lbl_statEnemy = Label()
        self.layoutCheckbox.add_widget(self.layoutCheckbox.lbl_statEnemy)
        self.layoutCheckbox.lbl_statElite = Label()
        self.layoutCheckbox.add_widget(self.layoutCheckbox.lbl_statElite)
        self.layoutCheckbox.lbl_statPort = Label()
        self.layoutCheckbox.add_widget(self.layoutCheckbox.lbl_statPort)
        self.layoutCheckbox.lbl_statTower = Label()
        self.layoutCheckbox.add_widget(self.layoutCheckbox.lbl_statTower)
        self.layoutCheckbox.lbl_statBoss = Label()
        self.layoutCheckbox.add_widget(self.layoutCheckbox.lbl_statBoss)

        # Adding IMAGES
        self.layoutImage.Enemy = Image(source=Source + '1 Enemy count.png')
        self.layoutImage.add_widget(self.layoutImage.Enemy)
        self.layoutImage.Elite = Image(source=Source + '1 Elite count.png')
        self.layoutImage.add_widget(self.layoutImage.Elite)
        self.layoutImage.Portal = Image(source=Source + '1 Portal count.png')
        self.layoutImage.add_widget(self.layoutImage.Portal)
        self.layoutImage.Tower = Image(source=Source + '1 Portal count.png')
        self.layoutImage.add_widget(self.layoutImage.Tower)
        self.layoutImage.Boss = Image(source=Source + '1 Portal count.png')
        self.layoutImage.add_widget(self.layoutImage.Boss)

        # Buttons
        self.Return = Button(background_normal=LoAImages + 'Yellow.jpg', border=(0, 0, 0, 0),
                             text="Return",
                             size_hint=(SizeW, SizeH / 5), pos_hint={'x': .75, 'y': 0.90},
                             on_press=callbackTo2)
        self.add_widget(self.Return)

        # Misc/AUTOMATED THINGS TO START
        # Clock.schedule_interval(self.update, 2)
        self.on_start()

    def on_start(self, *args):
        # ALWAYS ON TOP DEF
        TITLE = 'ScreenPlay'  # name of the window
        Window.set_title(TITLE)

        # Register top-most
        register_topmost(Window, TITLE)
        # Unregister top-most (not necessary, only an example)
        self.bind(on_stop=lambda *args, w=Window, t=TITLE: unregister_topmost(w, t))

    def on_keyboard(self, window, key, scancode, codepoint, modifier, *args):
        global Enemies
        Enemies = modifier, codepoint
        # print(' - modifiers are %r', modifier)
        # print('The key', codepoint, 'have been pressed')
        if modifier == ['ctrl', 'numlock'] and codepoint == 'q':
            global stop_threads
            stop_threads = True
            self.stop()
            print("pressed CTRL + Q")

    def update(self, *args):
        from METHODS_OLD_BACKUP import Elites
        from METHODS_OLD_BACKUP import Bosses
        from METHODS_OLD_BACKUP import Towers
        from METHODS_OLD_BACKUP import Enemies
        from METHODS_OLD_BACKUP import Portals
        global Enemies
        global Portals
        global Elites
        global Bosses
        global Towers
        # TURN DEBUGING ON IF YOU WANT TO CHECK STUFF ON SCREEN
        # debugging()
        self.layoutImage.Boss.reload()
        self.layoutImage.Tower.reload()
        self.layoutImage.Enemy.reload()
        self.layoutImage.Elite.reload()
        self.layoutImage.Portal.reload()
        self.layoutCheckbox.lbl_statTower.text = "Towers :" + str(Towers)
        self.layoutCheckbox.lbl_statBoss.text = "Bosses :" + str(Bosses)
        self.layoutCheckbox.lbl_statEnemy.text = "Enemies :" + str(Enemies)
        self.layoutCheckbox.lbl_statPort.text = "Portals :" + str(Portals)
        self.layoutCheckbox.lbl_statElite.text = "Elites :" + str(Elites)

        # self.lbl_stat.text = str(GlobalLabel2)
        # print("this is global labe", GlobalLabel, "test")


class Skills(Screen):
    # @mainthread
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        super(Skills, self).__init__(name='Skills')
        # Main Buttons
        ButtonY = 0.5
        SizeH = 0.5
        SizeW = 0.33
        PosX = 0.0

        # GRID LAYOUT
        self.layoutImage = GridLayout(pos_hint={'x': PosX, 'y': .0}, cols=3, size_hint=(1, 1),
                                      row_force_default=True, row_default_height=120, col_default_width=150)
        self.add_widget(self.layoutImage)

        self.layoutSkillInput = GridLayout(pos_hint={'x': PosX, 'y': 0.97}, cols=3, size_hint=(0.01, 0.01),
                                           row_force_default=True, row_default_height=40, col_default_width=165)
        self.add_widget(self.layoutSkillInput)

        # Buttons
        self.Return = Button(background_normal=LoAImages + 'Yellow.jpg', border=(0, 0, 0, 0),
                             text="Return",
                             size_hint=(SizeW, SizeH / 5), pos_hint={'x': .75, 'y': 0.90},
                             on_press=callbackTo2)
        self.add_widget(self.Return)

        # Class as selection from drop down menu

        # Class identity

        # Test inputs
        self.layoutSkillInput.skill1 = TextInput(hint_text="Keybind for Skill 1? Q", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1)
        self.layoutSkillInput.skill1cd = TextInput(hint_text="Cooldown?", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1cd)
        self.layoutSkillInput.skill1prio = TextInput(hint_text="Priority? -1=Dont use", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1prio)

        self.layoutSkillInput.skill1 = TextInput(hint_text="Keybind for Skill 1? Q", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1)
        self.layoutSkillInput.skill1cd = TextInput(hint_text="Cooldown?", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1cd)
        self.layoutSkillInput.skill1prio = TextInput(hint_text="Priority? -1=Dont use", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1prio)

        self.layoutSkillInput.skill1 = TextInput(hint_text="Keybind for Skill 1? Q", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1)
        self.layoutSkillInput.skill1cd = TextInput(hint_text="Cooldown?", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1cd)
        self.layoutSkillInput.skill1prio = TextInput(hint_text="Priority? -1=Dont use", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1prio)

        self.layoutSkillInput.skill1 = TextInput(hint_text="Keybind for Skill 1? Q", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1)
        self.layoutSkillInput.skill1cd = TextInput(hint_text="Cooldown?", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1cd)
        self.layoutSkillInput.skill1prio = TextInput(hint_text="Priority? -1=Dont use", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1prio)

        self.layoutSkillInput.skill1 = TextInput(hint_text="Keybind for Skill 1? Q", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1)
        self.layoutSkillInput.skill1cd = TextInput(hint_text="Cooldown?", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1cd)
        self.layoutSkillInput.skill1prio = TextInput(hint_text="Priority? -1=Dont use", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1prio)

        self.layoutSkillInput.skill1 = TextInput(hint_text="Keybind for Skill 1? Q", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1)
        self.layoutSkillInput.skill1cd = TextInput(hint_text="Cooldown?", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1cd)
        self.layoutSkillInput.skill1prio = TextInput(hint_text="Priority? -1=Dont use", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1prio)

        self.layoutSkillInput.skill1 = TextInput(hint_text="Keybind for Skill 1? Q", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1)
        self.layoutSkillInput.skill1cd = TextInput(hint_text="Cooldown?", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1cd)
        self.layoutSkillInput.skill1prio = TextInput(hint_text="Priority? -1=Dont use", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1prio)

        self.layoutSkillInput.skill1 = TextInput(hint_text="Keybind for Skill 1? Q", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1)
        self.layoutSkillInput.skill1cd = TextInput(hint_text="Cooldown?", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1cd)
        self.layoutSkillInput.skill1prio = TextInput(hint_text="Priority? -1=Dont use", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1prio)

        self.layoutSkillInput.skill1 = TextInput(hint_text="Keybind for ULTIMATE 1? V", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1)
        self.layoutSkillInput.skill1cd = TextInput(hint_text="Cooldown?", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1cd)
        self.layoutSkillInput.skill1prio = TextInput(hint_text="Priority? -1=Dont use", multiline=False, font_size=16)
        self.layoutSkillInput.add_widget(self.layoutSkillInput.skill1prio)

        # Misc
        Clock.schedule_interval(self.update, 2)
        self.on_start()

    def on_start(self, *args):
        # ALWAYS ON TOP DEF
        TITLE = 'ScreenPlay'  # name of the window
        Window.set_title(TITLE)

        # Register top-most
        register_topmost(Window, TITLE)
        # Unregister top-most (not necessary, only an example)
        self.bind(on_stop=lambda *args, w=Window, t=TITLE: unregister_topmost(w, t))

    def on_keyboard(self, window, key, scancode, codepoint, modifier, *args):
        global Enemies
        Enemies = modifier, codepoint
        # print(' - modifiers are %r', modifier)
        # print('The key', codepoint, 'have been pressed')
        if modifier == ['ctrl', 'numlock'] and codepoint == 'q':
            global stop_threads
            stop_threads = True
            self.stop()
            print("pressed CTRL + Q")

    def update(self, *args):
        123
        # self.lbl_stat.text = str(GlobalLabel2)
        # print("this is global labe", GlobalLabel, "test")


class DailyQuests(Screen):
    # @mainthread
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        super(DailyQuests, self).__init__(name='DailyQuests')

        # Main Buttons
        SizeH = 0.5
        SizeW = 0.33
        # Base
        base_label_x = -.44
        base_image_x = -.24
        grid_checkbox_x = 0.07
        grid_label_x = -.46
        # Steps
        grid_step_x = 0.11
        # create a dropdown
        self.dropdown = DropDown()

        # MAIN GRID
        self.MAIN_GRID = GridLayout(pos_hint={'x': 0.01, 'y': 0.97}, cols=10,
                                    size_hint=(0.01, 0.01),
                                    row_force_default=True, row_default_height=60, col_default_width=240)
        self.add_widget(self.MAIN_GRID)

        # Label/Checkbox adding
        # GRID LAYOUT [ LEAPSTONES ]
        self.leapstone_grid = GridLayout(cols=2,
                                         row_force_default=True, row_default_height=60, col_default_width=110)
        self.MAIN_GRID.add_widget(self.leapstone_grid)

        self.leapstone_lbl = Label(text='Leapstone dailies:',
                                   pos_hint={'x': base_label_x, 'y': +0.45})
        self.leapstone_grid.add_widget(self.leapstone_lbl)
        self.leapstone_image = Image(source=LoAImages + 'Greater Honor leapstone.png',
                                     size_hint=(0.5, 0.5), pos_hint={'x': base_image_x, 'y': +0.70})
        self.leapstone_grid.add_widget(self.leapstone_image)

        # Checkbox
        self.leapstone_grid.ALL_lbl = Label(text='Accept ALL favorites')
        self.leapstone_grid.add_widget(self.leapstone_grid.ALL_lbl)
        self.leapstone_grid.ALL_checkbox = CheckBox(ids=({'name': 'all_leapstone'}))
        self.leapstone_grid.add_widget(self.leapstone_grid.ALL_checkbox)

        self.leapstone_grid.Hypno_lbl = Label(text='Hypno')
        self.leapstone_grid.add_widget(self.leapstone_grid.Hypno_lbl)
        self.leapstone_grid.Hypno_checkbox = CheckBox(ids=({'name': 'hypno'}))
        self.leapstone_grid.add_widget(self.leapstone_grid.Hypno_checkbox)

        self.leapstone_grid.Nameless_valley = Label(text='Nameless Valley')
        self.leapstone_grid.add_widget(self.leapstone_grid.Nameless_valley)
        self.leapstone_grid.Nameless_valley = CheckBox(ids=({'name': 'nameless_valley'}))
        self.leapstone_grid.add_widget(self.leapstone_grid.Nameless_valley)

        self.leapstone_grid.Swamp = Label(text='Wailling swamp')
        self.leapstone_grid.add_widget(self.leapstone_grid.Swamp)
        self.leapstone_grid.Swamp = CheckBox(ids=({'name': 'swamp'}))
        self.leapstone_grid.add_widget(self.leapstone_grid.Swamp)
        # BINDING Checkboxes
        self.leapstone_grid.ALL_checkbox.bind(active=self.uncheck_other)

        # # Labels
        # GRID LAYOUT [ SILVER ]
        self.silver_grid = GridLayout(cols=2,
                                      row_force_default=True, row_default_height=60, col_default_width=110)
        self.MAIN_GRID.add_widget(self.silver_grid)  # <<<<<<<<<<<<<<<<<

        self.silver_lbl = Label(text='Silver dailies:',
                                pos_hint={'x': base_label_x + grid_step_x, 'y': +0.45})
        self.silver_grid.add_widget(self.silver_lbl)
        self.silver_image = Image(source=LoAImages + 'Chest T2.png',size_hint=(0.5, 0.5),
                                  pos_hint={'x': base_image_x + grid_step_x, 'y': +0.70})
        self.silver_grid.add_widget(self.silver_image)

        # Checkbox
        self.silver_grid.ALL = Label(text='Accept ALL favorites')
        self.silver_grid.add_widget(self.silver_grid.ALL)
        self.silver_grid.ALL = CheckBox(ids=({'name': 'all_silver'}))
        self.silver_grid.add_widget(self.silver_grid.ALL)

        self.silver_grid.lopang_vern = Label(text='Lopang Vern')
        self.silver_grid.add_widget(self.silver_grid.lopang_vern)
        self.silver_grid.lopang_vern = CheckBox(ids=({'name': 'vern'}))
        self.silver_grid.add_widget(self.silver_grid.lopang_vern)

        self.silver_grid.lopang_arthentine = Label(text='Lopang Arthentine')
        self.silver_grid.add_widget(self.silver_grid.lopang_arthentine)
        self.silver_grid.lopang_arthentine = CheckBox(ids=({'name': 'arthentine'}))
        self.silver_grid.add_widget(self.silver_grid.lopang_arthentine)

        self.silver_grid.lopang_shushire = Label(text='Lopang Shushire')
        self.silver_grid.add_widget(self.silver_grid.lopang_shushire)
        self.silver_grid.lopang_shushire = CheckBox(ids=({'name': 'shushire'}))
        self.silver_grid.add_widget(self.silver_grid.lopang_shushire)

        # BINDING Checkboxes
        self.silver_grid.ALL.bind(active=self.uncheck_other)

        # GRID LAYOUT [ GUILD ATTENDENCE ]
        self.guild_grid = GridLayout(cols=2,
                                     row_force_default=True, row_default_height=60, col_default_width=110)
        self.MAIN_GRID.add_widget(self.guild_grid)

        self.guild_lbl = Label(text='Guild attendence:')
        self.guild_grid.add_widget(self.guild_lbl)
        self.guild_image = Image(source=LoAImages + 'Bloodcrystal.png')
        self.guild_grid.add_widget(self.guild_image)

        # Checkbox
        self.guild_grid.silver = Label(text='Silver')
        self.guild_grid.add_widget(self.guild_grid.silver)
        self.guild_grid.silver = CheckBox(ids=({'name': 'guild_silver'}))
        self.guild_grid.add_widget(self.guild_grid.silver)

        self.guild_grid.gold = Label(text='Gold')
        self.guild_grid.add_widget(self.guild_grid.gold)
        self.guild_grid.gold = CheckBox(ids=({'name': 'guild_gold'}))
        self.guild_grid.add_widget(self.guild_grid.gold)

        self.guild_grid.honor = Label(text='Honor')
        self.guild_grid.add_widget(self.guild_grid.honor)
        self.guild_grid.honor = CheckBox(ids=({'name': 'guild_honor', 'checkbox': 'guild_honor'}))
        self.guild_grid.add_widget(self.guild_grid.honor)

        self.guild_grid.gienah_coins = Label(text='Gienah Coins')
        self.guild_grid.add_widget(self.guild_grid.gienah_coins)
        self.guild_grid.gienah_coins = CheckBox(ids=({'name': 'unknown'}))
        self.guild_grid.add_widget(self.guild_grid.gienah_coins)

        self.guild_grid.boss_rush = Label(text='Boss Rush')
        self.guild_grid.add_widget(self.guild_grid.boss_rush)
        self.guild_grid.boss_rush = CheckBox(ids=({'name': 'unknown'}))
        self.guild_grid.add_widget(self.guild_grid.boss_rush)

        self.guild_grid.cube = Label(text='Cube')
        self.guild_grid.add_widget(self.guild_grid.cube)
        self.guild_grid.cube = CheckBox(ids=({'name': 'unknown'}))
        self.guild_grid.add_widget(self.guild_grid.cube)

        # GRID LAYOUT [ Weekly ]
        self.weekly_grid = GridLayout(cols=2,
                                      row_force_default=True, row_default_height=60, col_default_width=60)
        self.MAIN_GRID.add_widget(self.weekly_grid)  # <<<<<<<<<<<<<<<<<

        self.weekly_lbl = Label(text='Weeklies:',
                                pos_hint={'x': base_label_x + grid_step_x * 3, 'y': +0.45})
        self.weekly_grid.add_widget(self.weekly_lbl)

        self.weekly_image = Image(source=LoAImages + 'Weekly_icon.png', size_hint=(0.5, 0.5),
                                  pos_hint={'x': base_image_x + grid_step_x * 3, 'y': +0.70})
        self.weekly_grid.add_widget(self.weekly_image)
        # Checkbox
        self.weekly_grid.ALL = Label(text='Accept ALL favorites')
        self.weekly_grid.add_widget(self.weekly_grid.ALL)
        self.weekly_grid.ALL = CheckBox(ids=({'name': 'all_weekly'}))
        self.weekly_grid.add_widget(self.weekly_grid.ALL)

        # GRID LAYOUT [ Presets ]
        self.presets_grid = GridLayout(cols=2,
                                       row_force_default=True, row_default_height=60, col_default_width=60)
        self.MAIN_GRID.add_widget(self.presets_grid)  # <<<<<<<<<<<<<<<<<

        self.presets_lbl = Label(text='Choose your preset:',
                                 pos_hint={'x': base_label_x + grid_step_x * 3, 'y': +0.45})
        self.presets_grid.add_widget(self.presets_lbl)

        self.presets_image = Image(source=LoAImages + 'Presets.png', size_hint=(0.5, 0.5),
                                   pos_hint={'x': base_image_x + grid_step_x * 3, 'y': +0.70})
        self.presets_grid.add_widget(self.presets_image)
        # Checkbox
        self.presets_grid.preset_1_lbl = Label(text='Preset 1')
        self.presets_grid.add_widget(self.presets_grid.preset_1_lbl)
        self.presets_grid.preset_1_checkbox = CheckBox(ids=({'name': 'preset_1'}))
        self.presets_grid.add_widget(self.presets_grid.preset_1_checkbox)

        self.presets_grid.preset_2_lbl = Label(text='Preset 2')
        self.presets_grid.add_widget(self.presets_grid.preset_2_lbl)
        self.presets_grid.preset_2_checkbox = CheckBox(ids=({'name': 'preset_2'}))
        self.presets_grid.add_widget(self.presets_grid.preset_2_checkbox)

        self.presets_grid.preset_3_lbl = Label(text='Preset 3')
        self.presets_grid.add_widget(self.presets_grid.preset_3_lbl)
        self.presets_grid.preset_3_checkbox = CheckBox(ids=({'name': 'preset_3'}))
        self.presets_grid.add_widget(self.presets_grid.preset_3_checkbox)

        self.presets_grid.preset_4_lbl = Label(text='Preset 4')
        self.presets_grid.add_widget(self.presets_grid.preset_4_lbl)
        self.presets_grid.preset_4_checkbox = CheckBox(ids=({'name': 'preset_4'}))
        self.presets_grid.add_widget(self.presets_grid.preset_4_checkbox)

        self.presets_grid.preset_5_lbl = Label(text='Preset 5')
        self.presets_grid.add_widget(self.presets_grid.preset_5_lbl)
        self.presets_grid.preset_5_checkbox = CheckBox(ids=({'name': 'preset_5'}))
        self.presets_grid.add_widget(self.presets_grid.preset_5_checkbox)

        # GRID LAYOUT [ Stronghold ]
        self.stronghold_grid = GridLayout(cols=2,
                                          row_force_default=True, row_default_height=60, col_default_width=60)
        self.MAIN_GRID.add_widget(self.stronghold_grid)  # <<<<<<<<<<<<<<<<<

        self.stronghold_lbl = Label(text='STRONGHOLD:',
                                    pos_hint={'x': base_label_x + grid_step_x * 3, 'y': +0.45})
        self.stronghold_grid.add_widget(self.stronghold_lbl)

        self.stronghold_image = Image(source=LoAImages + 'Weekly_icon.png', size_hint=(0.5, 0.5),
                                      pos_hint={'x': base_image_x + grid_step_x * 3, 'y': +0.70})
        self.stronghold_grid.add_widget(self.stronghold_image)
        # Checkbox
        self.stronghold_grid.all_lbl_stronghold = Label(text='Do ALL stronghold')
        self.stronghold_grid.add_widget(self.stronghold_grid.all_lbl_stronghold)
        self.stronghold_grid.all_stronghold = CheckBox(ids=({'name': 'all_stronghold'}))
        self.stronghold_grid.add_widget(self.stronghold_grid.all_stronghold)

        # GRID LAYOUT [ Exchange pirate ]
        self.misc_grid = GridLayout(cols=2,
                                    row_force_default=True, row_default_height=60, col_default_width=60)
        self.MAIN_GRID.add_widget(self.misc_grid)

        self.exchange_lbl = Label(text='Misc:',
                                  pos_hint={'x': base_label_x + grid_step_x * 3, 'y': +0.45})
        self.misc_grid.add_widget(self.exchange_lbl)

        self.exchange_image = Image(source=LoAImages + 'Weekly_icon.png', size_hint=(0.5, 0.5),
                                    pos_hint={'x': base_image_x + grid_step_x * 3, 'y': +0.70})
        self.misc_grid.add_widget(self.exchange_image)
        # Checkbox
        self.misc_grid.ALL = Label(text='Exchange pirate')
        self.misc_grid.add_widget(self.misc_grid.ALL)
        self.misc_grid.ALL = CheckBox(ids=({'name': 'all_exchange'}))
        self.misc_grid.add_widget(self.misc_grid.ALL)
        self.misc_grid.ALL = Label(text='Pet status')
        self.misc_grid.add_widget(self.misc_grid.ALL)
        self.misc_grid.ALL = CheckBox(ids=({'name': 'pet_status'}))
        self.misc_grid.add_widget(self.misc_grid.ALL)

        # GRID LAYOUT [ CHAOS DUNGEON ]
        self.chaos_grid = GridLayout(cols=2,
                                     row_force_default=True, row_default_height=60, col_default_width=60)
        self.MAIN_GRID.add_widget(self.chaos_grid)

        self.chaos_lbl = Label(text='CHAOS DUNGEON:',
                               pos_hint={'x': base_label_x + grid_step_x * 3, 'y': +0.45})
        self.chaos_grid.add_widget(self.chaos_lbl)
        self.chaos_image = Image(source=LoAImages + 'Chaos_dungeon.png', size_hint=(0.5, 0.5),
                                 pos_hint={'x': base_image_x + grid_step_x * 3, 'y': +0.70})
        self.chaos_grid.add_widget(self.chaos_image)
        # Checkbox
        self.chaos_grid.Infinite_Chaos = Label(text='Infinite Chaos')
        self.chaos_grid.add_widget(self.chaos_grid.Infinite_Chaos)
        self.chaos_grid.Infinite_Chaos = CheckBox(ids=({'name': 'all_infinite_Chaos'}))
        self.chaos_grid.add_widget(self.chaos_grid.Infinite_Chaos)
        self.chaos_grid.Two_chaos = Label(text='2 daily chaos')
        self.chaos_grid.add_widget(self.chaos_grid.Two_chaos)
        self.chaos_grid.Two_chaos = CheckBox(ids=({'name': '2_daily_chaos'}))
        self.chaos_grid.add_widget(self.chaos_grid.Two_chaos)
        # BINDING Checkboxes
        self.chaos_grid.Infinite_Chaos.bind(active=self.uncheck_other)

        # CHARACTER SELECTION
        position_y = 0.15
        position_x = 0.05
        # WORKERS LAYOUT [ CHAOS DUNGEON ]
        self.work_lbl = Label(text='CURRENT WORKERS:',
                              pos_hint={'x': -0.464, 'y': -0.10})
        self.add_widget(self.work_lbl)

        self.worker_grid = GridLayout(pos_hint={'x': 0.02, 'y': 0.41}, cols=20, rows=2,
                                      size_hint=(0.01, 0.01), row_force_default=True,
                                      row_default_height=40, col_default_width=100)
        self.add_widget(self.worker_grid)
        # Needed for loop check
        self.worker_grid.empty = Label(ids=({'name': 'random name'}), text="")
        self.worker_grid.add_widget(self.worker_grid.empty)
        self.worker_grid.empty = Label(ids=({'name': 'random name'}), text="")
        self.worker_grid.add_widget(self.worker_grid.empty)
        # self.worker_grid.character2 = CheckBox(ids=({'name': ""}))
        # self.worker_grid.add_widget(self.worker_grid.character2)

        self.lbl_pirate = Label(text='Your roster will show here after update',
                                pos_hint={'x': 0, 'y': -0.2})
        self.add_widget(self.lbl_pirate)

        self.textinput_add = TextInput(hint_text="Add character?",
                                       pos_hint={'x': position_x, 'y': position_y + 0.05}, multiline=False,
                                       font_size=16, size_hint=(0.08, 0.04))

        self.textinput_add.bind(on_text_validate=self.on_text)
        self.add_widget(self.textinput_add)

        self.textinput_remove = TextInput(hint_text="Remove character?",
                                          pos_hint={'x': position_x, 'y': position_y}, multiline=False,
                                          font_size=16, size_hint=(0.08, 0.04))

        self.textinput_remove.bind(on_text_validate=self.remove_on_text)

        self.add_widget(self.textinput_remove)

        # create a big MAIN BUTTON 1280x720,1280x1024,1360x768,1440x900,1600x900,1920x1080
        self.mainbutton = Button(text='Select Character',
                                 border=(0, 0, 0, 0), width=2, height=3,
                                 size_hint=(0.07, 0.05),
                                 pos_hint={'x': position_x + 0.10, 'y': position_y})

        # show the dropdown menu when the main button is released
        # note: all the bind() calls pass the instance of the caller (here, the
        # mainbutton instance) as the first argument of the callback (here,
        # dropdown.open.).
        self.mainbutton.bind(on_release=self.dropdown.open)

        # one last thing, listen for the selection in the dropdown list and
        # assign the data to the button text.
        self.dropdown.bind(on_select=self.on_dropdown)

        self.add_widget(self.mainbutton)
        # Misc
        self.Return = Button(background_normal=LoAImages + 'Blue.jpg', border=(0, 0, 0, 0),
                             text="Return",
                             size_hint=(SizeW / 5, SizeH / 5), pos_hint={'x': .65, 'y': 0.05},
                             on_press=callbackTo2)
        self.add_widget(self.Return)

        self.Return = Button(background_normal=LoAImages + 'Blue.jpg', border=(0, 0, 0, 0),
                             text="Clear Finished list",
                             size_hint=(SizeW / 5, SizeH / 5), pos_hint={'x': .75, 'y': 0.05},
                             on_press=self.clear_finished)
        self.add_widget(self.Return)

        self.Start = Button(background_normal=LoAImages + 'Blue.jpg', border=(0, 0, 0, 0),
                            text="Start",
                            size_hint=(SizeW / 5, SizeH / 5), pos_hint={'x': .55, 'y': 0.05},
                            on_press=start_work)
        self.add_widget(self.Start)

        self.update_roster_button = Button(background_normal=LoAImages + 'Blue.jpg', border=(0, 0, 0, 0),
                                           text="Save settings", size_hint=(SizeW / 5, SizeH / 5),
                                           pos_hint={'x': .4, 'y': 0.15},
                                           on_press=self.save_settings)
        self.add_widget(self.update_roster_button)

        self.skills = Button(background_normal=LoAImages + 'Blue.jpg', text="Skills",
                             size_hint=(SizeW/4, SizeH / 4), pos_hint={'x': .90, 'y': 0.05},
                             on_press=callbackTo4)
        self.add_widget(self.skills)

        self.on_start()
        Clock.schedule_interval(self.update, 2)

    def update(self, *args):
        self.lbl_pirate.text = "Your CHARACTERS:" + str(roster_list)
        # updating workers
        count_checkbox = 0
        # for x in self.worker_grid.children:
        #     count_checkbox += 1
        for x in np.unique(roster_list):
            for n in self.worker_grid.children:
                if x not in worker_list:
                    # if n.ids.get("name") != x:
                    # print(n.ids.get("name"), x)
                    self.worker_grid.character = Label(text=str(x))
                    self.worker_grid.add_widget(self.worker_grid.character)
                    self.worker_grid.character = CheckBox(ids=({'name': x}))
                    self.worker_grid.add_widget(self.worker_grid.character)
                    worker_list.append(x)
        # CONFIG - > CHECKBOX WORKER LIST [PROBLEM IS IT UPDATES too often and not checkbox ->config ]
        # checkbox_instances = [self.worker_grid]
        # for box_instance in checkbox_instances:
        #     # READING STATUS FROM CONFIG
        #     for section_name in configparser.sections():
        #         # print('Section:', section_name)
        #         # print('  Options:', ConfigParser.options(section_name))
        #         option = configparser.options(section_name)
        #         # print("STATUS IS", section_name)
        #         for name, value in configparser.items(section_name):
        #             # print('  %s = %s' % (name, value))
        #             config_name = name
        #             config_value = value
        #             # Looking at CHECKBOXES
        #             if section_name == "Workers":
        #                 for n in box_instance.children:
        #                     # print(option, "OPTION AND CHECKED IS : ", value)
        #                     # CONFIG 2 CHECKBOX
        #                     # print(n)
        #                     # print("CONFIG NAME:", config_name)
        #                     # if section_name == selected_character:
        #                     # print(n, n.ids.get("name"))
        #                     if "label" in str(n) or "image" in str(n):
        #                         123
        #                     else:
        #                         if n.ids.get("name") == config_name.capitalize():
        #                             # print(n.ids.get("name"), config_name.capitalize())
        #                             # print("ENTERED ", n.ids.get("name"), config_name)
        #                             if config_value == "yes":
        #                                 try:
        #                                     # print(n.ids.get("name"), " IS TRUE")
        #                                     n.active = True
        #                                 except:
        #                                     print("NOT A CHECKBOX")
        #                             else:
        #                                 try:
        #                                     n.active = False
        #                                 except:
        #                                     print("DISABLE NOT A CHECKBOX")

    def clear_finished(self, *args):
        for name, value in configparser.items("Finished_Characters"):
            if value == "yes":
                configparser.set("Finished_Characters", name, "no")
                configparser.write()

    def start_tasks(self, unusedarg):
        for n in self.silver_checkbox.children:
            if n.active and n.ids.get("name") == "ALL":
                print("Doing Lopang Daily...")
                callbackTo2(self)
                # lopang_daily()
                print(n.ids.get("name"))

    def disable_numpad(self):
        for child in reversed(self.ids.button_grid.children):
            if isinstance(child, Button):
                child.disabled = not child.disabled
                child.opacity = 0 if child.disabled else 1

    def uncheck_other(self, checkboxInstance, isActive):
        if isActive:
            # Parent of Checkbox and then children within it
            for n in checkboxInstance.parent.children:
                # print(str(n))
                if "label" in str(n) or "image" in str(n):
                    123
                else:
                    if "all_" not in n.ids.get("name"):
                        n.active = False
                        n.disabled = True
        if not isActive:
            for n in checkboxInstance.parent.children:
                if "label" in str(n) or "image" in str(n):
                    123
                else:
                    if "all_" not in n.ids.get("name"):
                        n.disabled = False

    # def go_through_all(self,checkboxInstance):
    #     count = 0
    #     for n in checkboxInstance.parent.children:
    #         print(count)
    #         print(n)
    #         count = count + 1

    def status_of_checkboxes(self, checkboxInstance):
        configparser.read("myapp.ini")
        if selected_character != '':
            # READING STATUS FROM CONFIG
            for section_name in configparser.sections():
                # print('Section:', section_name)
                # print('  Options:', ConfigParser.options(section_name))
                option = configparser.options(section_name)
                # print("STATUS IS", section_name)
                for name, value in configparser.items(section_name):
                    # print('  %s = %s' % (name, value))
                    config_name = name
                    config_value = value
                for n in checkboxInstance.children:
                    # print(option, "OPTION AND CHECKED IS : ", value)
                    # print(checkboxInstance.children)
                    if section_name == selected_character:
                        if n.ids.get("name") == config_name:
                            if config_value == "yes":
                                try:
                                    n.active = True
                                except:
                                    print("NOT A CHECKBOX")
                            else:
                                try:
                                    n.active = False
                                except:
                                    print("DISABLE NOT A CHECKBOX")

    def save_settings(self, *args):
        checkbox_instances = [self.silver_grid, self.leapstone_grid, self.guild_grid,
                              self.presets_grid, self.weekly_grid, self.stronghold_grid,
                              self.chaos_grid, self.worker_grid, self.misc_grid]
        # ADD CODE HERE IF SELECTED CHARACTER IS "ALL" then change value for all characters in database to the
        # checkbox values of "ALL"
        if selected_character != '':
            for box_instance in checkbox_instances:
                # For Work grid
                configparser.read("myapp.ini")
                # Looking at CHECKBOXES
                for n in box_instance.children:
                    # CHECKBOX to->> config
                    if "label" in str(n) or "image" in str(n):
                        123
                    else:
                        if box_instance == self.worker_grid:
                            if n.active:
                                try:
                                    Config.set("Workers", n.ids.get("name"), "yes")
                                except:
                                    123
                                    # print(selected_character, "Already in section")
                                configparser.set("Workers", n.ids.get("name"), "yes")
                            elif not n.active:
                                configparser.set("Workers", n.ids.get("name"), "no")
                        else:
                            if n.active:
                                try:
                                    Config.add_section(selected_character)
                                except:
                                    123
                                    # print(selected_character, "Already in section")
                                configparser.set(selected_character, n.ids.get("name"), "yes")
                                print(n.ids.get("name"))
                            elif not n.active:
                                configparser.set(selected_character, n.ids.get("name"), "no")
                configparser.write()
            print("SAVED TO CONFIG")
        else:
            print("Write your character name")

    def set_approval_rating(self):
        if self.ids.checkbox.active:  # checkbox checked i.e. True
            print("its active")
        else:
            print("not active")

    # This is instantce execution of CHECKBox IF Active
    def daily_quest_check(self, checkboxInstance, isActive):
        global PirateCoins
        print(checkboxInstance)
        if isActive:
            print(" STARTING lopang_daily")
            # lopang_daily()
        else:
            print("lopang daily off")

    def on_dropdown(self, checkboxinstance, checkboxvalue):
        global selected_character
        self.mainbutton.text = checkboxvalue
        selected_character = checkboxvalue
        print("SELECTED CHARACTER : ", selected_character)
        checkbox_instances = [self.silver_grid, self.leapstone_grid, self.guild_grid,
                              self.presets_grid, self.weekly_grid, self.stronghold_grid,
                              self.chaos_grid, self.worker_grid, self.misc_grid]
        for box_instance in checkbox_instances:
            # READING STATUS FROM CONFIG
            for section_name in configparser.sections():
                # print('Section:', section_name)
                # print('  Options:', ConfigParser.options(section_name))
                option = configparser.options(section_name)
                # print("STATUS IS", section_name)
                for name, value in configparser.items(section_name):
                    # print('  %s = %s' % (name, value))
                    config_name = name
                    config_value = value
                    # Looking at CHECKBOXES
                    if section_name == selected_character:
                        for n in box_instance.children:
                            # print(option, "OPTION AND CHECKED IS : ", value)
                            # print(checkboxInstance.children)
                            # CONFIG 2 CHECKBOX
                            # print(n.ids.get("name"))
                            # print("CONFIG NAME:", config_name)
                            # if section_name == selected_character:
                            # print(n, n.ids.get("name"))
                            if n.ids.get("name") == config_name:
                                # print("ENTERED ", n.ids.get("name"), config_name)

                                if config_value == "yes":
                                    try:
                                        # print(n.ids.get("name"), " IS TRUE")
                                        n.active = True
                                    except:
                                        print("NOT A CHECKBOX")
                                else:
                                    try:
                                        n.active = False
                                    except:
                                        print("DISABLE NOT A CHECKBOX")

        # Based on selected character add values of selected tasks and other things to config file

    def on_text(self, instance):
        print(roster_array, roster_list)
        roster_list.append(self.textinput_add.text)
        # roster_array.append(self.textinput_add.text)
        self.textinput_add.text = ''
        self.update_roster()
        # adding character to config?

    def remove_on_text(self, instance):
        count = 0
        configparser.read('myapp.ini')
        try:
            for x in np.array(roster_list):
                character = 'character'
                count = count + 1
                character = "" + character + str(count)
                print(character, x)
                if x == self.textinput_remove.text:
                    print("removing this ", x)
                    configparser.remove_option('account', character)
            configparser.remove_section(self.textinput_remove.text)
            roster_list.remove(self.textinput_remove.text)
            configparser.write()
        except:
            print("No character with that name!")
        self.textinput_remove.text = ''
        self.update_roster()
        configparser.write()

        # adding character to config?

    def update_roster(self, *args):
        print("UPDATING roster")
        global roster_list
        global roster_array
        self.dropdown.clear_widgets()
        count = 0
        for x in np.unique(roster_list):
            character = 'character'
            count = count + 1
            character = "" + character + str(count)
            # print(character, x)
            configparser.set('account', character, x)
            if x not in configparser.sections():
                configparser.add_section(x)
            configparser.write()
        roster_list.clear()

        # Building roster_list from CONFIG
        for i in range(1, 24, 1):
            character = 'character'
            character = "" + character + str(i)
            # print(character)
            try:
                roster_list.append(configparser.get('account', character))
            except:
                123
                # print("no option")
        # print(roster_list)

        for index in roster_list:
            # When adding widgets, we need to specify the height manually
            # (disabling the size_hint_y) so the dropdown can calculate
            # the area it needs.

            self.btn = Button(text=index, size_hint_y=None, height=44)

            # for each button, attach a callback that will call the select() method
            # on the dropdown. We'll pass the text of the button as the data of the
            # selection.
            self.btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))

            # then add the BUTTON INSIDE the dropdown
            self.dropdown.add_widget(self.btn)

    def on_start(self, *args):
        self.update_roster()
        # self.leapstone_checkbox
        configparser.read("myapp.ini")
        # if selected_character != '':
        # self.status_of_checkboxes(self.guild_checkbox)
        # print("printing guild checkbox from on_start", self.guild_checkbox)
        # self.status_of_checkboxes(self.guild_checkbox)

    def on_keyboard(self, window, key, scancode, codepoint, modifier, *args):
        global Enemies
        Enemies = modifier, codepoint
        # print(' - modifiers are %r', modifier)
        # print('The key', codepoint, 'have been pressed')
        if modifier == ['ctrl', 'numlock'] and codepoint == 'q':
            global stop_threads
            stop_threads = True
            self.stop()
            print("pressed CTRL + Q")


class Calculate(Screen):
    # @mainthread
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        super(Calculate, self).__init__(name='Calculate')

        # positions
        ButtonY = 0.5
        SizeH = 0.2
        SizeW = 0.1
        PosX = .65
        # Checkbox
        CheckH = 0.1
        CheckW = 0.1

        global FeverTime
        ##PIRATE COINS MENU
        global PirateCoins
        global NumberofChar
        Charinput = TextInput(hint_text="No of char?",
                              pos_hint={'x': .07, 'y': 0.92}, multiline=False,
                              font_size=16, size_hint=(0.05, 0.06), width=2, height=3)

        def on_text(instance):
            global NumberofChar
            NumberofChar = int(Charinput.text)

        Charinput.bind(on_text_validate=on_text)

        self.add_widget(Charinput)

        # Label
        self.lbl_pirate = Label(text='Pirate coins needed this week:',
                                pos_hint={'x': -.45, 'y': +0.45})
        self.add_widget(self.lbl_pirate)

        self.pirate_gold = Label(text='Gold earned:',
                                 pos_hint={'x': -.25, 'y': +0.45})
        self.add_widget(self.pirate_gold)

        self.pirate_coins = Image(source=LoAImages + 'Pirate coin.png',
                                  size_hint=(0.5, 0.5), pos_hint={'x': -.24, 'y': +0.70})
        self.add_widget(self.pirate_coins)

        # GRID LAYOUT
        layoutCheckbox = GridLayout(pos_hint={'x': 0.03, 'y': 0.93}, cols=1, size_hint=(0.01, 0.01),
                                    row_force_default=True, row_default_height=77, col_default_width=60)
        self.add_widget(layoutCheckbox)  # <<<<<<<<<<<<<<<<<

        layoutImage = GridLayout(pos_hint={'x': -.49, 'y': .19}, cols=1, size_hint=(1, 0.75),
                                 row_force_default=True, row_default_height=80)
        self.add_widget(layoutImage)  # <<<<<<<<<<<<<<<<<

        # Checkbox
        layoutCheckbox.cb_D_stone = CheckBox(active=True)
        layoutCheckbox.add_widget(layoutCheckbox.cb_D_stone)
        layoutCheckbox.cb_G_stone = CheckBox(active=True)
        layoutCheckbox.add_widget(layoutCheckbox.cb_G_stone)
        layoutCheckbox.cb_shard_pouch = CheckBox(active=True)
        layoutCheckbox.add_widget(layoutCheckbox.cb_shard_pouch)

        # images
        layoutImage.Image_D_stone = Image(source=LoAImages + 'Destruction stone T3.png', )
        layoutImage.add_widget(layoutImage.Image_D_stone)
        layoutImage.Image_G_stone = Image(source=LoAImages + 'Guardian stone T3.png')
        layoutImage.add_widget(layoutImage.Image_G_stone)
        layoutImage.image_shard_pouch = Image(source=LoAImages + 'Shard pouch.png')
        layoutImage.add_widget(layoutImage.image_shard_pouch)

        # Attach a callback
        layoutCheckbox.cb_D_stone.bind(active=self.Pirate_D_Active)
        layoutCheckbox.cb_G_stone.bind(active=self.Pirate_G_Active)
        layoutCheckbox.cb_shard_pouch.bind(active=self.Pirate_Shard_Active)

        ###
        ##Honor SHOP MENU
        FeverTime = 135
        textinput = TextInput(hint_text="Current amount?",
                              pos_hint={'x': 0.23, 'y': 0.92}, multiline=False,
                              font_size=16, size_hint=(0.05, 0.06), width=2, height=3)

        def on_text(instance):
            global CurrentCoins
            CurrentCoins = int(textinput.text)

        textinput.bind(on_text_validate=on_text)

        self.add_widget(textinput)
        # Label
        self.Courage = Image(source=LoAImages + 'Coin of Courage.png',
                             size_hint=(0.5, 0.5), pos_hint={'x': -.04, 'y': +0.70})
        self.add_widget(self.Courage)

        self.lbl_courage = Label(text='Proof of courage Needed',
                                 pos_hint={'x': -.2, 'y': +0.45})
        self.add_widget(self.lbl_courage)

        self.lbl_courage_time = Label(text='Time Needed',
                                      pos_hint={'x': -0.15, 'y': +0.45})
        self.add_widget(self.lbl_courage_time)
        ########
        PvpMethod = ["Team Elemination", "3v3", "Coop", "FFA"]

        # create a dropdown with 10 buttons
        self.dropdown = DropDown()
        for index in PvpMethod:
            # When adding widgets, we need to specify the height manually
            # (disabling the size_hint_y) so the dropdown can calculate
            # the area it needs.

            self.btn = Button(text=index, size_hint_y=None, height=44)

            # for each button, attach a callback that will call the select() method
            # on the dropdown. We'll pass the text of the button as the data of the
            # selection.
            self.btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))

            # then add the BUTTON INSIDE the dropdown
            self.dropdown.add_widget(self.btn)

        # create a big MAIN BUTTON 1280x720,1280x1024,1360x768,1440x900,1600x900,1920x1080
        mainbutton = Button(text='Farming Method',
                            border=(0, 0, 0, 0),
                            size_hint=(0.07, 0.05),
                            pos_hint={'x': .29, 'y': 0.86})

        # show the dropdown menu when the main button is released
        # note: all the bind() calls pass the instance of the caller (here, the
        # mainbutton instance) as the first argument of the callback (here,
        # dropdown.open.).
        mainbutton.bind(on_release=self.dropdown.open)

        # one last thing, listen for the selection in the dropdown list and
        # assign the data to the button text.
        self.dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

        self.add_widget(mainbutton)

        #######

        ##GRID LAYOUT
        courage_layoutCheckbox = GridLayout(pos_hint={'x': 0.15, 'y': 0.8}, cols=1, size_hint=(0.1, 0.1),
                                            row_force_default=True, row_default_height=50, col_default_width=120)
        self.add_widget(courage_layoutCheckbox)  # <<<<<<<<<<<<<<<<<

        courage_layoutImage = GridLayout(pos_hint={'x': 0.20, 'y': 0.8}, cols=1, size_hint=(0.1, 0.1),
                                         row_force_default=True, row_default_height=50)
        self.add_widget(courage_layoutImage)  # <<<<<<<<<<<<<<<<<
        # Checkbox
        courage_layoutCheckbox.Fever_time = CheckBox(active=True)
        courage_layoutCheckbox.add_widget(courage_layoutCheckbox.Fever_time)
        courage_layoutCheckbox.cb_D_stone = CheckBox(active=True)
        courage_layoutCheckbox.add_widget(courage_layoutCheckbox.cb_D_stone)
        courage_layoutCheckbox.cb_G_stone = CheckBox(active=True)
        courage_layoutCheckbox.add_widget(courage_layoutCheckbox.cb_G_stone)
        courage_layoutCheckbox.cb_Shards_L = CheckBox(active=True)
        courage_layoutCheckbox.add_widget(courage_layoutCheckbox.cb_Shards_L)
        courage_layoutCheckbox.cb_Leapstone = CheckBox(active=True)
        courage_layoutCheckbox.add_widget(courage_layoutCheckbox.cb_Leapstone)
        courage_layoutCheckbox.cb_GLeapstone = CheckBox(active=True)
        courage_layoutCheckbox.add_widget(courage_layoutCheckbox.cb_GLeapstone)
        courage_layoutCheckbox.cb_Grace = CheckBox(active=True)
        courage_layoutCheckbox.add_widget(courage_layoutCheckbox.cb_Grace)
        courage_layoutCheckbox.cb_Blessing = CheckBox(active=True)
        courage_layoutCheckbox.add_widget(courage_layoutCheckbox.cb_Blessing)
        courage_layoutCheckbox.cb_Protection = CheckBox(active=True)
        courage_layoutCheckbox.add_widget(courage_layoutCheckbox.cb_Protection)

        # images
        courage_layoutImage.Image_Fever_time = Image(source=LoAImages + 'pvp_event.png', )
        courage_layoutImage.add_widget(courage_layoutImage.Image_Fever_time)
        courage_layoutImage.Image_D_stone = Image(source=LoAImages + 'Destruction stone T3.png', )
        courage_layoutImage.add_widget(courage_layoutImage.Image_D_stone)
        courage_layoutImage.Image_G_stone = Image(source=LoAImages + 'Guardian stone T3.png')
        courage_layoutImage.add_widget(courage_layoutImage.Image_G_stone)
        courage_layoutImage.Image_Shards_L = Image(source=LoAImages + 'Honor Shard L.png')
        courage_layoutImage.add_widget(courage_layoutImage.Image_Shards_L)

        courage_layoutImage.Image_GLeapstone = Image(source=LoAImages + 'Greater Honor leapstone.png')
        courage_layoutImage.add_widget(courage_layoutImage.Image_GLeapstone)
        courage_layoutImage.Image_Leapstone = Image(source=LoAImages + 'Honor Leapstone.png')
        courage_layoutImage.add_widget(courage_layoutImage.Image_Leapstone)

        courage_layoutImage.Image_Grace = Image(source=LoAImages + 'Solar Grace.png')
        courage_layoutImage.add_widget(courage_layoutImage.Image_Grace)
        courage_layoutImage.Image_Blessing = Image(source=LoAImages + 'Solar Blessings.png')
        courage_layoutImage.add_widget(courage_layoutImage.Image_Blessing)
        courage_layoutImage.Image_Protection = Image(source=LoAImages + 'Solar Protection.png')
        courage_layoutImage.add_widget(courage_layoutImage.Image_Protection)

        # Attach a callback
        courage_layoutCheckbox.Fever_time.bind(active=self.Fever_time_Active)
        courage_layoutCheckbox.cb_D_stone.bind(active=self.Courage_D_Active)
        courage_layoutCheckbox.cb_G_stone.bind(active=self.Courage_G_Active)
        courage_layoutCheckbox.cb_Shards_L.bind(active=self.Courage_Shards_Active)

        courage_layoutCheckbox.cb_GLeapstone.bind(active=self.Courage_GLeapstone_Active)
        courage_layoutCheckbox.cb_Leapstone.bind(active=self.Courage_Leapstone_Active)

        courage_layoutCheckbox.cb_Grace.bind(active=self.Courage_Grace_Active)
        courage_layoutCheckbox.cb_Blessing.bind(active=self.Courage_Blessing_Active)
        courage_layoutCheckbox.cb_Protection.bind(active=self.Courage_Protection_Active)

        ###Guild SHOP
        # Label
        self.bloodstone = Image(source=LoAImages + 'Bloodcrystal.png',
                                size_hint=(0.5, 0.5), pos_hint={'x': .17, 'y': +0.70})
        self.add_widget(self.bloodstone)

        self.lbl_bloodstone = Label(text='Bloodstones Needed',
                                    pos_hint={'x': 0, 'y': +0.45})
        self.add_widget(self.lbl_bloodstone)

        self.lbl_bloodstone_time = Label(text='Time Needed',
                                         pos_hint={'x': 0.06, 'y': +0.45})
        self.add_widget(self.lbl_bloodstone_time)

        ##GRID LAYOUT
        bloodstone_layoutCheckbox = GridLayout(pos_hint={'x': 0.42, 'y': 0.8}, cols=1, size_hint=(0.1, 0.1),
                                               row_force_default=True, row_default_height=50, col_default_width=120)
        self.add_widget(bloodstone_layoutCheckbox)  # <<<<<<<<<<<<<<<<<

        bloodstone_layoutImage = GridLayout(pos_hint={'x': 0.37, 'y': 0.8}, cols=1, size_hint=(0.1, 0.1),
                                            row_force_default=True, row_default_height=50)
        self.add_widget(bloodstone_layoutImage)  # <<<<<<<<<<<<<<<<<
        # Checkbox
        bloodstone_layoutCheckbox.cb_D_stone = CheckBox(active=True)
        bloodstone_layoutCheckbox.add_widget(bloodstone_layoutCheckbox.cb_D_stone)
        bloodstone_layoutCheckbox.cb_G_stone = CheckBox(active=True)
        bloodstone_layoutCheckbox.add_widget(bloodstone_layoutCheckbox.cb_G_stone)
        bloodstone_layoutCheckbox.cb_Shards_L = CheckBox(active=True)
        bloodstone_layoutCheckbox.add_widget(bloodstone_layoutCheckbox.cb_Shards_L)
        bloodstone_layoutCheckbox.cb_Leapstone = CheckBox(active=True)
        bloodstone_layoutCheckbox.add_widget(bloodstone_layoutCheckbox.cb_Leapstone)
        bloodstone_layoutCheckbox.cb_GLeapstone = CheckBox(active=True)
        bloodstone_layoutCheckbox.add_widget(bloodstone_layoutCheckbox.cb_GLeapstone)
        bloodstone_layoutCheckbox.cb_Ticket = CheckBox(active=True)
        bloodstone_layoutCheckbox.add_widget(bloodstone_layoutCheckbox.cb_Ticket)

        # images
        bloodstone_layoutImage.Image_D_stone = Image(source=LoAImages + 'Destruction stone T3.png', )
        bloodstone_layoutImage.add_widget(bloodstone_layoutImage.Image_D_stone)
        bloodstone_layoutImage.Image_G_stone = Image(source=LoAImages + 'Guardian stone T3.png')
        bloodstone_layoutImage.add_widget(bloodstone_layoutImage.Image_G_stone)
        bloodstone_layoutImage.Image_Shards_L = Image(source=LoAImages + 'Honor Shard S.png')
        bloodstone_layoutImage.add_widget(bloodstone_layoutImage.Image_Shards_L)

        bloodstone_layoutImage.Image_GLeapstone = Image(source=LoAImages + 'Greater Honor leapstone.png')
        bloodstone_layoutImage.add_widget(bloodstone_layoutImage.Image_GLeapstone)
        bloodstone_layoutImage.Image_Leapstone = Image(source=LoAImages + 'Honor Leapstone.png')
        bloodstone_layoutImage.add_widget(bloodstone_layoutImage.Image_Leapstone)
        bloodstone_layoutImage.Image_Ticket = Image(source=LoAImages + 'Chest T2.png')
        bloodstone_layoutImage.add_widget(bloodstone_layoutImage.Image_Ticket)
        bloodstone_layoutImage.Image_Supply = Image(source=LoAImages + 'Chest Supply.png')
        bloodstone_layoutImage.add_widget(bloodstone_layoutImage.Image_Supply)

        # Attach a callback
        bloodstone_layoutCheckbox.cb_D_stone.bind(active=self.Courage_D_Active)
        bloodstone_layoutCheckbox.cb_G_stone.bind(active=self.Courage_G_Active)
        bloodstone_layoutCheckbox.cb_Shards_L.bind(active=self.Courage_Shards_Active)

        bloodstone_layoutCheckbox.cb_GLeapstone.bind(active=self.Courage_GLeapstone_Active)
        bloodstone_layoutCheckbox.cb_Leapstone.bind(active=self.Courage_Leapstone_Active)

        self.mainmenu = Button(background_normal=LoAImages + 'Yellow.jpg',
                               border=(0, 0, 0, 0),
                               text="Main Menu", size_hint=(SizeW, SizeH / 2), pos_hint={'x': .0, 'y': 0.1}
                               , on_press=callbackTo2)
        self.add_widget(self.mainmenu)

        self.skills = Button(background_normal=LoAImages + 'Blue.jpg', border=(0, 0, 0, 0),
                             text="Skills", size_hint=(SizeW, SizeH / 2), pos_hint={'x': .80, 'y': 0.1},
                             on_press=callbackTo4)
        self.add_widget(self.skills)

        self.DailyQuests = Button(background_normal=LoAImages + 'Blue.jpg', border=(0, 0, 0, 0),
                                  text="Tasks", size_hint=(SizeW, SizeH / 2), pos_hint={'x': .80, 'y': 0.22},
                                  on_press=callbackTo6)
        self.add_widget(self.DailyQuests)

        Clock.schedule_interval(self.update, 0.3)

    def update(self, *args):
        self.lbl_pirate.text = str(PirateCoins * NumberofChar)
        self.pirate_gold.text = str(PirateGold * NumberofChar)
        self.lbl_courage.text = str(CoinOfCourage - CurrentCoins)
        self.lbl_courage_time.text = "Time2get: " + str(round((CoinOfCourage - CurrentCoins) / FeverTime * 3)) \
                                     + " Minutes"
        # print("this is global labe", GlobalLabel, "test")

        # Pirate SHOP

    def Pirate_D_Active(self, checkboxInstance, isActive):
        global PirateCoins
        if isActive:
            PirateCoins = PirateCoins + 9900
        else:
            PirateCoins = PirateCoins - 9900

    def Pirate_Shard_Active(self, checkboxInstance, isActive):
        global PirateCoins
        if isActive:
            PirateCoins = PirateCoins + 4000
        else:
            PirateCoins = PirateCoins - 4000

    def Pirate_G_Active(self, checkboxInstance, isActive):
        global PirateCoins
        if isActive:
            PirateCoins = PirateCoins + 6300
        else:
            PirateCoins = PirateCoins - 6300

        ##PVP SHOP

    def Fever_time_Active(self, checkboxInstance, isActive):
        global FeverTime
        if isActive:
            FeverTime = 135
        else:
            FeverTime = 90

    def Courage_G_Active(self, checkboxInstance, isActive):
        global CoinOfCourage
        global PirateGold
        if isActive:
            PirateGold = PirateGold + 5000
            CoinOfCourage = CoinOfCourage + 6320
        else:
            CoinOfCourage = CoinOfCourage - 6320

    def Courage_D_Active(self, checkboxInstance, isActive):
        global CoinOfCourage
        if isActive:
            CoinOfCourage = CoinOfCourage + 3840
        else:
            CoinOfCourage = CoinOfCourage - 3840

    def Courage_Shards_Active(self, checkboxInstance, isActive):
        global CoinOfCourage
        if isActive:
            CoinOfCourage = CoinOfCourage + 16080
        else:
            CoinOfCourage = CoinOfCourage - 16080

    def Courage_Leapstone_Active(self, checkboxInstance, isActive):
        global CoinOfCourage
        if isActive:
            CoinOfCourage = CoinOfCourage + 2240
        else:
            CoinOfCourage = CoinOfCourage - 2240

    def Courage_GLeapstone_Active(self, checkboxInstance, isActive):
        global CoinOfCourage
        if isActive:
            CoinOfCourage = CoinOfCourage + 1120
        else:
            CoinOfCourage = CoinOfCourage - 1120

    def Courage_Grace_Active(self, checkboxInstance, isActive):
        global CoinOfCourage
        if isActive:
            CoinOfCourage = CoinOfCourage + 3840
        else:
            CoinOfCourage = CoinOfCourage - 3840

    def Courage_Blessing_Active(self, checkboxInstance, isActive):
        global CoinOfCourage
        if isActive:
            CoinOfCourage = CoinOfCourage + 5000
        else:
            CoinOfCourage = CoinOfCourage - 5000

    def Courage_Protection_Active(self, checkboxInstance, isActive):
        global CoinOfCourage
        if isActive:
            CoinOfCourage = CoinOfCourage + 4320
        else:
            CoinOfCourage = CoinOfCourage - 4320
    ##GUILD SHOP
    # def Courage_G_Active(self, checkboxInstance, isActive):
    #     global CoinOfCourage
    #     if isActive:
    #         CoinOfCourage = CoinOfCourage + 6320
    #     else:
    #         CoinOfCourage = CoinOfCourage - 6320
    #
    # def Courage_D_Active(self, checkboxInstance, isActive):
    #     global CoinOfCourage
    #     if isActive:
    #         CoinOfCourage = CoinOfCourage + 3840
    #     else:
    #         CoinOfCourage = CoinOfCourage - 3840
    #
    # def Courage_Shards_Active(self, checkboxInstance, isActive):
    #     global CoinOfCourage
    #     if isActive:
    #         CoinOfCourage = CoinOfCourage + 16080
    #     else:
    #         CoinOfCourage = CoinOfCourage - 16080
    #
    # def Courage_Leapstone_Active(self, checkboxInstance, isActive):
    #     global CoinOfCourage
    #     if isActive:
    #         CoinOfCourage = CoinOfCourage + 2240
    #     else:
    #         CoinOfCourage = CoinOfCourage - 2240
    #
    # def Courage_GLeapstone_Active(self, checkboxInstance, isActive):
    #     global CoinOfCourage
    #     if isActive:
    #         CoinOfCourage = CoinOfCourage + 1120
    #     else:
    #         CoinOfCourage = CoinOfCourage - 1120


class Settings(Screen):
    # @mainthread
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        super(Settings, self).__init__(name='Settings')
        # Positions
        ButtonY = 0.5
        SizeH = 0.2
        SizeW = 0.1
        resolutions = ["2560x1080", "1920x1080", "1366x768", "1280x768", "1280x720"]

        self.tittle_grid = GridLayout(pos_hint={'x': 0.0575, 'y': -0.05}, rows=4, cols=2,
                                      size_hint=(0.1, 1),
                                      row_force_default=True, row_default_height=30, col_default_width=120)
        self.add_widget(self.tittle_grid)
        self.tittle_1 = Label(text='SCREEN SETTINGS', font_size=20,bold=True,
                              halign="center", valign="middle")
        self.tittle_grid.add_widget(self.tittle_1)

        self.main_grid = GridLayout(pos_hint={'x': 0.025, 'y': -0.15}, rows=4, cols=2,
                                    size_hint=(0.1, 1),
                                    row_force_default=True, row_default_height=30, col_default_width=120)
        self.add_widget(self.main_grid)
        self.lbl_resolution = Label(text='Resolution:')
        self.main_grid.add_widget(self.lbl_resolution)

        # create a dropdown with 10 buttons
        self.dropdown = DropDown()
        self.dropdown.bind(on_select=self.on_dropdown)
        for index in resolutions:
            # When adding widgets, we need to specify the height manually
            # (disabling the size_hint_y) so the dropdown can calculate
            # the area it needs.
            self.btn = Button(text=index, size_hint_y=None, height=44)
            # for each button, attach a callback that will call the select() method
            # on the dropdown. We'll pass the text of the button as the data of the
            # selection.
            self.btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            # then add the BUTTON INSIDE the dropdown
            self.dropdown.add_widget(self.btn)
        # create a big MAIN BUTTON 1280x720,1280x1024,1360x768,1440x900,1600x900,1920x1080
        self.mainbutton = Button(text='Resolution',
                                 border=(0, 0, 0, 0),
                                 size_hint=(0.07, 0.05),
                                 pos_hint={'x': .29, 'y': 0.86})
        # show the dropdown menu when the main button is released
        # note: all the bind() calls pass the instance of the caller (here, the
        # mainbutton instance) as the first argument of the callback (here,
        # dropdown.open.).
        self.mainbutton.bind(on_release=self.dropdown.open)
        # one last thing, listen for the selection in the dropdown list and
        # assign the data to the button text.
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))
        self.main_grid.add_widget(self.mainbutton)

        self.mainmenu = Button(background_normal=LoAImages + 'Yellow.jpg',
                               border=(0, 0, 0, 0),
                               text="Main Menu", size_hint=(SizeW, SizeH / 2), pos_hint={'x': .0, 'y': 0.1}
                               , on_press=callbackTo2)
        self.add_widget(self.mainmenu)

        self.skills = Button(background_normal=LoAImages + 'Blue.jpg', border=(0, 0, 0, 0),
                             text="Skills", size_hint=(SizeW, SizeH / 2), pos_hint={'x': .80, 'y': 0.1},
                             on_press=callbackTo4)
        self.add_widget(self.skills)

        self.DailyQuests = Button(background_normal=LoAImages + 'Blue.jpg', border=(0, 0, 0, 0),
                                  text="Tasks", size_hint=(SizeW, SizeH / 2), pos_hint={'x': .80, 'y': 0.22},
                                  on_press=callbackTo6)
        self.add_widget(self.DailyQuests)

        Clock.schedule_interval(self.update, 0.3)
        self.on_start()

    def update(self, *args):
        self.mainbutton.text = configparser.get('Settings', "resolution")
        # print(selected_character)
        # self.dropdown.reload()
        # self.lbl_pirate.text = str(PirateCoins * NumberofChar)
        # self.pirate_gold.text = str(PirateGold * NumberofChar)
        # self.lbl_courage.text = str(CoinOfCourage - CurrentCoins)
        # self.lbl_courage_time.text = "Time2get: " + str(round((CoinOfCourage - CurrentCoins) / FeverTime * 3)) \
        #                              + " Minutes"
        # print("this is global labe", GlobalLabel, "test")

    def on_dropdown(self, checkboxinstance, checkboxvalue):
        global Resolution
        # print(checkboxinstance, checkboxvalue)
        self.mainbutton.text = checkboxvalue
        Resolution = [int(checkboxvalue.split("x")[0]),
                      int(checkboxvalue.split("x")[1])]
        try:
            configparser.get('Settings', "resolution")
        except:
            configparser.add_section('Settings')
        configparser.set('Settings', "resolution", checkboxvalue)
        configparser.write()
        # Based on selected character add values of selected tasks and other things to config file

    def on_text(self, instance):
        print(roster_array, roster_list)
        roster_list.append(self.textinput_add.text)
        # roster_array.append(self.textinput_add.text)
        self.textinput_add.text = ''
        self.update_roster()
        # adding character to config?

    def remove_on_text(self, instance):
        count = 0
        try:
            print(roster_list)
            for x in np.array(roster_list):
                character = 'character'
                count = count + 1
                character = "" + character + str(count)
                print(character, x)
                configparser.set('account', character, x)
                configparser.write()
                if x == self.textinput_remove.text:
                    print("removing this shit", x)
                    roster_list.remove(self.textinput_remove.text)
                    configparser.remove_option('account', character)
            roster_list.remove(self.textinput_remove.text)
        except:
            print("No character with that name!")
        self.textinput_remove.text = ''
        self.update_roster()

        # adding character to config?


        for index in roster_list:
            # When adding widgets, we need to specify the height manually
            # (disabling the size_hint_y) so the dropdown can calculate
            # the area it needs.

            self.btn = Button(text=index, size_hint_y=None, height=44)

            # for each button, attach a callback that will call the select() method
            # on the dropdown. We'll pass the text of the button as the data of the
            # selection.
            self.btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))

            # then add the BUTTON INSIDE the dropdown
            self.dropdown.add_widget(self.btn)

    def on_start(self, *args):
        123
        # Executes things on startup where self.on_start() is
        # print("THIS IS ON START")
        # time.sleep(5)


class Grids(GridLayout):
    def __init__(self):
        GridLayout.__init__(self, cols=3, rows=3);
        self.add_widget(MainMenu());
        self.add_widget(Settings());
        self.add_widget(Debugging());
        self.add_widget(Skills());
        self.add_widget(Lifeskills());
        self.on_start()

    def on_start(self, *args):
        # ALWAYS ON TOP DEF
        123
        # TITLE = 'Example' # name of the window
        # Window.set_title(TITLE)
        #
        # # Register top-most
        # register_topmost(Window, TITLE)
        #
        # # Unregister top-most (not necessary, only an example)
        # self.bind(on_stop=lambda *args, w=Window, t=TITLE: unregister_topmost(w, t))


sm = ScreenManager()


class ScreenPlayApp(App):

    def on_stop(self):
        # The Kivy event loop is about to stop, set a stop signal;
        # otherwise the app window will close, but the Python process will
        # keep running until all secondary threads exit.
        global stop_threads
        stop_threads = True
        self.root.stop.set()

    def build(self):
        sm.add_widget(MainMenu())
        sm.add_widget(Settings())
        sm.add_widget(Debugging())
        sm.add_widget(Minimalistic())
        sm.add_widget(Skills())
        sm.add_widget(DailyQuests())
        sm.add_widget(Lifeskills())

        return sm

    def on_start(self, *args):
        # ALWAYS ON TOP DEF
        Thread(target=kill_app, args=()).start()
        # TITLE = 'Example' # name of the window
        # Window.set_title(TITLE)
        #
        # # Register top-most
        # register_topmost(Window, TITLE)
        #
        # # Unregister top-most (not necessary, only an example)
        # self.bind(on_stop=lambda *args, w=Window, t=TITLE: unregister_topmost(w, t))


def kill_app():
    while True:
        if keyboard.is_pressed("del"):
            print("TRYING TO STOP APP")
            os._exit(1)
        time.sleep(1)


if __name__ == '__main__':
    MAINTHREAD = Thread(target=ScreenPlayApp)
    MAINTHREAD.daemon = True
    MAINTHREAD.start()

    # x = Thread(target=get_battery)
    # x.daemon = True
    # x.start()
    # start_app()

    # Example().run()
    app = ScreenPlayApp()
    app.run()
