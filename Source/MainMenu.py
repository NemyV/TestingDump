# import kivy module
import kivy

# this restrict the kivy version i.e
# below this kivy version you cannot
# use the app or software
kivy.require("1.9.1")

# base Class of your App inherits from the App class.
# app:always refers to the instance of your application
from kivy.app import App

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from  kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
# class in which we are defining action on click
class MyGUI(FloatLayout):
    pass



# class MyGUI(Label):
#     Label(text=u'Hello world ', font_size='20sp', )

# creating action class and calling
# Rootwidget by returning it
class testkvApp(App):
    def build(self):
        Window.size = (1111, 777)
        #Window.left = (1920-320)
        Window.borderless = True
        Window.add_widget(Label(text='GFG is Good Website foe CSE Students\n' * 5))
        return MyGUI()


    def labelx(self):
        # label display the text on screen
        lbl = Label(text="Label is Added on screen !!:):)")
        return lbl


    # creating the myApp root for ActionApp() class


myApp = testkvApp()

# run function runs the whole program
# i.e run() method which calls the
# target function passed to the constructor.
if __name__ == '__main__':
    testkvApp().run()