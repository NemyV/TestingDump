from kivy.config import ConfigParser
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
import threading
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.button import Button

configparser = ConfigParser()
configparser.read("example.ini")

sm = ScreenManager()
LoAImages = 'C:\\Users\\Ggjustice\\Pictures\\Buttons\\'
Resolution = [2560, 1080]


class MainMenu(Screen):
    # @mainthread
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        super(MainMenu, self).__init__(name='MainMenu')
        # Window.bind(on_keyboard=self.on_keyboard)  # bind our handler
        Window.size = (Resolution[0] / 1.2, Resolution[1] / 1.2)
        Window.left = Resolution[0] / 10.5
        Window.top = Resolution[1] / 9

        # Main Buttons
        SizeH = 0.5
        SizeW = 0.33
        # Base
        base_label_x = -.44
        base_image_x = -.24
        grid_checkbox_x = 0.07
        grid_label_x = -.26
        # GIGA GRID
        self.GIGA_GRID = GridLayout(pos_hint={'x': 0, 'y': .00}, cols=2, rows=2,
                                    row_force_default=True, row_default_height=60, col_default_width=60)
        self.add_widget(self.GIGA_GRID)

        self.GIGA_GRID.layout = GridLayout(pos_hint={'x': 0.0, 'y': -0.2}, cols=1,
                                           row_force_default=True, row_default_height=60, col_default_width=60)

        # self.GIGA_GRID.add_widget(self.GIGA_GRID.layout)

        self.GIGA_GRID.add_widget(Button(text='Hello 1'))
        self.GIGA_GRID.add_widget(Button(text='World 1'))

        self.GIGA_GRID.layout.add_widget(Button(text='Hello 2'))
        self.GIGA_GRID.layout.add_widget(Button(text='World 2'))

        # SMALL GRID 1
        self.leapstone_checkbox = GridLayout(pos_hint={'x': grid_checkbox_x, 'y': 0.93}, cols=1,
                                             row_force_default=True, row_default_height=60, col_default_width=60)
        self.GIGA_GRID.add_widget(self.leapstone_checkbox)

        # Label
        self.lbl_leapstone = Label(text='Leapstone dailies:',
                                   pos_hint={'x': base_label_x, 'y': +0.45})
        self.add_widget(self.lbl_leapstone)

        self.pirate_coins = Image(source=LoAImages + 'Greater Honor leapstone.png',
                                  size_hint=(0.5, 0.5), pos_hint={'x': base_image_x, 'y': +0.70})
        self.add_widget(self.pirate_coins)

        # # GRID LAYOUT [ LEAPSTONES ]
        # self.leapstone_checkbox = GridLayout(pos_hint={'x': grid_checkbox_x, 'y': 0.93}, cols=1, size_hint=(0.01, 0.01),
        #                                      row_force_default=True, row_default_height=60, col_default_width=60)
        # self.add_widget(self.leapstone_checkbox)  # <<<<<<<<<<<<<<<<<

        # Checkbox
        self.leapstone_checkbox.ALL = CheckBox(ids=({'name': 'all_leapstone'}))
        self.leapstone_checkbox.add_widget(self.leapstone_checkbox.ALL)
        self.leapstone_checkbox.Hypno = CheckBox(ids=({'name': 'hypno'}))
        self.leapstone_checkbox.add_widget(self.leapstone_checkbox.Hypno)
        self.leapstone_checkbox.Nameless_valley = CheckBox(ids=({'name': 'nameless_valley'}))
        self.leapstone_checkbox.add_widget(self.leapstone_checkbox.Nameless_valley)
        self.leapstone_checkbox.Swamp = CheckBox(ids=({'name': 'swamp'}))
        self.leapstone_checkbox.add_widget(self.leapstone_checkbox.Swamp)

        # Labels
        self.GIGA_GRID.layout_label = GridLayout(pos_hint={'x': 0, 'y': .00}, cols=2, rows=5,)
        self.GIGA_GRID.add_widget(self.GIGA_GRID.layout_label)  # <<<<<<<<<<<<<<<<<

        self.GIGA_GRID.layout_label.ALL = Label(text='Accept ALL favorites')
        self.GIGA_GRID.layout_label.add_widget(self.GIGA_GRID.layout_label.ALL)
        self.GIGA_GRID.layout_label.Hypno = Label(text='Hypno')
        self.GIGA_GRID.layout_label.add_widget(self.GIGA_GRID.layout_label.Hypno)
        self.GIGA_GRID.layout_label.Nameless_valley = Label(text='Nameless Valley')
        self.GIGA_GRID.layout_label.add_widget(self.GIGA_GRID.layout_label.Nameless_valley)
        self.GIGA_GRID.layout_label.Swamp = Label(text='Wailling swamp')
        self.GIGA_GRID.layout_label.add_widget(self.GIGA_GRID.layout_label.Swamp)


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

        return sm

    def on_start(self):
        123



if __name__ == '__main__':

    app = ScreenPlayApp()
    app.run()
