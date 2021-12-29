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
import pregnant_strategy
import star_strategy
import swallon_strategy
import swallon_strategy as ss
import tower_strategy
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
    result.extend(swallon_strategy.upper_swallow_lower(klines))
    result.extend(impale_strategy.upper_impale(klines))
    result.extend(star_strategy.morning_star(klines))
    result.extend(pregnant_strategy.upper_pregnant(klines))
    result.extend(tower_strategy.tower_bottom(klines))
    return result

def get_sell_action(klines):
    result = hammer_strategy.define_lower_hammer(klines)
    result.extend(swallon_strategy.lower_swallow_upper(klines))
    result.extend(impale_strategy.lower_impale(klines))
    result.extend(star_strategy.evening_star(klines))
    result.extend(hammer_strategy.handstand_lower_hammer(klines))
    result.extend(star_strategy.falling_star(klines))
    result.extend(pregnant_strategy.lower_pregnant(klines))
    result.extend(tower_strategy.tower_head(klines))
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
    RET_OK, ret_frame = quote_ctx.get_user_security("first")
    result = []
    for code in ret_frame['code']:
        RET_OK, kline_frame_table, next_page_req_key = quote_ctx.request_history_kline(code=code)
        result.extend(get_buy_action(kline_frame_table))
        result.extend(get_sell_action(kline_frame_table))
        # result.extend(get_unknown_action(kline_frame_table))

    # result = util.filter_day(result,'2021-12-28')
    frame = pd.DataFrame(result, columns=Result.columns)
    values = frame.sort_values(by=['stock_code', 'date'])
    print(values)
    quote_ctx.close()  # 关闭对象，防止连接条数用尽
    print(int(time.time()-start))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
