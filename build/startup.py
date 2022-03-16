from threading import Thread
from time import sleep
import tkinter as tk
from tkinter import * 
from tkinter.ttk import *
from gui import Gui
from pathlib import *
  
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    """
    Creates a file path that leads to the specified file name in the assets folder.

    Arguments:
        path {str} -- filename in assets

    Returns:
        Path -- the file path for the file in assets
    """
    return ASSETS_PATH / Path(path)

class App(tk.Tk):
    """
    This is the start up screen for the rest of the GUI
    Think of it as a main menu of sorts

    Arguments:
        Tk {tkinter} -- Inherits from tkinter, App is a tkinter window. 
    """
    def __init__(self):
        super().__init__()
        self.sel = 1
        
        # root window
        self.title('CME-STEM Challenge')
        self.resizable(False, False)
        self.geometry('400x400')
        self.style = Style(self)


        # Create Canvas
        canvas1 = Canvas(self, width = 400,height = 449)
        canvas1.pack()
        
        # radio button
        theme_frame = LabelFrame(canvas1, text='Start Options')
        theme_frame.pack(padx=10, pady=10, ipadx=20, ipady=20)

        # for theme_name in ["CME-STEM load from CSV (fast)", "CME load from internet (slow)", "Import custom CSV", "Load custom data"]:
        rb = Radiobutton(
            theme_frame,
            text="CME-STEM load from CSV (fast)",
            command=lambda: self.set_sel(1),
            value=1
            )
        rb.pack(expand=True, fill='both')

        rb = Radiobutton(
            theme_frame,
            text="CME-STEM load from Internet (slow)",
            command=lambda: self.set_sel(2),
            value=2
            )
        rb.pack(expand=True, fill='both')
        
         # button
        btn = Button(master = canvas1, style='Accent.TButton', text='Start', command=self.start_gui)
        btn.pack(padx=10, pady=10)
                  
    def start_gui(self):
        """
        Starts the GUI class, and sets it's theme
        """
        g = Gui(self.get_sel())
        g.tk.call("source", r"build\assets\azure.tcl")
        g.tk.call("set_theme", "light")
        g.mainloop()
    
    def set_sel(self, selection):
        """
        Setter function for self.sel

        Arguments:
            selection {int} -- determines the selection from radio buttons
        """
        self.sel = selection

    def get_sel(self) -> int:
        """
        Getter function for self.sel

        Returns:
            self.sel {int} -- returns self.sel
        """
        return self.sel
    

if __name__ == "__main__":
    app = App()
    app.tk.call("source", r"build\assets\azure.tcl")
    app.tk.call("set_theme", "light")
    app.mainloop()