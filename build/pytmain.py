from pytrends.request import TrendReq

class Pytmain:
    def get_data(self, keyword):
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([keyword], timeframe='2018-01-01 2022-01-01')
        
        return pytrends.interest_over_time()
