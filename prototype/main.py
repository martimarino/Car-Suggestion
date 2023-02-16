import GUI
import VUI
import queue

if __name__=='__main__':

    BUF_SIZE = 10
    command = queue.Queue(BUF_SIZE)
    gui = GUI.GUI(command)     #consumer
    # # vui = VUI.VUI(command)     #producer
    #
    gui.start()
    # # vui.start()