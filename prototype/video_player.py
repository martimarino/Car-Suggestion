import fnmatch
import os

import vlc
import threading

class Simulation (threading.Thread):

    sea = ["https://www.youtube.com/watch?v=JHAcW9cU0mY",
           "https://www.youtube.com/watch?v=-Tm4H4CrKT0",
           "https://www.youtube.com/watch?v=wFN_QaTw1Bo"]
    mountain = ["https://www.youtube.com/watch?v=eNhPu4Yf4s8",
                "https://www.youtube.com/watch?v=cJpyQ9f1pQU&list=RDCMUCoTedxE3WwpDUGW8P6a3T6Q&index=5",
                "https://www.youtube.com/watch?v=cJHGKSz_CDw&list=RDCMUCoTedxE3WwpDUGW8P6a3T6Q&index=15"]

    def choose_video(self):
        #.......
        return

    def play_pause(self):
        """ pauses and plays """
        if self.status == "pause":
            self.media_player.play()
            self.status = "play"
            return
        if self.status == "play":
            self.media_player.pause()
            self.status = "pause"
            return

    def __init__(self):
        super().__init__()
        self.scent = None
        self.temp = None
        self.scenario = None
        self.color_light = None
        self.status = ""
        self.media_player = None

    def load_video(self, place, temperature, scent):
        self.status = "play"
        for file in os.listdir('sim'):
            if fnmatch.fnmatch(file, place.get() + "_" + temperature.get() + "_" + scent.get() + ".*"):
                self.media_player = vlc.MediaPlayer("./sim/" + file)
            elif fnmatch.fnmatch(file, place.get() + "_" + temperature.get() + "_*" + ".*"):
                self.media_player = vlc.MediaPlayer("./sim/" + file)
            elif fnmatch.fnmatch(file, place.get() + "_*" + "_*" + ".*"):
                self.media_player = vlc.MediaPlayer("./sim/" + file)
            else:
                self.media_player = vlc.MediaPlayer("./sim/prova.mkv")

        self.media_player.play()
        
    def speedup(self):
        self.media_player.set_rate(2)

    def slowdown(self):
        self.media_player.set_rate(0.5)
    def run(self):

        return
