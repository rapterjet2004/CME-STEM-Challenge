import backtrader as bt
import datetime
import pandas as pd
import numpy as np
from tkinter import * 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import matplotlib.dates
from strategies import *

class Btmain:
    def __init__(self) -> None:
        #Instantiate Cerebro engine
        self.cerebro = bt.Cerebro()

        #Gets data feed from CSV 
        data = bt.feeds.GenericCSVData(
            dataname=r'C:\Users\juliu\PythonProjects\BTC_3.csv',
            fromdate=datetime.datetime(2018, 1, 1),
            todate=datetime.datetime(2022, 1, 1),
            nullvalue=0.0,
            dtformat=('%m/%d/%Y'),
            datetime=0,
            high=3,
            low=4,
            open=2,
            close=2,
            volume=8,
            openinterest=-1,
            timeframe=bt.TimeFrame.Days)

        # data1 = bt.feeds.YahooFinanceCSVData(
        #     dataname=r'C:\Users\juliu\PythonProjects\GME.csv',
        #     fromdate=datetime.datetime(2018, 1, 1),
        #     todate=datetime.datetime(2022, 1, 1),
        # )
        
        #Add CSV data to Cerebro
        self.cerebro.adddata(data)

        #Add strategy to Cerebro
        self.cerebro.addstrategy(FirstStrategy)

        #Add sizer to Cerebro
        self.cerebro.addsizer(bt.sizers.SizerFix, stake=3)

    def get_plot(self):
        """
        Calls the Cerebro engine and returns the Backtrader strategy plot from Cerebro. 

        Returns:
            _Figure_ -- A figure from matplotlib
        """
        self.cerebro.run(runonce=False)
        #pnl = end_portfolio_value - start_portfolio_value
        fig = self.cerebro.plot(iplot=False)

        return fig[0][0]
    
    def get_starting_value(self):
        """
        Returns the starting value of the Cerebro broker. 

        Returns:
            _float_ -- the starting portfolio value 
        """
        start_portfolio_value = self.cerebro.broker.getvalue()
        return start_portfolio_value

    def get_ending_value(self):
        """
        Returns the ending value of the Cerebro broker. 

        Returns:
            _float_ -- the ending portfolio value 
        """
        end_portfolio_value = self.cerebro.broker.getvalue()
        return round(end_portfolio_value, 2)
    
    def get_pnl(self):
        """
        Returns the difference between the starting and ending portfolio values

        Returns:
            _float_ -- the difference between starting and ending portfolio values
        """
        pnl = self.get_ending_value() - self.get_starting_value()
        return pnl


