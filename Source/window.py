"""Window class contains the coordinate for the top left of the game window."""
import ctypes
import platform
import numpy as np
import itertools
from collections import OrderedDict
import win32gui

from deprecated import deprecated
from typing import Dict, Tuple

win2find = 'LOST ARK (64-bit'
LAhex = '0xe0b80 LOST ARK (64 - bit) v.1.9.0.3'
LAhexonly = '0xe0b80'
LANEW = r"920448, 'LOST ARK (64-bit) v.1.9.0.3'"
LANEWn = '920448'
LANUMP = r"'920448' 'LOST ARK (64-bit) v.1.9.0.3'"

steam = r"'steam'"

class Window:
    """This class contains game window coordinates."""

    id = 0
    x = 0
    y = 0
    dc = 0
    WindowCoordArr = []

    #print("i was in window")

    @deprecated(reason="Window() -Window instantiation- is deprecated, use Window.init() instead")
    def __init__(self, debug=False):
        Window.init(debug)

    @staticmethod
    def init(debug: bool = False) -> Dict[int, Tuple[int, int, int, int]]:
        """Finds the game window and returns its coords."""
        if platform.release() == "10":
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        else:
            ctypes.windll.user32.SetProcessDPIAware()

        def window_enumeration_handler(hwnd, top_windows):
            """Add window title and ID to array."""
            top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
            dict_window[hwnd] = win32gui.GetWindowText(hwnd)

        if debug:
            window_name = "debugg"
        else:
            window_name = steam

        top_windows = []
        dict_window = {}
        windows = []
        candidates = {}
        coordinates = []

        win32gui.EnumWindows(window_enumeration_handler, top_windows)
        windows = []

        # CONVERTS ARRAY TO STRING
        test = [str(i) for i in top_windows]
        # Print dictionary :print(dict_window)
        # x = dict_window[920448] pri
        # Finds dictionary VALUE based on KEY(win2find)


        # FINDS ELEMENT IN STRING ARRAY THAT MATCHES text
        matchstring = ("".join(s for s in test if window_name.lower() in s.lower()))
        d = matchstring.split(",")
        d = d[1]
        #removes first letter(1) and(:) last character(-1)
        window_name = d[1:-1]
        #removes last character in string
        #window_name = d[:-1]

        window_name = window_name.replace("'", "")

        # print("this is new window name")
        # print(window_name)

        for key in dict_window:
            #print(dict_window[key])
            if dict_window[key] == window_name:
            #if any(window_name in s for s in dict_window[key]):
                global id
                id = key  # Dictionary Key
                Window.id = key
                windows.append(id)
                print("key: %s , value: %s" % (key, dict_window[key]))
            # for window in windows:
            #     global WindowCoordArr
            #     WindowCoordArr = Window.winRect(window)


        # print(id)
        # print(window_name)
        # print("this is the test for dictionary")

        # FINDS ELEMENT IN STRING ARRAY THAT MATCHES text
        matchstring = ("".join(s for s in test if LANEW.lower() in s.lower()))

        # window_id = Window.id
        # print("top windows: " + str(top_windows[14]))
        # print("window name : " + window_name)
        # print("windows is : ")
        # print(windows)
        for window in windows:
            global WindowCoordArr
            #print("these are window coordinates")
            #print(Window.winRect(window))
            Window.WindowCoordArr = Window.winRect(window)
            # print(WindowCoordArr[0])
            # print(WindowCoordArr[1])
            # print(WindowCoordArr[2])
            # print(WindowCoordArr[3])
            candidates[window] = Window.winRect(window)
            #print('candidate is :' + str(candidates))
        return candidates

    @staticmethod
    def setPos(x: int, y: int) -> None:
        """Set top left coordinates."""
        Window.x = x
        Window.y = y

    @staticmethod
    def winRect(window_id: int) -> Tuple[int, int, int, int]:
        """Returns the coordinates of the window"""
        return win32gui.GetWindowRect(window_id)

    @staticmethod
    def shake() -> None:
        """Shake that Window"""
        for x in range(1000):
            win32gui.MoveWindow(Window.id, x, 0, 1000, 800, False)
        for y in range(1000):
            win32gui.MoveWindow(Window.id, 1000, y, 1000, 800, False)
        for x in reversed(range(1000)):
            win32gui.MoveWindow(Window.id, x, 1000, 1000, 800, False)
        for y in reversed(range(1000)):
            win32gui.MoveWindow(Window.id, 0, y, 1000, 800, False)

    @staticmethod
    def gameCoords(x1: int, y1: int, x2: int, y2: int) -> Tuple[int, int, int, int]:
        """Converts coords relative to the game to coords relative to the window."""
        return Window.x + x1, Window.y + y1, Window.x + x2, Window.y + y2


