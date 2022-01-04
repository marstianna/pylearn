from numba import cuda

from result import Result
import talib as ta


@cuda.jit
def upper_pregnant(open,close,high,low,ma_5,results,days=5,k=3):
    index = cuda.threadIdx.x + cuda.blockDim.x * cuda.gridDim.x
    
    if index < days:
        return
    if index >= len(open):
        return

    today_body = max(open[index],close[index]) - min(open[index],close[index])
    yesterday_body = max(open[index-1], close[index-1]) - min(open[index-1], close[index-1])

    if open[index-1] < close[index-1]:
        return

    if yesterday_body > today_body * k and min(open[index-1], close[index-1]) < min(open[index],close[index]) and  max(open[index-1], close[index-1]) > max(open[index],close[index]):
        satisfy_ma = True
        # 连续days天ma趋势线都是下跌形态
        for ma_index in range(days):
            satisfy_ma = ma_5[index - ma_index] < ma_5[index - ma_index - 1]
            if not satisfy_ma:
                break
        if satisfy_ma:
            results[index][0] = 1
            results[index][1] = index


@cuda.jit
def lower_pregnant(open,close,high,low,ma_5,results,days=5,k=3):
    index = cuda.threadIdx.x + cuda.blockDim.x * cuda.gridDim.x
    
    if index < days:
        return
    if index >= len(open):
        return

    today_body = max(open[index], close[index]) - min(open[index], close[index])
    yesterday_body = max(open[index-1], close[index-1]) - min(open[index-1], close[index-1])

    if open[index-1] > close[index-1]:
        return

    if yesterday_body > today_body * k and min(open[index-1], close[index-1]) < min(open[index],close[index]) and  max(open[index-1], close[index-1]) > max(open[index],close[index]):
        satisfy_ma = True
        # 连续days天ma趋势线都是上涨形态
        for ma_index in range(days):
            satisfy_ma = ma_5[index - ma_index] > ma_5[index - ma_index - 1]
            if not satisfy_ma:
                break
        if satisfy_ma:
            results[index][0] = 0
            results[index][1] = index