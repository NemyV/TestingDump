import sys

sys.path.insert(0, 'E:\Hello wolrd Python\LOSTARKB')

import threading
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from KivyOnTop import register_topmost, unregister_topmost
from kivy.clock import Clock
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput

from kivy.uix.dropdown import DropDown
from threading import Thread
# IMPORTS FROM LOOKFOR
from Source.STARTlookfor import startlookfor

GlobalLabel = '123'
GlobalLabel2 = 'GlobalLabel2'
PirateCoins = 20200
CoinOfCourage = 42760
Bloodstones = 11000
CurrentCoins = 0
NumberofChar = 0
PirateGold = 0
sm = ScreenManager()
LoAImages = 'C:\\Users\\AdminN\\Pictures\\Buttons\\'

energy = 100
hours = 4

core_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
core_num = 8

battery_state = "Charging"
battery_capacity = "100"

stop_threads = False


def callbackTo2(instance):
    Window.size = (2560, 150)
    Window.top = 930  # 930
    Window.left = 0
    sm.current = "MainMenu"

    # MainMenu = Thread(target=sm)
    # MainMenu.daemon = True
    # MainMenu.start()


def callbackTo1(instance):
    Window.size = (2560, 250 * 2)
    Window.top = 355
    Window.left = 0
    sm.current = "Settings"
    # Settings = Thread(target=sm)
    # Settings.daemon = True
    # Settings.start()


def startxxx(instance):
    startla = Thread(target=startlookfor)
    startla.daemon = True
    startla.start()


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
        Window.size = (2560, 500)
        Window.top = 580  # 930
        Window.left = 0
        Window.borderless = 0
        Window.borderless = True

        # Main Buttons
        ButtonY = 0.5
        SizeH = 0.2
        SizeW = 0.1
        PosX = .65
        # Checkbox
        checkH = 0.01
        CheckW = 0.01
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

        ##GRID LAYOUT
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







        self.on_start()

        self.food_button = Button(background_normal=LoAImages + 'Yellow.jpg',
                                  border=(0, 0, 0, 0),
                                  text="Main Menu", size_hint=(SizeW, SizeH / 2), pos_hint={'x': .0, 'y': 0.1}
                                  , on_press=callbackTo2)
        self.add_widget(self.food_button)

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
            PirateGold = PirateGold +5000
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
    #

    def on_start(self, *args):
        # ALWAYS ON TOP DEF
        TITLE = 'ScreenPlay'  # name of the window
        Window.set_title(TITLE)

        # Register top-most
        register_topmost(Window, TITLE)
        # Unregister top-most (not necessary, only an example)
        self.bind(on_stop=lambda *args, w=Window, t=TITLE: unregister_topmost(w, t))

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

    # def update(self, *args):
    #     from LostARKFOCUS import GlobalLabel
    #     self.craft_button.text = str(GlobalLabel)
    #     self.lbl_stat.text = str(GlobalLabel2)
    #     #print("this is global labe", GlobalLabel, "test")


class Settings(Screen):
    # @mainthread
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        super(Settings, self).__init__(name='Settings')

        # Main Buttons
        ButtonY = 0.5
        SizeH = 0.2
        SizeW = 0.1
        PosX = .65
        # Checkbox
        checkH = 0.1
        CheckW = 0.1


########


class Grids(GridLayout):
    def __init__(self):
        GridLayout.__init__(self, cols=2, rows=2)
        self.add_widget(MainMenu())
        self.add_widget(Settings())
        self.on_start()

    def on_start(self, *args):
        # ALWAYS ON TOP DEF

        TITLE = 'Example'  # name of the window
        Window.set_title(TITLE)

        # Register top-most
        register_topmost(Window, TITLE)

        # Unregister top-most (not necessary, only an example)
        self.bind(on_stop=lambda *args, w=Window, t=TITLE: unregister_topmost(w, t))


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

        return sm

    # def on_start(self):
    #     self.root.ids.main_tabs.add_widget(BatteryTab())
    #     self.root.ids.main_tabs.add_widget(CPUTab())


if __name__ == '__main__':
    MAINTHREAD = Thread(target=ScreenPlayApp)
    MAINTHREAD.daemon = True
    MAINTHREAD.start()

    # x = Thread(target=get_battery)
    # x.daemon = True
    # x.start()

    # Example().run()
    app = ScreenPlayApp()
    app.run(
    )
