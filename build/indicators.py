import backtrader as bt

class DummyInd(bt.Indicator):
    """
    Dummy Indicator, outputs either 0.0 or param(default is 5), Inherits from 
    Indicator

    Arguments:
        lines {Lines} -- the lines or bars that the data will take
        
    """
    lines = ('dummyline',)

    params = (('value', 5),)

    def __init__(self):
        self.lines.dummyline = bt.Max(0.0, self.params.value)