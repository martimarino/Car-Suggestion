import vlc
import threading
from tkinter import *

import voice_recognition

class GUI(threading.Thread):
    def __init__(self):
        super().__init__()
        self.status = ""
        self.play_pause_btn = None
        self.media_player = None
        self.start_img = None
        self.pause_img = None

    def speedup(self):
        self.media_player.set_rate(2)

    def slowdown(self):
        self.media_player.set_rate(0.5)

    def load_video(self, video):
        self.status = "play"
        print("LOAD " + self.status)#
        self.media_player = vlc.MediaPlayer(video)
        self.media_player.play()
        self.play_pause_btn.config(image=self.pause_img)

    def play_pause(self):
        """ pauses and plays """
        if self.status == "pause":
            print("IF PAUSE ")
            self.media_player.play()
            self.status = "play"
            print("SET play")
            self.play_pause_btn.config(image=self.pause_img)
            return
        if self.status == "play":
            print("IF PLAY ")
            self.media_player.pause()
            self.status = "pause"
            print("SET pause")
            self.play_pause_btn.config(image=self.start_img)
            return

    def run(self):

        # Configure root params
        root = Tk()
        root.title("Car Suggestion")
        root.geometry('900x700+300+50')
        # root.resizable(False, False)
        root.iconbitmap('img/logo.ico')

        # Configure root rows and columns
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=2)
        root.rowconfigure(2, weight=1)
        root.columnconfigure(0, weight=1)

        top_frame = Frame(root, padx=7, bg='green')
        center_frame = Frame(root, padx=7, bg='yellow')
        btm_frame = Frame(root, padx=7, bg='red')

        # top_frame
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=1)
        root.columnconfigure(3, weight=1)
        root.columnconfigure(4, weight=1)
        root.columnconfigure(5, weight=1)

        speed_lb = Label(top_frame, text='Actual Speed: ', padx=20,
                         font=('Helvetica', 16), justify='left')
        speed = Label(top_frame, text='              ', padx=20,
                      font=('Helvetica', 16), justify='left')
        scents_lb = Label(top_frame, text='Scent: ', padx=20,
                          font=('Helvetica', 16), justify='left')
        scent = Label(top_frame, text='               ', padx=20,
                      font=('Helvetica', 16), justify='left')
        music_lb = Label(top_frame, text="Playing: ", padx=20,
                         font=('Helvetica', 16), justify='left')
        song = Label(top_frame, text='               ', padx=20,
                     font=('Helvetica', 16), justify='left')

        speed_lb.grid(row=0, column=0)
        speed.grid(row=0, column=1)
        scents_lb.grid(row=0, column=2)
        scent.grid(row=0, column=3)
        music_lb.grid(row=0, column=4)
        song.grid(row=0, column=5)

        # center_frame
        center_frame.rowconfigure(0, weight=1)
        center_frame.columnconfigure(0, weight=3)
        center_frame.columnconfigure(1, weight=1)

        simulation_lb = Label(center_frame, background='cyan')
        simulation_lb.grid(row=0, column=0, columnspan=5, sticky=NSEW)

        # vvideoplayer = TkinterVideo(master=center_frame, keep_aspect=True)
        # vvideoplayer.load(r"sim/sea1.mp4")
        # videoplayer.play()
        str = Label(center_frame, text='......', padx=20,
                    font=('Helvetica', 16), justify='left')

        # vvideoplayer.grid(row=0, column=0, columnspan=5, sticky=NSEW)
        str.grid(row=0, column=9)

        # Configure btm_frame  rows and columns
        self.start_img = PhotoImage(file=f"img/play.png")
        self.pause_img = PhotoImage(file=f"img/pause.png")
        self.play_pause_btn = Button(master=btm_frame, image=self.start_img, borderwidth=0, highlightthickness=0,
                                     relief="flat",
                                     command=lambda: threading.Thread(target=self.play_pause).start())
        slow_img = PhotoImage(file=f"img/slow.png")
        slow_btn = Button(master=btm_frame, image=slow_img, borderwidth=0, relief="flat",
                          command=self.slowdown)
        fast_img = PhotoImage(file=f"img/fast.png")
        fast_btn = Button(master=btm_frame, image=fast_img, borderwidth=0, relief="flat",
                          command=self.speedup)
        load_img = PhotoImage(file=f"img/load.png")
        load_btn = Button(master=btm_frame, image=load_img, borderwidth=0, highlightthickness=0, relief="flat",
                          command=lambda: self.load_video("sim/prova.mkv"))
        voice_img = PhotoImage(file=f"img/003-microphone.png")
        voice_btn = Button(btm_frame, image=voice_img, borderwidth=0, highlightthickness=0, relief="flat",
                           command=lambda: voice_recognition.SR().start())

        load_btn.grid(row=0, column=0, sticky=EW)
        slow_btn.grid(row=0, column=1, sticky=EW)
        self.play_pause_btn.grid(row=0, column=2, sticky=EW)
        # progress_slider.grid(row=0, column=3, sticky=EW)
        fast_btn.grid(row=0, column=4, sticky=EW)
        voice_btn.grid(row=0, column=5, sticky=EW)

        top_frame.grid(row=0, sticky=EW)
        center_frame.grid(row=1, sticky=NSEW)
        btm_frame.grid(row=2, sticky=EW)

        root.mainloop()


def main():  # stuff to run always here such as class/def
    pass


if __name__ == "__main__":  # stuff only to run when not called via 'import' here
    gui = GUI().start()
    main()
