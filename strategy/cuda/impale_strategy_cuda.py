from numba import cuda

from result import Result
import talib as ta


@cuda.jit
def upper_impale(open,close,high,low,ma_7,results,days=7):
    index = cuda.grid(1)
    if index < days:
        return
    if index >= len(open):
        return

    if open[index-1] < close[index-1]:
        return
    if open[index] > close[index]:
        return

    if max(open[index-1], close[index-1]) > close[index] > (0.5 * (open[index-1] + close[index-1])) \
            and open[index] < low[index-1]:

        satisfy_ma = True
        # 连续days天ma趋势线都是下跌形态
        for ma_index in range(days):
            satisfy_ma = ma_7[index - ma_index] < ma_7[index - ma_index - 1]
            if not satisfy_ma:
                break
        if satisfy_ma:
            satisfy_low = True
            for body_index in range(days):
                if body_index == 0:
                    continue
                satisfy_low = open[index] < min(close[index - body_index],open[index - body_index])
                if not satisfy_low:
                    break
            if satisfy_low:
                results[index][0] = 1
                results[index][1] = index


@cuda.jit
def lower_impale(open,close,high,low,ma_7,results,days=7):
    index = cuda.grid(1)
    if index < days:
        return
    if index >= len(open):
        return

    if open[index-1] > close[index-1]:
        return
    if open[index] < close[index]:
        return ;

    if open[index] > high[index-1] \
            and (0.5 * (open[index-1] + close[index-1])) > close[index] > min(open[index-1],close[index-1]):

        satisfy_ma = True
        # 连续days天ma趋势线都是上涨形态
        for ma_index in range(days):
            if ma_index == 0:
                continue
            satisfy_ma = ma_7[index - ma_index] > ma_7[index - ma_index - 1]
            if not satisfy_ma:
                break
        if satisfy_ma:
            satisfy_high = True
            for body_index in range(days):
                if body_index == 0:
                    continue
                satisfy_high = open[index] > max(close[index - body_index],
                                                   open[index - body_index])
                if not satisfy_high:
                    break
            if satisfy_high:
                results[index][0] = 0
                results[index][1] = index
