import threading
import time
from tkinter import *
import cv2
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo
from PIL import ImageTk, Image

import voice_recognition
import video_player

status = ""
cap = cv2.VideoCapture('samplevideo.mp4')

def video_stream():
    # i = 0
    # frameTime = 1
    # _, frame = cap.read()
    # cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    # img = Image.fromarray(cv2image)
    # imgtk = ImageTk.PhotoImage(image=img)
    # simulation_lb.imgtk = imgtk
    # simulation_lb.configure(image=imgtk)
    # simulation_lb.after(1, video_stream)

    # if status == "pause":
    #     cv2.waitKey(0)
    # else:
    #     simulation_lb.after(1, video_stream)

    while cap.isOpened():
        ret, frame = cap.read()  # Reads the video
        # Converting the video for Tkinter
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        # Setting the image on the label
        simulation_lb.config(image=imgtk)
        root.update()  # Updates the Tkinter window

def show_video():
    status = "play"
    video_stream()



def load_video():
    # """ loads the video """
    # file_path = filedialog.askopenfilename()
    #
    # if file_path:
    #     vvideoplayer.load(file_path)
    #
    #     # progress_slider.config(to=0, from_=0)
    #     play_pause_btn["text"] = "Play"
    #     # progress_value.set(0)
    print("LOAD")


def play_pause():
    """ pauses and plays """
    if status == "":
        show_video()
        play_pause_btn.config(image=pause_img)
    if status == "pause":
        play_pause_btn.config(image=start_img)
    if status == "play":
        play_pause_btn.config(image=pause_img)


# stuff to run always here such as class/def
def main():
    pass

if __name__ == "__main__":
    # stuff only to run when not called via 'import' here

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
    start_img = PhotoImage(file=f"img/play.png")
    pause_img = PhotoImage(file=f"img/pause.png")
    play_pause_btn = Button(master=btm_frame, image=start_img, borderwidth=0, highlightthickness=0, relief="flat",
                           command=lambda:threading.Thread(target=play_pause).start())
    slow_img = PhotoImage(file=f"img/slow.png")
    slow_btn = Button(master=btm_frame, image=slow_img, borderwidth=0, relief="flat")
    fast_img = PhotoImage(file=f"img/fast.png")
    fast_btn = Button(master=btm_frame, image=fast_img, borderwidth=0, relief="flat")
    load_img = PhotoImage(file=f"img/load.png")
    load_btn = Button(master=btm_frame, image=load_img, borderwidth=0, highlightthickness=0, relief="flat",
                     command=load_video)
    voice_img = PhotoImage(file=f"img/003-microphone.png")
    voice_btn = Button(btm_frame, image=voice_img, borderwidth=0, highlightthickness=0, relief="flat",
                     command=lambda: voice_recognition.SR().start())

    load_btn.grid(row=0, column=0, sticky=EW)
    slow_btn.grid(row=0, column=1, sticky=EW)
    play_pause_btn.grid(row=0, column=2, sticky=EW)
    # progress_slider.grid(row=0, column=3, sticky=EW)
    fast_btn.grid(row=0, column=4, sticky=EW)
    voice_btn.grid(row=0, column=5, sticky=EW)

    top_frame.grid(row=0, sticky=EW)
    center_frame.grid(row=1, sticky=NSEW)
    btm_frame.grid(row=2, sticky=EW)

    root.mainloop()


    main()
