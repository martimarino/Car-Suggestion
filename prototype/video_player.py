import threading
import cv2
import numpy as np
from PIL import ImageTk, Image

class Player(threading.Thread):

    def __init__(self, path):
        super().__init__()
        self.cap = cv2.VideoCapture(path)


    # def accelerate(self, speed):
    #     i = 0  # frame counter
    #     frameTime = 1  # time of each frame in ms, you can add logic to change this value.
    #     while (cap.isOpened()):
    #         ret = cap.grab()  # grab frame
    #         i = i + 1  # increment counter
    #         if i % 3 == 0:  # display only one third of the frames, you can change this parameter according to your needs
    #             ret, frame = cap.retrieve()  # decode frame
    #             cv2.imshow('frame', frame)
    #             if cv2.waitKey(frameTime) & 0xFF == ord('q'):
    #                 break
    #     cap.release()
    #     cv2.destroyAllWindows()
    #
    # def decelerate(self):



    def run(self):

        # Check if camera opened successfully
        if (self.cap.isOpened() == False):
            print("Error opening video file")

        # Read until video is completed
        while (self.cap.isOpened()):

            # Capture frame-by-frame
            ret, frame = self.cap.read()
            if ret == True:
                # Display the resulting frame
                cv2.imshow('Frame', frame)

                # Press Q on keyboard to exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

            # Break the loop
            else:
                break

        # When everything done, release
        # the video capture object
        self.cap.release()

        # Closes all the frames
        cv2.destroyAllWindows()