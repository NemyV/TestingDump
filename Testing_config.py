from kivy.config import ConfigParser
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
import threading

configparser = ConfigParser()
configparser.read("example.ini")

sm = ScreenManager()


class MainMenu(Screen):
    # @mainthread
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        super(MainMenu, self).__init__(name='MainMenu')
        # Window.bind(on_keyboard=self.on_keyboard)  # bind our handler
        # Window.size = (2560, 150)
        # Window.top = 930  # 930
        # Window.left = 0
        self.on_start()


class ScreenPlayApp(App):

    def on_stop(self):
        # The Kivy event loop is about to stop, set a stop signal;
        # otherwise the app window will close, but the Python process will
        # keep running until all secondary threads exit.
        global stop_threads
        stop_threads = True
        self.root.stop.set()

    def build(self):
        123

        return sm

    def on_start(self):
        list_of_workers = [
                            "Gladiatrix",
                            "Ggwarlord",
                            "Ggsor"
                            ]
        for x in list_of_workers:
            for section_name in configparser.sections():
                # option = configparser.options(section_name)
                if x == section_name:
                    for name, value in configparser.items(section_name):
                        # config_name = name
                        # config_value = value
                        # print(name)
                        if value == "yes":
                            print("WORK FOR ", x, " :")
                            if "preset" in name:
                                import re
                                # print([int(s) for s in name.split() if s.isdigit()])
                                found = re.findall(r'\d+', name)
                                print(found)
                                print("doing PRESETS", int(found[0]))
                            if "all_silver" in name:
                                print("ACCEPTING ALL QUESTS")
                                print("doing silver")
                            elif "all_leapstone" in name:
                                print("ACCEPTING ALL QUESTS")
                                print("doing leapstone")
                            if "guild_silver" in name:
                                print("doing GUILD silver")


if __name__ == '__main__':
    app = ScreenPlayApp()
    app.run()
