import physics
import communicate
import movement
import maze_logic
import box_logic
import path_logic

import cv2
import time
import common

from Tkinter import Tk
from Tkinter import Frame
from Tkinter import BOTH
from Tkinter import Button


class TestingGUI(Frame):
    def __init__(self, parent):
        self.width = 720
        self.height = 480

        Frame.__init__(self, master=parent, background='white')

        self.parent = parent

        self.init_ui()

    def init_ui(self):
        self.parent.title('Testing Framework')
        self.pack(fill=BOTH, expand=1)
        self.center_window()

        quit_button = Button(self, text='Quit', command=self.quit())
        quit_button.place(x=50, y=50)

    def center_window(self):
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()

        x = (screen_width - self.width) / 2
        y = (screen_height - self.height) / 2
        self.parent.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))

if __name__ == '__main__':
    root = Tk()
    app = TestingGUI(root)
    root.mainloop()

    comm = communicate.Port()                                   # Raspberry pi - Arduino serial communication interface
    # robot = physics.Robot(comm, '192.168.1.4:8080')             # Define current robot state
    robot = physics.Robot(comm)                                 # Define current robot state
    path_queue = movement.PathQueue(robot.get_frame_height())   # Expected path offset values
    pid = movement.PID(robot, path_queue)                       # Adjust course through pid
    control = movement.Control(robot, comm)                     # Robot movement controls

    maze = maze_logic.Maze(robot)                               # Maze logic
    box = box_logic.Box(robot)                                  # Box logic
    path = path_logic.Path(robot, path_queue, box)              # Path logic

    while True:
        robot.see('red_arrow.png')
        start = time.time()

        path.create_path()
        path.path_queue.draw_path(robot.get_frame_width(), robot.get_frame_height())

        end = time.time()
        diff = end - start
        if diff == 0:
            diff = 0.0000001

        fps = 1.0 / diff

        common.draw_machine_details(robot.processed_frame, fps)
        common.draw_crosshair(robot.processed_frame)

        cv2.imshow('Feed', robot.current_frame)
        cv2.imshow('Processed feed', robot.processed_frame)
        cv2.imshow('Threshold image', path.threshold_img)

        if cv2.waitKey(1) % 256 == 27:
            break

robot.cam.release()
cv2.destroyAllWindows()
exit(0)
