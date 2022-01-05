
import talib as ta
import pandas as pd

#当前upper和lower都存在一个如果实体(body)过小的情况下会导致命中逻辑不够精确的问题
from numba import cuda


@cuda.jit
def define_upper_hammer(open,close,high,low,ma_5,results,k=0.4):
    index = cuda.grid(1)
    days = 5
    if index < days:
        return
    if index >= len(open):
        return
    # 实体长度
    body = 0
    # 上影线
    upper_line = 0
    #下影线
    lower_line = 0
    if open[index] < close[index]:
        body = open[index] - close[index]
        upper_line = high[index] - open[index]
        lower_line = close[index] - low[index]
    else:
        body = close[index] - open[index]
        upper_line = high[index] - close[index]
        lower_line = open[index] - low[index]
        #上影线是实体的2倍,下影线是上影线的k,当前设定k=0.4
    if lower_line > 2 * body and upper_line < k * lower_line:
        # 上涨锤子线出现之前的MA5连续5天下跌,
        if ma_5[index-5] > ma_5[index-4] and ma_5[index-4] > ma_5[index - 3] and ma_5[index-3] > ma_5[index-2] and ma_5[index-2] > ma_5[index-1] and ma_5[index-1] > ma_5[index]:
            #锤子线的实体不能超过前一天的实体
            if max(close[index],open[index]) < max(close[index-1],open[index-1]):
                #锤子线的最低点要低于前5天的最低价,且下影线越长约好
                if low[index] < low[index-1] and low[index] < low[index-2] and low[index] < low[index-3] and low[index] < low[index-4] and low[index] < low[index-5]:
                    results[index][0] = 1
                    results[index][1] = index


@cuda.jit
def define_lower_hammer(open,close,high,low,ma_12,results,k=0.3):
    days = 12
    index = cuda.grid(1)

    if index < days:
        return
    if index >= len(open):
        return
    # 实体长度
    body = 0
    # 上影线
    upper_line = 0
    # 下影线
    lower_line = 0
    if open[index] < close[index]:
        body = open[index] - close[index]
        upper_line = high[index] - open[index]
        lower_line = close[index] - low[index]
    else:
        body = close[index] - open[index]
        upper_line = high[index] - close[index]
        lower_line = open[index] - low[index]
        # 上影线是实体的2倍,下影线是上影线的k,当前设定k=0.4
    if lower_line > 2 * body and upper_line < k * lower_line:
        satisfy_ma = True
        # 连续12天ma趋势线都是上涨形态
        for ma_index in range(days):
            if ma_index == 0:
                continue
            satisfy_ma = ma_12[index] > ma_12[index-ma_index]
            if not satisfy_ma:
                break;
        if satisfy_ma:
            if max(close[index],open[index]) > max(close[index-1],open[index-1]):
                satisfy_high = True;
                for body_index in range(days):
                    if body_index == 0:
                        continue
                    satisfy_high = high[index] > max(close[index-body_index],open[index-body_index])
                    if not satisfy_high:
                        break;
                if satisfy_high:
                    results[index][0] = 0
                    results[index][1] = index


@cuda.jit
def handstand_lower_hammer(open,close,high,low,ma_12,results,k=3):
    index = cuda.grid(1)

    days = 12
    if index < days:
        return
    if index >= len(open):
        return

    today_upper_line = high[index] - max(open[index], close[index])
    today_lower_line = min(open[index], close[index]) - low[index]
    today_body = max(open[index], close[index]) - min(open[index], close[index])

    if today_lower_line * k < today_upper_line and today_upper_line > today_body:
        for ma_index in range(days):
            if ma_index == 0:
                continue
            satisfy_ma = ma_12[index] > ma_12[index - ma_index]
            if not satisfy_ma:
                break;
        if satisfy_ma:
            satisfy_high = True;
            for body_index in range(days):
                if body_index == 0:
                    continue
                satisfy_high = high[index] > high[index - body_index]
                if not satisfy_high:
                    break;
            if satisfy_high:
                results[index][0] = 0
                results[index][1] = index
