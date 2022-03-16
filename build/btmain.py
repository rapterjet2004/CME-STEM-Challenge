from ast import Param
from pathlib import Path
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
import yfinance as yf
from yahoofinancials import YahooFinancials
from pytrends import dailydata


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

class Btmain:
    """
    Backtrader class, gathers data from built in CSV files by default
    but can be configured to gather pytrends data from different time 
    ranges as well. 
    """
    

    def __init__(self, option=True) -> None:
        #Instantiate Cerebro engine
        self.cerebro = bt.Cerebro()

        #Gets data feed from CSV 
        btc_data = bt.feeds.GenericCSVData(
            dataname=relative_to_assets('bitcoin_usd_data.csv'),
            fromdate=datetime.datetime(2017, 2, 1),
            todate=datetime.datetime(2022, 1, 1),
            nullvalue=0.0,
            dtformat=('%m/%d/%Y'),
            datetime=0,
            high=3,
            low=4,
            open=2,
            close=1,
            volume=5,
            openinterest=-1,
            timeframe=bt.TimeFrame.Days)


        if option:
            # faster approach but not scalable for other inputs
            pytrends_data = bt.feeds.GenericCSVData(
                dataname=relative_to_assets('google_trends_data.csv'),
                fromdate=datetime.datetime(2017, 2, 1),
                todate=datetime.datetime(2022, 1, 1),
                nullvalue=0.0,
                dtformat=('%Y-%m-%d'),
                datetime=0,
                high=-1,
                low=-1,
                open=-1,
                close=5,
                volume=-1,
                openinterest=-1,
                timeframe=bt.TimeFrame.Days)
        else:
            # Slower approach but scalable for other inputs
            df = dailydata.get_daily_data('bitcoin', 2021, 7, 2022, 1)
            pytrends_data = bt.feeds.PandasData(dataname=df,
                                                open=None, 
                                                high=None, 
                                                low=None,  
                                                close=4, 
                                                volume=None, 
                                                openinterest=None)
        

        #Disables plotting from showing up for this CSV
        pytrends_data.plotinfo.plot = False
        
        #Add bitcoin CSV data to Cerebro
        self.cerebro.adddata(btc_data)

        #Add pytrends CSV data to Cerebro
        self.cerebro.adddata(pytrends_data)

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

class Ytmain:
    """
    Backtrader class, gathers data online from Yahoo finance and pytrends.
    Scalable to other inputs, but slower.
    """
    def __init__(self) -> None:
        #Instantiate Cerebro engine
        self.cerebro = bt.Cerebro()

        #download CSV, added to assets (I should probably do this is another function)
        #on an unrelated note I should probably try to add the custom dependencies added to the github manifest file
        
        #Gets data feed from CSV , potential error later on for invalid names
        btc_data = bt.feeds.PandasData(dataname=self.get_yahoo_financials("BTC"))

        #Gets datafeed from CSV
            
        df = dailydata.get_daily_data('bitcoin', 2017, 2, 2022, 1)
        pytrends_data = bt.feeds.PandasData(dataname=df,
                                            open=None, 
                                            high=None, 
                                            low=None,  
                                            close=4, 
                                            volume=None, 
                                            openinterest=None)

        # pytrends_data = bt.feeds.GenericCSVData(
        #     dataname=relative_to_assets('google_trends_data.csv'),
        #     fromdate=datetime.datetime(2017, 2, 1),
        #     todate=datetime.datetime(2022, 1, 1),
        #     nullvalue=0.0,
        #     dtformat=('%Y-%m-%d'),
        #     datetime=0,
        #     high=-1,
        #     low=-1,
        #     open=-1,
        #     close=5,
        #     volume=-1,
        #     openinterest=-1,
        #     timeframe=bt.TimeFrame.Days)

        #Disables plotting from showing up for this CSV
        pytrends_data.plotinfo.plot = False
        
        #Add bitcoin CSV data to Cerebro
        self.cerebro.adddata(btc_data)

        #Add pytrends CSV data to Cerebro
        self.cerebro.adddata(pytrends_data)

        #Add strategy to Cerebro
        self.cerebro.addstrategy(FirstStrategy)

        #Add sizer to Cerebro
        self.cerebro.addsizer(bt.sizers.SizerFix, stake=3)
    
    def get_yahoo_financials(self, txt: str) -> pd.DataFrame:
        """
        _summary_

        Arguments:
            txt {str} -- The name of the yahoo finance data you want to gather

        Returns:
            pd.DataFrame -- Pandas DataFrame containing yahoo finance data
        """
        df = yf.download(txt, 
                        start='2017-02-01', 
                        end='2022-01-31', 
                        )
        return df
    
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
