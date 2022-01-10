import numpy as np

import pandas as pd
import futu as ft

from strategy import flat_strategy, hammer_strategy, impale_strategy, pregnant_strategy, swallow_strategy, \
    star_strategy
from indicator import ma_strategy
import main
import util
from result import Result
import time

from strategy.stop_loss import bottom_stop_loss_line
from strategy.stop_loss import head_stop_loss_line


def test_hammer(klines):
    result = hammer_strategy.define_upper_hammer(klines)
    result.extend(hammer_strategy.define_lower_hammer(klines))
    result.extend(hammer_strategy.handstand_lower_hammer(klines))
    return result


def test_swallow(klines):
    result = swallow_strategy.upper_swallow_lower(klines)
    result.extend(swallow_strategy.lower_swallow_upper(klines))
    return result


def test_impale(klines):
    upper_result = impale_strategy.upper_impale(klines)
    upper_result.extend(impale_strategy.lower_impale(klines))
    return upper_result


def test_star(klines):
    result = star_strategy.morning_star(klines)
    result.extend(star_strategy.evening_star(klines))
    result.extend(star_strategy.falling_star(klines))
    return result


def test_ma(klines):
    ma = []
    ma.extend(ma_strategy.multi_ma(klines, short_day=12, long_day=26))
    # ma.extend(ma_strategy.single_ma2(klines,days=26))
    # ma.extend(ma_strategy.single_ma(klines,days=26))
    compute_profit(ma)
    return ma


def test_pregnant(klines):
    result = pregnant_strategy.lower_pregnant(klines)
    result.extend(pregnant_strategy.upper_pregnant(klines))
    return result


def test_flat(klines):
    result = flat_strategy.flat_bottom(klines)
    result.extend(flat_strategy.flat_head(klines))
    return result


def stop_loss(today_results, results, kline):
    random = today_results[0]
    timeperiod = np.int(7),
    if random['action'] == 'BUY':
        bottom_stop_loss_line.bottom_stop_loss_line(random, results, kline, np.int(7))
    else:
        head_stop_loss_line.head_stop_loss_line(random, results, kline, np.int(12))


def test_group():
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.max_rows', 10000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.width', 1000)
    quote_ctx = ft.OpenQuoteContext()  # 创建行情对象
    RET_OK, ret_frame = quote_ctx.get_user_security("港股")
    results = []
    for code in ret_frame['code']:
        print("-----------------start:" + code + "-------------------")
        RET_OK, kline_frame_table, next_page_req_key = quote_ctx.request_history_kline(code=code)
        tmp = []
        tmp.extend(test_flat(kline_frame_table))
        tmp.extend(test_impale(kline_frame_table))
        tmp.extend(test_hammer(kline_frame_table))
        tmp.extend(test_swallow(kline_frame_table))
        tmp.extend(test_star(kline_frame_table))
        tmp.extend(test_pregnant(kline_frame_table))
        # compute_profit(ma)
        today = util.filter_today(tmp)
        if len(today) > 0:
            stop_loss(today, tmp, kline_frame_table)
        results.extend(today)
        # results.extend(util.filter_day(tmp,'2022-01-07'))
        # results.extend(tmp)
    t = pd.DataFrame(results, columns=Result.columns)
    values = t.sort_values(by=['stock_code', 'date'])
    print(values)
    quote_ctx.close()


def test_single():
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.max_rows', 10000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.width', 1000)
    quote_ctx = ft.OpenQuoteContext()  # 创建行情对象
    RET_OK, kline_frame_table, next_page_req_key = quote_ctx.request_history_kline(code='SH.601888')
    tmp = []
    tmp.extend(test_flat(kline_frame_table))
    tmp.extend(test_impale(kline_frame_table))
    tmp.extend(test_hammer(kline_frame_table))
    tmp.extend(test_swallow(kline_frame_table))
    tmp.extend(test_star(kline_frame_table))
    tmp.extend(test_pregnant(kline_frame_table))

    today = util.filter_today(tmp)

    bottom_stop_loss_line.bottom_stop_loss_line(today[0], tmp, kline_frame_table, 7)

    frame = pd.DataFrame(tmp, columns=Result.columns)
    frame = frame.sort_values(by=['stock_code', 'date'])
    print(frame)
    quote_ctx.close()


def compute_profit(results):
    profit = 0
    buy_price = -1
    for result in results:
        if buy_price == -1 and result['action'] == 'SELL':
            continue
        if result['action'] == 'BUY':
            if buy_price == -1:
                buy_price = result['price']
            else:
                buy_price = (result['price'] + buy_price) / 2
        if result['action'] == 'SELL':
            profit += (result['price'] - buy_price) / buy_price
            buy_price = -1
        result['profit'] = profit


if __name__ == '__main__':
    start = time.time()
    test_group()
    # test_single()
    # print(100000*(1.5**12))
    print(int(time.time() - start))
