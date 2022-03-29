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
        self.resizable(False, True)
        #self.geometry('400x500')
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
        btn = Button(master = theme_frame, style='Accent.TButton', text='Start', command=self.start_gui)
        btn.pack(padx=10, pady=10)
        
        self.theme_frame1 = LabelFrame(canvas1, text='Enter Bounds')

        srt_ylbl = Label(self.theme_frame1, text="Start Year:")
        srt_ylbl.pack()

        self.srt_year = Entry(self.theme_frame1)
        self.srt_year.insert(0, "2021")
        self.srt_year.pack()

        srt_mlbl = Label(self.theme_frame1, text="Start Month:")
        srt_mlbl.pack()

        self.srt_month = Entry(self.theme_frame1)
        self.srt_month.insert(0, "7")
        self.srt_month.pack()

        end_ylbl = Label(self.theme_frame1, text="End Year:")
        end_ylbl.pack()

        self.end_year = Entry(self.theme_frame1)
        self.end_year.insert(0, "2022")
        self.end_year.pack()

        end_mlbl = Label(self.theme_frame1, text="End Month:")
        end_mlbl.pack()

        self.end_month = Entry(self.theme_frame1)
        self.end_month.insert(0, "1")
        self.end_month.pack()

        self.theme_frame1.pack_forget()

        self.error_ylbl = tk.Label(canvas1, text="Invalid Input", fg="#a8384a")
        self.error_ylbl.pack_forget()


        
                  
    def start_gui(self):
        """
        Starts the GUI class, and sets it's theme
        """
        if not self.checkinputs():
            if self.sel == 1:
                g = Gui(self.sel)
            elif self.sel == 2:
                g = Gui(self.sel, 
                        srt_year=int(self.srt_year.get()),
                        srt_month=int(self.srt_month.get()),
                        end_year=int(self.end_year.get()),
                        end_month=int(self.end_month.get())
                        )
            g.tk.call("source", r"build\assets\azure.tcl")
            g.tk.call("set_theme", "light")
            g.mainloop()
        else:
            self.show_error()
    
    def set_sel(self, selection):
        """
        Setter function for self.sel

        Arguments:
            selection {int} -- determines the selection from radio buttons
        """

        if selection == 1:
            self.hide_options()
        else:
            self.show_options()
        self.sel = selection
    
    def show_options(self):
        self.theme_frame1.pack(padx=10, pady=10, ipadx=75, ipady=20)

    def hide_options(self):
        self.theme_frame1.pack_forget()
    
    def show_error(self):
        self.error_ylbl.pack()
    
    def checkinputs(self):
        """
        Checks the inputs if they are valid or not. If the inputed
        years are of the correct 4 digit format, and the inputed months 
        of the correct 1 digit format and are less than or equal to 12.
        Also checks the inputed values to see that they are not 0, and that 
        they fall within the time interval of the data given.

        Returns:
            _boolean_ -- True if input is invalid, false is passing
        """
        if not self.srt_year.get().isalpha() and not self.srt_month.get().isalpha() and not self.end_month.get().isalpha() and not self.end_year.get().isalpha():
            start_y=int(self.srt_year.get())
            start_m=int(self.srt_month.get())
            end_y=int(self.end_year.get())
            end_m=int(self.end_month.get())


            if start_y == 0 or end_y == 0 or start_m == 0 or end_m == 0:
                return True
            
            if not(len(self.srt_year.get()) == 4) or not(len(self.end_year.get()) > 4):
                if start_y > 2022 or end_y < 2017:
                    return True
            
            if not(len(self.srt_month.get()) == 1) or not(len(self.end_month.get()) == 1):
                if start_m > 12 or end_m > 12 or (start_y == 2017 and start_m <2) or (end_y == 2022 and end_m > 1):
                    return True
        else:
            return True

        return False
    

if __name__ == "__main__":
    app = App()
    app.tk.call("source", r"build\assets\azure.tcl")
    app.tk.call("set_theme", "light")
    app.mainloop()
