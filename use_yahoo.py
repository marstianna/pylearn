import pandas_datareader as pdd
import pandas as pd
import requests

if __name__ == '__main__':
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.width', 1000)

    url = 'http://hq.sinajs.cn/list=gb_baba'
    url_1 = 'http://stock2.finance.sina.com.cn/futures/api/json.php/CffexFuturesService.getCffexFuturesDailyKLine?symbol=baba'
    print(requests.get(url_1).text)
