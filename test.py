import pandas as pd
import numpy as np
import futu as ft

import flat_strategy
import hammer_strategy
import impale_strategy
import ma_strategy
import pregnant_strategy
import star_strategy
import swallon_strategy
import main
import util
from result import Result


def test_hammer(klines):
    result = hammer_strategy.define_upper_hammer(klines)
    result.extend(hammer_strategy.define_lower_hammer(klines))
    result.extend(hammer_strategy.handstand_lower_hammer(klines))
    return result


def test_swallow(klines):
    result = swallon_strategy.upper_swallow_lower(klines)
    result.extend(swallon_strategy.lower_swallow_upper(klines))
    return result


def test_impale(klines):
    upper_result = impale_strategy.upper_impale(klines)
    upper_result.extend(impale_strategy.lower_impale(klines))
    return upper_result


def test_star(klines):
    result = star_strategy.morning_star(klines)
    # print(pd.DataFrame(upper_result, columns=Result.columns))
    star = star_strategy.evening_star(klines)
    result.extend(star)
    result.extend(star_strategy.falling_star(klines))
    return result
    # print(pd.DataFrame(lower_result, columns=Result.columns))


def test_ma(klines):
    ma = ma_strategy.multi_ma(klines,short_day=7,long_day=21)
    ma.extend(ma_strategy.single_ma2(klines,days=2))
    ma.extend(ma_strategy.single_ma(klines,days=2))
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


def test_group():
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.width', 1000)
    quote_ctx = ft.OpenQuoteContext()  # 创建行情对象
    RET_OK, ret_frame = quote_ctx.get_user_security("first")
    results = []
    for code in ret_frame['code']:
        RET_OK, kline_frame_table, next_page_req_key = quote_ctx.request_history_kline(code=code)
        ma = test_swallow(kline_frame_table)
        results.extend(ma)
    frame = pd.DataFrame(results, columns=Result.columns)
    values = frame.sort_values(by=['stock_code', 'date'])
    print(values)
    quote_ctx.close()


def test_single():
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.max_rows', 10000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.width', 1000)
    quote_ctx = ft.OpenQuoteContext()  # 创建行情对象
    RET_OK, kline_frame_table, next_page_req_key = quote_ctx.request_history_kline(code='SH.601012')
    result = []
    # buy_actions = main.get_buy_action(kline_frame_table)
    # if len(buy_actions) > 0:
    #     for buy_action in buy_actions:
    #         result.append(buy_action)
    # sell_actions = main.get_sell_action(kline_frame_table)
    # if len(sell_actions) > 0:
    #     for sell_action in sell_actions:
    #         result.append(sell_action)
    unknown_actions = main.get_unknown_action(kline_frame_table)
    if len(unknown_actions) > 0:
        for unknown_action in unknown_actions:
            result.append(unknown_action)

    frame = pd.DataFrame(result, columns=Result.columns)
    frame = frame.sort_values(by=['stock_code','date'],inplace=True)
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
    test_group()