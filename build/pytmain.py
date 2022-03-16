from pytrends.request import TrendReq

class Pytmain:
    def get_data(self, keyword):
        """
        Gathers the google trends data using the pytrends api. Returns 
        a pandas dataframe

         Arguments:
            keyword {_str_} -- search keyword to gather google search trends for

        Returns:
            _pd.Dataframe_ -- Pandas Dataframe to be used when plotting
        """
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([keyword], timeframe='2017-02-01 2022-01-31')
        
        return pytrends.interest_over_time()
