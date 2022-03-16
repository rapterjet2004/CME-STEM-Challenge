from ntpath import join
from tkinter import HORIZONTAL, Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, Label
from tkinter.ttk import *
from btmain import Btmain, Ytmain
from pytmain import Pytmain as pyt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from time import sleep
from threading import Thread
from pathlib import Path

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

class Gui(Tk):
    """
    GUI class for displaying the graphs and data. Multiple
    GUI's can be opened from the start menu. 

    Arguments:
        Tk {tkinter} -- GUI is a Tkinter window
    """
    def __init__(self, selection=1):
        super().__init__()
        self.title('CME-STEM Challenge')
        self.geometry("1000x680")
        self.configure(bg = "#373737")
        self.resizable(False, False)

        if selection == 1:
            self.b = Btmain()
        elif selection == 2:
            self.b = Btmain(option=False)
        
        #root canvas for the gui
        main_canvas = Canvas(
            self,
            bg = "#e6e6e6",
            height = 700,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        main_canvas.place(x = 0, y = 0)

        # bitmain layout marker
        main_canvas.create_rectangle(
            15.0,
            13.0,
            985.0,
            412.0,
            fill="#FFFFFF",
            outline="")

        # bitmain canvas
        self.btmain_canvas = Canvas(
            main_canvas,
            bg = "#FFFFFF",
            height = 480,
            width = 970,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.btmain_canvas.place(x=15, y=13)


        # pytrends layout marker
        main_canvas.create_rectangle(
            15.0,
            504.0,
            985.0,
            604.0,
            fill="#FFFFFF",
            outline="")

        # pytrends canvas
        self.pytrends_canvas = Canvas(
            main_canvas,
            bg = "#FFFFFF",
            height = 150,
            width = 970,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.pytrends_canvas.place(x=15, y=430)

        # Bottom text banner
        main_canvas.create_rectangle(
            15.0,
            611.0,
            986.0,
            689.0,
            fill="#abc8e0",
            outline="")

        #Starting portfolio value label
        main_canvas.create_text(
            22.0,
            611.0,
            anchor="nw",
            text="Starting portfolio value:",
            fill="#000000",
            font=("Roboto", 24 * -1)
        )

        #Ending portfolio value label
        main_canvas.create_text(
            22.0,
            651.0,
            anchor="nw",
            text="Ending portfolio value:",
            fill="#000000",
            font=("Roboto", 24 * -1)
        )

        #Starting portfolio value, called after btmain is initialized but before cerebro is run
        main_canvas.create_text(
            292.0,
            611.0,
            anchor="nw",
            text=self.b.get_starting_value(),
            fill="#000000",
            font=("Roboto", 24 * -1)
        )


        # Calls the graphing functions
        # Pytrends has to be called first otherwise it doesn't plot for some reason
        self.plot_pytrends()
        self.plot_btmain()

        # Ending portfolio value, called after cerebro is run else returns starting value
        main_canvas.create_text(
            292.0,
            651.0,
            anchor="nw",
            text=self.b.get_ending_value(),
            fill="#000000",
            font=("Roboto", 24 * -1)
        )
        


    def plot_btmain(self):
        """
        Embeds the Backtrader plot from btmain into the tKinter window. Master canvas
        is btmain_canvas. Size and dpi are specific for formatting.  
        
        """
        fig = self.b.get_plot()
        fig.set_size_inches(13, 5)
        fig.set_dpi(74.5)
        graph = FigureCanvasTkAgg(fig, master = self.btmain_canvas) 
        graph.draw()
        graph.get_tk_widget().pack()


    def plot_pytrends(self):
        """
        Embeds the pytrends plot from pyt into the tKinter window. Master canvas
        is pytrends_canvas. Size and dpi are specific for formatting. 

        """

        p = pyt()
        
        data = p.get_data("bitcoin")
        
        y = data["bitcoin"].values
        
        # TODO: add actual dates instead of 0-whatever
        x = data.index
            
        fig = Figure()
        fig.set_size_inches(13, 2)
        fig.set_dpi(74.6)
        fig.add_subplot(111, title=f"Bitcoin: Interest Over Time").plot(x, y)
            
        canvas = FigureCanvasTkAgg(fig, master=self.pytrends_canvas)
        canvas.draw()
        canvas.get_tk_widget().pack()



