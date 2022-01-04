import time

import jqdatasdk as jq
import pandas as pd

import config
import test
import test_cuda
import util
from chinese import shenzhen_a, chuangye, kechuang
from market.chinese import shanghai_a
from result import Result

if __name__ == '__main__':
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.max_rows', 10000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.width', 1000)

    jq.auth(username=config.jqdata_username,password=config.jqdata_password)

    results = []
    start_time = time.time()
    stocks = []
    stocks.extend(shanghai_a.stocks)
    stocks.extend(shenzhen_a.stocks)
    stocks.extend(chuangye.stocks)
    stocks.extend(kechuang.stocks)
    for stock_code in stocks:
        print("-----------------start:"+stock_code+"-------------------")
        daily = jq.get_price(security=stock_code, frequency='1d', start_date='2021-11-01', end_date='2022-01-04')
        frame = pd.DataFrame(
            data={'code': stock_code, 'time_key': daily.index.values, 'open': daily['open'], 'close': daily['close'],
                  'high': daily['high'], 'low': daily['low'], 'volume': daily['volume']}).dropna()
        if len(frame) == 0:
            continue
        tmp = []
        tmp.extend(test_cuda.get_result_from_cuda(frame))
        today = util.filter_timestamp_day(tmp)
        if len(today) > 0:
            print(pd.DataFrame(today, columns=Result.columns))
            results.extend(today)
    print(pd.DataFrame(results,columns=Result.columns))
    print("Cost time:"+str(time.time()-start_time))


