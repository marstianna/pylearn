# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import numpy as np
import futu as ft

import flat_strategy
import hammer_strategy
import impale_strategy
import ma_strategy as ma_s
import pregnant_strategy
import star_strategy
import swallon_strategy
import tower_strategy
from strategy import flat_strategy, hammer_strategy, impale_strategy, pregnant_strategy, \
    swallon_strategy, star_strategy
from indicator import ma_strategy as ma_s
import util
from result import Result
import time


def get_buy_action(klines):
    result = hammer_strategy.define_upper_hammer(klines)
    result.extend(swallon_strategy.upper_swallow_lower(klines))
    result.extend(impale_strategy.upper_impale(klines))
    result.extend(star_strategy.morning_star(klines))
    result.extend(pregnant_strategy.upper_pregnant(klines))
    result.extend(flat_strategy.flat_bottom(klines))
    return result


def get_sell_action(klines):
    result = hammer_strategy.define_lower_hammer(klines)
    result.extend(swallon_strategy.lower_swallow_upper(klines))
    result.extend(impale_strategy.lower_impale(klines))
    result.extend(star_strategy.evening_star(klines))
    result.extend(hammer_strategy.handstand_lower_hammer(klines))
    result.extend(star_strategy.falling_star(klines))
    result.extend(pregnant_strategy.lower_pregnant(klines))
    result.extend(flat_strategy.flat_head(klines))
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
    RET_OK, ret_frame = quote_ctx.get_user_security("港股")
    result = []
    for code in ret_frame['code']:
        print("-----------------"+code+"------------------")
        RET_OK, kline_frame_table, next_page_req_key = quote_ctx.request_history_kline(code=code)
        result.extend(get_buy_action(kline_frame_table))
        result.extend(get_sell_action(kline_frame_table))
        # result.extend(get_unknown_action(kline_frame_table))
    result = util.filter_day(result,'2022-01-03')
    frame = pd.DataFrame(result, columns=Result.columns)
    values = frame.sort_values(by=['stock_code', 'date'])
    print(values)
    quote_ctx.close()  # 关闭对象，防止连接条数用尽
    print(int(time.time()-start))

