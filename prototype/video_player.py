import threading
import cv2
from PIL import ImageTk, Image
import gui

class Player(threading.Thread):

    def __init__(self):
        super().__init__()
        self.frameTime = 1  # time of each frame in ms, you can add logic to change this value.
        self.frame = None
        self.cap = None

    def accelerate(self, speed):
        cap = cv2.VideoCapture('video.mp4')
        i = 0  # frame counter
        frameTime = 1  # time of each frame in ms, you can add logic to change this value.
        while (cap.isOpened()):
            ret = cap.grab()  # grab frame
            i = i + 1  # increment counter
            if i % 3 == 0:  # display only one third of the frames, you can change this parameter according to your needs
                ret, frame = cap.retrieve()  # decode frame
                cv2.imshow('frame', frame)
                if cv2.waitKey(frameTime) & 0xFF == ord('q'):
                    break
        cap.release()
        cv2.destroyAllWindows()

    def decelerate(self):
        cap = cv2.VideoCapture('video.mp4')
        frameTime = 10  # time of each frame in ms, you can add logic to change this value.
        while (cap.isOpened()):
            ret, frame = cap.read()
            cv2.imshow('frame', frame)
            if cv2.waitKey(frameTime) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()


    def run(self):
        self.cap = cv2.VideoCapture('samplevideo.mp4')
        self.video_stream()
        # while cap.isOpened():
        #     ret, main.videocv = cap.read()
        #     # if frame is read correctly ret is True
        #     if not ret:
        #         print("Can't receive frame (stream end?). Exiting ...")
        #         break
        #     cv2.imshow('frame', main.videocv)
        #     if cv2.waitKey(1) == ord('q'):
        #         break
        # cap.release()
        # cv2.destroyAllWindows()


    def video_stream(self):
        _, frame = self.cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        gui.simulation.imgtk = imgtk
        gui.simulation.configure(image=imgtk)
        gui.simulation.after(1, self.video_stream)