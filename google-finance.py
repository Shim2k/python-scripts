'''
Import libraries to handle files, json and time.
'''
import os
import urllib2
import json
import datetime
import time as t

'''
GoogleFinanceData class takes Google Finance stock data as a source
and parse it into an object we are going to use to save our data
'''
class GoogleFinanceData:
    def __init__(self):
        self.prefix = "http://finance.google.com/finance/info?client=ig&q="
    
    def get(self, symbol, exchange):
        source = self.prefix+"%s:%s"%(exchange,symbol)
        data = urllib2.urlopen(source)
        
        obj = json.loads(data.read()[3:])

        return obj[0]
        
'''
First we instantiate the Google Finance class, assign today's date to "day" and current time to "time".
After that we enter an infinite loop which checks if the stock market is open and if so starts saving data.
We assign all symbols we want to track to the "symbols" variable and then for each one we call GoogleFinanceData().
'''
if __name__ == "__main__":
    f = GoogleFinanceData()
    while 1:
        day = datetime.date.today().weekday() # 0 is Monday, 6 is Sunday
        time = datetime.datetime.now().time()
        if (time > datetime.time(23,00)):
            sleep(57600)
        while day < 5 and (time >= datetime.time(16,00) and time <= datetime.time(23,00)):
            symbols = {("SBUX", "NASDAQ"), ("AAPL", "NASDAQ"), ("AIG", "NYSE"), ("KO", "NYSE"), ("V", "NYSE"), ("TSLA", "NASDAQ")} #All the symbols you want to track
            for quote in symbols:
                tick = f.get(quote[0], quote[1])
                str = '{0}\t{1}\t{2}\t{3}\t{4}\t{5}'.format(tick['e'], tick['t'], tick['l'], tick['c'], tick['cp'], tick['lt'])

                '''
                The final data we're going to append to our file is stored in the "str" variable.
                We check if a file exists and if so, append "str" to it. If not, create one:
                '''
                if not os.path.exists('data'):
                    with open('data', 'w') as obj:
                        obj.write(str)
                        obj.write('\n')
                        obj.close()
                else:
                    with open('data', 'a') as obj:
                        obj.write(str)
                        obj.write('\n')
                        obj.close()
                t.sleep(1)