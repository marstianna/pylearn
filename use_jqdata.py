import time

import jqdatasdk as jq
import pandas as pd

import config
import test
import util
from market.chinese import shanghai_a, chuangye, shenzhen_a, kechuang
from result import Result

if __name__ == '__main__':
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.max_rows', 10000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.width', 1000)

    jq.auth(username=config.jqdata_username,password=config.jqdata_password)

    results = []
    start_time = time.time()
    stocks = ['600745.XSHG','603236.XSHG','603489.XSHG','002046.XSHE','002810.XSHE','002850.XSHE','002241.XSHE','300014.XSHE','300850.XSHE','300124.XSHE','688050.XSHG','688017.XSHG']
    # stocks.extend(shanghai_a.stocks)
    # stocks.extend(shenzhen_a.stocks)
    # stocks.extend(chuangye.stocks)
    # stocks.extend(kechuang.stocks)
    for stock_code in stocks:
        print("-----------------start:"+stock_code+"-------------------")
        daily = jq.get_price(security=stock_code, frequency='1d', start_date='2021-01-01', end_date='2022-01-14')
        frame = pd.DataFrame(
            data={'code': stock_code, 'time_key': daily.index.values, 'open': daily['open'], 'close': daily['close'],
                  'high': daily['high'], 'low': daily['low'], 'volume': daily['volume']}).dropna()
        if len(frame) == 0:
            continue
        tmp = test.execute_strategies(frame)

        tmp.sort(key=lambda res: res.date)
        test.compute_profit_score(tmp)
        if len(tmp) <= 0:
            continue
        # today = util.filter_last_day(tmp)
        # today = util.filter_day(tmp,'2022-01-12')
        # for result in today:
        #     test.stop_loss([result], tmp, frame)
        results.extend(tmp)
        # if len(today) > 0:
        #     print(pd.DataFrame(today, columns=Result.columns))
        #     results.extend(today)
    convert_results = []
    for result in results:
        convert_results.append(result.get_dict())
    print(pd.DataFrame(convert_results,columns=Result.columns))
    print("Cost time:"+str(time.time()-start_time))


