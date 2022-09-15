from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
import time

stopwatch_start = time.time()
start_time = time.time()


class IncrediblyCrudeClock(Label):
    def update(self, *args):
        # stopwatch_end = time.time()
        # execution_time = stopwatch_end - stopwatch_start
        end_time = time.time()
        time_lapsed = end_time - start_time
        self.text = str(self.time_convert(time_lapsed))
        # self.text = time.asctime()

    def time_convert(self, sec):
        mins = sec // 60
        sec = sec % 60
        hours = mins // 60
        mins = mins % 60
        # print("Time Lapsed = {0}:{1}:{2}".format(int(hours), int(mins), sec))
        return_value = "Time Lapsed = {0}:{1}:{2}".format(int(hours), int(mins), round(sec, 1))
        return return_value


class TimeApp(App):
    def build(self):
        crudeclock = IncrediblyCrudeClock()
        Clock.schedule_interval(crudeclock.update, 0.1)
        return crudeclock


if __name__ == "__main__":
    TimeApp().run()

