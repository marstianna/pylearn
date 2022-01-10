import talib as ta
import math

from numba import cuda

from result import Result


#平头顶
@cuda.jit
def flat_head(open,close,high,low,ma_5,results,days=5,k=0.005):

    index = cuda.grid(1)

    if index < days:
        return
    if index >= len(open):
        return

    # 昨天必须是一根大阳线
    if open[index-1] > close[index-1]:
        return
    # 今天必须是一根阴线
    if open[index] < close[index]:
        return

    today_upper_line = high[index] - max(open[index], close[index])
    today_lower_line = min(open[index], close[index]) - low[index]
    today_body = max(open[index], close[index]) - min(open[index], close[index])

    if today_body < today_upper_line or today_body < today_lower_line:
        return

    if high[index] * (1 + k) > high[index - 1] > high[index] * (1 - k):
        satisfy_ma = True
        # 连续days天ma趋势线都是上涨形态
        for ma_index in range(days):
            satisfy_ma = ma_5[index - ma_index] > ma_5[index - ma_index - 1]
            if not satisfy_ma:
                break
        if satisfy_ma:
            satisfy_low = True
            highest = max(high[index],high[index-1])
            for idx in range(days):
                if idx <= 1:
                    continue;
                if highest < high[index - idx]:
                    satisfy_low = False
                    break
            if satisfy_low:
                results[index][0]=1
                results[index][1]=index

@cuda.jit
def flat_bottom(open,close,high,low,ma_5,results,days=5,k=0.005):
    index = cuda.grid(1)
    if index < days:
        return
    if index >= len(open):
        return

    # 昨天必须是一根大阴线
    if open[index-1] < close[index-1]:
        return
    # 今天必须是一根阳线
    if open[index] > close[index]:
        return

    today_upper_line = high[index] - max(open[index], close[index])
    today_lower_line = min(open[index], close[index]) - low[index]
    today_body = max(open[index], close[index]) - min(open[index], close[index])
    
    if today_body > today_upper_line or today_body > today_lower_line:
        return

    if low[index] * (1 + k) > low[index-1] > low[index] * (1 - k):
        satisfy_ma = True
        # 连续days天ma趋势线都是上涨形态
        for ma_index in range(days):
            satisfy_ma = ma_5[index - ma_index] < ma_5[index - ma_index - 1]
            if not satisfy_ma:
                break
        if satisfy_ma:
            satisfy_low = True
            lowest = min(low[index], low[index-1])
            for idx in range(days):
                if idx <= 1:
                    continue
                if lowest > low[index - idx]:
                    satisfy_low = False
                    break
            if satisfy_low:
                results[index][0] = 0
                results[index][1] = index