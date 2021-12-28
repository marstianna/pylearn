import time

import jqdatasdk as jq
import pandas as pd

import chinese_stocks
import test
import util

if __name__ == '__main__':
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.max_rows', 10000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.width', 1000)

    jq.auth(username="18602842845",password="Cd02884077655")

    results = []
    start_time = time.time()
    for stock_code in chinese_stocks.chinese_stock:
        daily = jq.get_price(security=stock_code, frequency='1d', start_date='2021-11-01', end_date='2021-12-28')
        frame = pd.DataFrame(
            data={'code': stock_code, 'time_key': daily.index.values, 'open': daily['open'], 'close': daily['close'],
                  'high': daily['high'], 'low': daily['low'], 'volume': daily['volume']}).dropna()
        if len(frame) == 0:
            continue
        tmp = test.test_ma(frame)
        tmp.extend(test.test_impale(frame))
        tmp.extend(test.test_hammer(frame))
        tmp.extend(test.test_swallow(frame))
        tmp.extend(test.test_star(frame))
        results.extend(util.filter_today(tmp))
    print(results)
    print("Cost time:"+str(time.time()-start_time))


