from Tkinter import Tk, Frame, BOTH

width = 720
height = 480


class TestingGUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, master=parent, background='white')

        self.parent = parent

        self.init_ui()

    def init_ui(self):
        self.parent.title('Testing Framework')
        self.pack(fill=BOTH, expand=1)
        self.center_window()

    def center_window(self):
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()

        x = (screen_width - width) / 2
        y = (screen_height - height) / 2
        self.parent.geometry('%dx%d+%d+%d' % (width, height, x, y))

if __name__ == '__main__':
    root = Tk()
    app = TestingGUI(root)
    root.mainloop()