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
        #Instantiate Cerebro engin
        self.cerebro = bt.Cerebro()

        #Add data feed to Cerebro
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

        data1 = bt.feeds.YahooFinanceCSVData(
            dataname=r'C:\Users\juliu\PythonProjects\GME.csv',
            fromdate=datetime.datetime(2018, 1, 1),
            todate=datetime.datetime(2022, 1, 1),
        )

        self.cerebro.adddata(data)

        #Add strategy to Cerebro
        self.cerebro.addstrategy(PrintClose)

        self.cerebro.addsizer(bt.sizers.SizerFix, stake=3)

    def get_plot(self):
        self.cerebro.run(runonce=False)
        #pnl = end_portfolio_value - start_portfolio_value
        fig = self.cerebro.plot(iplot=False)

        return fig[0][0]
    
    def get_starting_value(self):
        start_portfolio_value = self.cerebro.broker.getvalue()
        return start_portfolio_value

    def get_ending_value(self):
        end_portfolio_value = self.cerebro.broker.getvalue()
        return round(end_portfolio_value, 2)
    
    def get_pnl(self):
        pnl = self.get_ending_value() - self.get_starting_value()
        return pnl


