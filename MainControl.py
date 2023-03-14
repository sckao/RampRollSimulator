# Main Control - Top Level Program Entry Point
# Author: Kevin Kao
# Contact: kaoshihchuan@gmail.com

# import os.path
import tkinter as tk
import TestPanel as TestPanel
import pathlib


def get_base_dir() -> str:
    return str(pathlib.Path(__file__).parent.resolve())
# end get_base_dir


def main():

    # Create UI to run
    rootgui = tk.Tk()
    rootgui.title('Ramp_and_Roll_Simulator')

    init_width = int(rootgui.winfo_screenwidth() * 0.7)
    init_height = int(rootgui.winfo_screenheight() * 0.8)
    init_x = int(rootgui.winfo_screenwidth() / 8)
    init_y = int(rootgui.winfo_screenheight() / 8)
    rootgui.geometry('{}x{}+{}+{}'.format(init_width, init_height, init_x, init_y))
    # Create Content for Main UI: rootgui
    TestPanel.GuiWindow(rootgui)

    rootgui.mainloop()

# end main


if __name__ == '__main__':
    main()
# end if
