import pandas as pd
import numpy as np
import futu as ft
import talib as ta
import math

from result import Result

BUY = 1
SELL = 3
IGNORE = -1
KEEP = 2
NOT_KEEP = 0


def single_ma(klines,days=2):
    results = []
    test = single_ma_back_test(klines, days)
    result = test.iloc[len(test) - 1]
    if result['action'] == 1:
        results.append(Result(result['stock'],"BUY",result['close_price'],result['time'],'single_ma').get_dict())
    elif result['action'] == 3:
        results.append(Result(result['stock'], "SELL", result['close_price'], result['time'], 'single_ma').get_dict())
    return results


def single_ma_back_test(kline, days):
    ma = ta.MA(kline['close'].values, timeperiod=days)
    close_values = kline['close'].values
    date = kline['time_key'].values
    result = np.arange(len(kline))
    keep = False
    for index in range(len(kline)):
        index_ = ma[index]
        if math.isnan(index_):
            result[index] = IGNORE
            continue
        if index == 0:
            result[index] = BUY
            keep = True
            continue
        before = ma[index-1]
        if math.isnan(before):
            result[index] = BUY
            keep = True
            continue
        if bool(keep):
            if index_ >= before:
                result[index] = KEEP
                keep = True
                continue
            else:
                result[index] = SELL
                keep = False
                continue
        else:
            if index_ >= before:
                result[index] = BUY
                keep = True
                continue
            else:
                result[index] = NOT_KEEP
                keep = False
                continue
    return pd.DataFrame({"stock": kline['code'], "time": kline['time_key'].values, "close_price": kline['close'], "action": result})


def single_ma2(klines,days=2):
    results = []
    test = single_ma_back_test(klines, days)
    result = test.iloc[len(test) - 1]
    if result['action'] == 1:
        results.append(Result(result['stock'], "BUY", result['close_price'], result['time'], 'single_ma2').get_dict())
    elif result['action'] == 3:
        results.append(Result(result['stock'], "SELL", result['close_price'], result['time'], 'single_ma2').get_dict())
    return results



def single_ma2_back_test(kline,days):
    ma = ta.MA(kline['close'].values, timeperiod=days)
    close_values = kline['close'].values
    date = kline['time_key'].values
    result = np.arange(len(kline))
    keep = False
    for index in range(len(kline)):
        index_ = ma[index]
        if math.isnan(index_):
            result[index] = IGNORE
            continue
        if index == 0:
            if close_values[index] > index_:
                result[index] = BUY
                keep = True
            else:
                result[index] = NOT_KEEP
                keep = False
            continue
        before = ma[index - 1]
        if math.isnan(before):
            if close_values[index] > index_:
                result[index] = BUY
                keep = True
            else:
                result[index] = NOT_KEEP
                keep = False
            continue
        if bool(keep):
            if close_values[index] > index_:
                result[index] = KEEP
                keep = True;
            else:
                result[index] = SELL
                keep = False
        else:
            if close_values[index] > index_:
                result[index] = BUY
                keep = True
                continue
            else:
                result[index] = NOT_KEEP
                keep = False
                continue

    frame = pd.DataFrame(
        {"stock": kline['code'], "time": kline['time_key'].values, "close_price": kline['close'],"ma":ma, "action": result})
    # print(frame)
    return frame


def multi_ma(kline,days=[2,12]):
    return "a"

