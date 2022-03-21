import backtrader as bt
from backtrader.indicators import MovingAverageSimple, BollingerBands

class TBBI(bt.Indicator):
    """
    Analyzes the google search trends csv, outputs either True if volatility detected
    or False if stable. Work in progress, but it is working

    Arguments:
        bt {backtrader.Datafeed} - the data that the indicator will work with

    """

    lines = ('tbbi',) 

    params = (('period', 30)
            ,('devfactor', .5),)
    
    def __init__(self) -> None:
        bb = BollingerBands(self.datas[0].close, period=self.params.period, devfactor=self.params.devfactor)
        self.top = bb.lines.top
        self.bot = bb.lines.bot

    def next(self):
        if self.datas[0].close[0] > self.top[0]:
            self.lines.tbbi[0] = 1
        elif self.datas[0].close[0] < self.bot[0]:
            self.lines.tbbi[0] = -1
        else:
            self.lines.tbbi[0] = 0  

        




