import pandas as pd
import numpy as np
import futu as ft
import talib as ta
import math

from result import Result


def single_ma(kline, days=2):
    ma = ta.MA(kline['close'].values, timeperiod=days)
    results = []
    keep = False
    for index in range(len(kline)):
        today = kline.iloc[index]
        index_ = ma[index]
        action = ''
        if index == 0:
            results.append(Result(today['code'], 'BUY', today['close'], today['time_key'], 'single_ma2').get_dict())
            keep = True
            continue
        before = ma[index-1]
        if math.isnan(before):
            results.append(Result(today['code'], 'BUY', today['close'], today['time_key'], 'single_ma2').get_dict())
            keep = True
            continue
        if bool(keep):
            if index_ < before:
                results.append(Result(today['code'], 'SELL', today['close'], today['time_key'], 'single_ma2').get_dict())
                keep = False
                continue
        else:
            if index_ >= before:
                results.append(Result(today['code'], 'BUY', today['close'], today['time_key'], 'single_ma2').get_dict())
                keep = True
                continue
    return results


def single_ma2(kline,days=2):
    ma = ta.MA(kline['close'].values, timeperiod=days)
    results = []
    close_values = kline['close'].values
    keep = False
    for index in range(len(kline)):
        today = kline.iloc[index]
        index_ = ma[index]

        if index == 0:
            if close_values[index] > index_:
                results.append(Result(today['code'], 'BUY', today['close'], today['time_key'], 'single_ma2').get_dict())
                keep = True
            continue
        before = ma[index - 1]
        if math.isnan(before):
            if close_values[index] > index_:
                results.append(Result(today['code'], 'BUY', today['close'], today['time_key'], 'single_ma2').get_dict())
                keep = True
            continue
        if bool(keep):
            if close_values[index] <= index_:
                results.append(Result(today['code'], 'SELL', today['close'], today['time_key'], 'single_ma2').get_dict())
                keep = False
        else:
            if close_values[index] > index_:
                results.append(Result(today['code'], 'BUY', today['close'], today['time_key'], 'single_ma2').get_dict())
                keep = True
                continue

    return results


def multi_ma(kline,short_day=2,long_day=12):
    results = []

    ma_short = ta.MA(kline['close'].values,timeperiod = short_day)
    ma_long = ta.MA(kline['close'].values,timeperiod = long_day)

    last_days = 1

    for ma_idx in range(len(ma_short)):
        today = kline.iloc[ma_idx]

        ma_short_day = ma_short[ma_idx]
        if math.isnan(ma_short_day):
            continue
        ma_long_day = ma_long[ma_idx]
        if math.isnan(ma_long_day):
            continue
        if ma_short_day >= ma_long_day:
            buy = True
            for idx in range(last_days):
                actual_idx = ma_idx - 1 - idx
                if math.isnan(ma_short[actual_idx]):
                    buy = False
                    break
                if math.isnan(ma_long[actual_idx]):
                    buy = False
                    break
                if ma_short[actual_idx] > ma_long[actual_idx]:
                    buy = False
                    break
            if buy:
                results.append(
                    Result(today['code'], 'BUY', today['close'], today['time_key'], 'double_ma').get_dict())
        if ma_short_day <= ma_long_day:
            sell = True
            for idx in range(last_days):
                actual_idx = ma_idx - 1 - idx
                if math.isnan(ma_short[actual_idx]):
                    sell = False
                    break
                if math.isnan(ma_long[actual_idx]):
                    sell = False
                    break
                if ma_short[actual_idx] < ma_long[actual_idx]:
                    sell = False
                    break
            if sell:
                results.append(
                    Result(today['code'], 'SELL', today['close'], today['time_key'], 'double_ma').get_dict())

    return results

