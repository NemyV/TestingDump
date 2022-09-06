import pydirectinput
import time
import win32gui
import re

def focus_window(NameofWindow):
    print("FOCUS SWITCH to ", NameofWindow)
    w = WindowMgr()
    w.find_window_wildcard(NameofWindow)
    w.set_foreground()


class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)


pydirectinput.click(799,
                    191, button="right")
focus_window('LOST ARK')
time.sleep(2)
pydirectinput.click(633,
                    685, button="right")
focus_window('LOST ARK')
time.sleep(1.2)
pydirectinput.click(1200,
                    878, button="right")
focus_window('LOST ARK')
time.sleep(1.2)
pydirectinput.click(1239,
                    878, button="right")
focus_window('LOST ARK')
time.sleep(1.1)
pydirectinput.click(1227,
                    909, button="right")
focus_window('LOST ARK')
time.sleep(1.1)
pydirectinput.click(972,
                    934, button="right")
focus_window('LOST ARK')
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
