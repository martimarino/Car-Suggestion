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
        self.media_player = vlc.MediaPlayer(video)
        self.media_player.play()
        self.play_pause_btn.config(image=self.pause_img)

    def play_pause(self):
        """ pauses and plays """
        if self.status == "pause":
            self.media_player.play()
            self.status = "play"
            self.play_pause_btn.config(image=self.pause_img)
            return
        if self.status == "play":
            self.media_player.pause()
            self.status = "pause"
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
        center_frame.rowconfigure(1, weight=1)
        center_frame.rowconfigure(2, weight=1)
        center_frame.rowconfigure(3, weight=1)
        center_frame.rowconfigure(4, weight=1)
        center_frame.rowconfigure(5, weight=1)

        radioSimulationValue = StringVar(value="Sea")

        Label(center_frame, text="Type of simulation").grid(row=0, column=5)
        Radiobutton(center_frame, text='Sea', value='sea', variable=radioSimulationValue).grid(row=1, column=5)
        Radiobutton(center_frame, text='Mountain', value='mountain', variable=radioSimulationValue).grid(row=2, column=5)
        Radiobutton(center_frame, text='City', value='city', variable=radioSimulationValue).grid(row=3, column=5)
        Radiobutton(center_frame, text='Highway', value='highway', variable=radioSimulationValue).grid(row=4, column=5)
        Radiobutton(center_frame, text='Forest', value='forest', variable=radioSimulationValue).grid(row=5, column=5)

        radioTemperatureValue = StringVar(value="Medium")
        labelTemp = Label(center_frame, text="Temperature").grid(row=0, column=6)
        rt1 = Radiobutton(center_frame, text='Low', value='low', variable=radioTemperatureValue).grid(row=1, column=6)
        rt2 = Radiobutton(center_frame, text='Medium', value='medium', variable=radioTemperatureValue).grid(row=2, column=6)
        rt3 = Radiobutton(center_frame, text='High', value='high', variable=radioTemperatureValue).grid(row=3, column=6)

        radioScentValue = StringVar(value="Peaches")
        labelSim = Label(center_frame, text="Scent").grid(row=0, column=7)
        rsc1 = Radiobutton(center_frame, text='Peaches', value='peaches', variable=radioScentValue).grid(row=1, column=7)
        rsc2 = Radiobutton(center_frame, text='Lavender ', value='lavender', variable=radioScentValue).grid(row=2,column=7)
        rsc3 = Radiobutton(center_frame, text='Cloves ', value='cloves', variable=radioScentValue).grid(row=3, column=7)
        rsc4 = Radiobutton(center_frame, text='Mushrooms', value='mushrooms', variable=radioScentValue).grid(row=4, column=7)

        buttonConfirm = Button(
            center_frame,
            text="Confirm selection",
            command=lambda: self.video.load_video(radioSimulationValue, radioTemperatureValue, radioScentValue))
        buttonConfirm.grid(row=6, column=6)

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
