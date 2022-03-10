import backtrader as bt

class TrendsVolatilityInd(bt.Indicator):
    """
    Analyzes the google search trends csv, outputs either True if volatility detected
    or False if stable. Work in progress, but it is working

    Arguments:
        bt {backtrader.Datafeed} - the data that the indicator will work with

    """

    lines = ('tvi',) 

    params = (('threshold', 50),)
    
    def next(self): 
        # check to see if previous self.lines.tvi exists
        if not(self.datas[0].close[-1] is None or self.datas[0].close[-1] == 0):
               # gather the percent rate of change of the data
            percent_change = ((self.datas[0].close[0] - self.datas[0].close[-1])/self.datas[0].close[-1]) * 100
            if abs(percent_change) > self.params.threshold:
                self.lines.tvi[0] = True
            else: 
                self.lines.tvi[0] = False