# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import numpy as np
import futu as ft

import hammer_strategy
import impale_strategy
import ma_strategy as ma_s
import hammer_strategy as hs
import star_strategy
import swallon_strategy
import swallon_strategy as ss
import util
from result import Result
import time

BUY = 1
SELL = 3
IGNORE = -1
KEEP = 2
NOT_KEEP = 0

def get_buy_action(klines):
    result = hammer_strategy.define_upper_hammer(klines)
    lower = swallon_strategy.upper_swallow_lower(klines)
    if len(lower) > 0:
        for r in lower:
            result.append(r)
    impale = impale_strategy.upper_impale(klines)
    if len(impale) > 0:
        for r in impale:
            result.append(r)
    star = star_strategy.morning_star(klines)
    if len(star) > 0:
        for r in star:
            result.append(r)
    return result

def get_sell_action(klines):
    result = hammer_strategy.define_lower_hammer(klines)
    upper = swallon_strategy.lower_swallow_upper(klines)
    if len(upper) > 0:
        for r in upper:
            result.append(r)
    impale = impale_strategy.lower_impale(klines)
    if len(impale) > 0:
        for r in impale:
            result.append(r)
    star = star_strategy.evening_star(klines)
    if len(star) > 0:
        for r in star:
            result.append(r)
    return result


def get_unknown_action(klines):
    # result = []
    result = ma_s.single_ma2(klines,2)
    ma = ma_s.single_ma(klines,2)
    if len(ma) > 0:
        for r in ma:
            result.append(r)
    multi_ma = ma_s.multi_ma(klines, short_day=5, long_day=17)
    if len(multi_ma) > 0:
        for r in multi_ma:
            result.append(r)
    return result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start = time.time()
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.width', 1000)
    quote_ctx = ft.OpenQuoteContext()  # 创建行情对象
    RET_OK, ret_frame = quote_ctx.get_user_security("target")
    result = []
    for code in ret_frame['code']:
        RET_OK, kline_frame_table, next_page_req_key = quote_ctx.request_history_kline(code=code)
        buy_actions = get_buy_action(kline_frame_table)
        if len(buy_actions) > 0:
            for buy_action in buy_actions:
                result.append(buy_action)
        sell_actions = get_sell_action(kline_frame_table)
        if len(sell_actions) >0:
            for sell_action in sell_actions:
                result.append(sell_action)
        unknown_actions = get_unknown_action(kline_frame_table)
        if len(unknown_actions) >0:
            for unknown_action in unknown_actions:
                result.append(unknown_action)

    result = util.filter_today(result)
    frame = pd.DataFrame(result, columns=Result.columns)
    frame.sort_values('stock_code', inplace=True)
    print(frame)
    quote_ctx.close()  # 关闭对象，防止连接条数用尽
    print(int(time.time()-start))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
