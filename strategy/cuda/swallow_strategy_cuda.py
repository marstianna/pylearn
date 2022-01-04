import talib as ta
from numba import cuda

from result import Result


# 吞没形态还需要考虑命中当天的成交量的情况,如果出现对应的放量,那么认为形态有效
# 吞没形态应该在吞噬的上行或者下行的实体越多,形态效果越强烈,intension的值应该越大
@cuda.jit
def upper_swallow_lower(open, close, high, low, ma_7, results):
    days = 7
    index = cuda.threadIdx.x + cuda.blockDim.x * cuda.gridDim.x

    if index < days:
        return
    if index >= len(open):
        return

    if open[index-1] < close[index-1]:
        return
    if open[index] > close[index]:
        return
    if close[index] >= max(open[index-1],close[index-1]) and open[index] <= min(open[index-1],close[index-1]):

        satisfy_ma = True
        # 连续days天ma趋势线都是下跌形态
        for ma_index in range(days):
            if ma_index == 0:
                continue
            satisfy_ma = ma_7[index - ma_index] < ma_7[index - ma_index -1]
            if not satisfy_ma:
                break
        if satisfy_ma:
            satisfy_low = True
            for body_index in range(days):
                if body_index == 0:
                    continue
                satisfy_low = open[index] <= min(close[index - body_index],
                                                                open[index - body_index])
                if not satisfy_low:
                    break
            if satisfy_low:
                results[index][0] = 1
                results[index][1] = index


@cuda.jit
def lower_swallow_upper(open, close, high, low, ma_7, results):
    days = 7
    index = cuda.threadIdx.x + cuda.blockDim.x * cuda.gridDim.x
    if index < days:
        return
    if index >= len(open):
        return

    if open[index-1] > close[index-1]:
        return
    if open[index] < close[index]:
        return

    if open[index] >= max(open[index-1], close[index-1]) and close[index] <= min(open[index-1],
                                                                                           close[index-1]):

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
                satisfy_high = open[index] >= max(close[index - body_index],
                                                  open[index - body_index])
                if not satisfy_high:
                    break
            if satisfy_high:
                results[index][0] = 0
                results[index][1] = index