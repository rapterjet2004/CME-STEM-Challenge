import backtrader as bt
import datetime
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from indicators import *

class FirstStrategy(bt.Strategy): 

    def log(self, txt, dt=None):
        """
        Logs the given text to the console, along with the current date.
        Example: 
        input
        >>> log(f'SELL CREATE {self.dataclose[0]:2f}')

        output
        >>> 2021-05-07 SELL CREATE 6146.00

        Arguments:
            txt {_str_} -- The text that is printed to the console

        Keyword Arguments:
            dt {_datetime_} -- The current datetime of the log  (default: {None})
        """
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}') # Comment this line when running optimization

    def __init__(self):
        """
        Instantiates the indicators used in the strategy, along with the order variable and the 
        date time array.

        """
        self.dataclose = self.datas[0].close
        
		# Order variable will contain ongoing order details/status
        self.order = None

        # Trends Volatility Indicator initalization, uses second data feed
        self.tbbi = TBBI(self.datas[1])

    def next(self):
        """
        For every bar in the csv, runs the moving average strategy and creates a buy, sell, or close order
        when needed. If 50 day moving average is above 200 day moving average, buy order is created. If opposite
        then sell order is created. 

        """
        # Check for open orders
        if self.order:
            return
        if not self.position:
		# We are not in the market, look for a signal to OPEN trades
            # dummy initialization for testing, doesn't actually do anything except log if volatile or not
            self.log(f'Volatile?: {self.tbbi[0]}')
            
            # If the Trends Volatility Indicator returns a positive, orders a buy order
            if self.tbbi[0] == 1:
                self.log(f'BUY CREATE {self.dataclose[0]:2f}')
                self.order = self.buy()
            # if returns -1 order a sell order
            elif self.tbbi[0] == -1:
                self.log(f'SELL CREATE {self.dataclose[0]:2f}')
                self.order = self.sell()
        else:
            # We are already in the market, look for a signal to CLOSE trades
            if len(self) >= (self.bar_executed + 10):
                self.log(f'CLOSE CREATE {self.dataclose[0]:2f}')
                self.order = self.close()
            
    def notify_order(self, order):
        """
        Checks if an order is completed, before logging it to the console. Can 
        reject the order if the money is not enough. Resets order the end.

        Arguments:
            order {Order} -- current buy/sell/close order 
        """
        if order.status in [order.Submitted, order.Accepted]:
            # An active Buy/Sell order has been submitted/accepted - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, {order.executed.price:.2f}')
            elif order.issell():
                self.log(f'SELL EXECUTED, {order.executed.price:.2f}')
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Reset orders
        self.order = None