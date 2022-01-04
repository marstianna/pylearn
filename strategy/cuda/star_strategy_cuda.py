from numba import cuda

from result import Result
import talib as ta


@cuda.jit
def morning_star(open, close, high, low, ma_5, results):
    index = cuda.threadIdx.x + cuda.blockDim.x * cuda.gridDim.x
    days = 5

    if index < days:
        return
    if (index + 1) >= len(open):
        return

    # 昨天必须是绿色
    if close[index - 1] > open[index - 1]:
        return
    # 明天必须是红色
    if close[index + 1] < open[index + 1]:
        return

    if max(open[index], close[index]) > min(open[index - 1], close[index - 1]):
        return

    if min(open[index + 1], close[index + 1]) < max(open[index], close[index]):
        return

    if close[index + 1] > 0.5 * (open[index - 1] + close[index - 1]):
        satisfy_ma = True
        # 连续days天ma趋势线都是下跌形态
        for ma_index in range(days):
            if ma_index == 0:
                continue
            satisfy_ma = ma_5[index - ma_index] < ma_5[index - ma_index - 1]
            if not satisfy_ma:
                break
        if satisfy_ma:
            satisfy_low = True
            for body_index in range(days):
                if body_index == 0:
                    continue
                satisfy_low = open[index] < min(close[index - body_index]['close'],
                                                open[index - body_index]['open'])
                if not satisfy_low:
                    break
            if satisfy_low:
                results[index][0] = 1
                results[index][1] = index


@cuda.jit
def evening_star(open, close, high, low, ma_5, results):
    index = cuda.threadIdx.x + cuda.blockDim.x * cuda.gridDim.x
    days = 5
    if index < days:
        return
    if (index + 1) >= len(open):
        return
    # 昨天必须是红色
    if close[index - 1] < open[index - 1]:
        return
    # 明天必须是绿色
    if close[index + 1] > open[index + 1]:
        return

    # if tomorrow['volume'] < yesterday['volume']:
    #     return

    if min(open[index], close[index]) < max(open[index - 1], close[index - 1]):
        return

    # if max(open[index+1],close[index+1]) > min(open[index],close[index]):
    #     return

    if close[index + 1] < 0.5 * (open[index - 1] + close[index - 1]):

        satisfy_ma = True
        # 连续days天ma趋势线都是上涨形态
        for ma_index in range(days):
            if ma_index == 0:
                continue
            satisfy_ma = ma_5[index - ma_index] > ma_5[index - ma_index - 1]
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


@cuda.jit
def falling_star(open, close, high, low, ma_5, results, k=3):
    index = cuda.threadIdx.x + cuda.blockDim.x * cuda.gridDim.x
    if index < 1:
        return
    if (index + 1) >= len(open):
        return

    today_upper_line = high[index] - max(open[index], close[index])
    yesterday_upper_line = high[index-1] - max(open[index - 1], close[index - 1])
    tomorrow_upper_line = high[index+1] - max(open[index + 1], close[index + 1])

    today_lower_line = min(open[index], close[index]) - low[index]
    yesterday_lower_line = min(open[index - 1], close[index - 1]) - low[index-1]
    tomorrow_lower_line = min(open[index + 1], close[index + 1]) - low[index+1]

    today_body = max(open[index], close[index]) - min(open[index], close[index])
    yesterday_body = max(open[index - 1], close[index - 1]) - min(open[index - 1], close[index - 1])
    tomorrow_body = max(open[index + 1], close[index + 1]) - min(open[index + 1], close[index + 1])

    if today_lower_line * k > today_upper_line:
        return
    if yesterday_lower_line * k > yesterday_upper_line:
        return
    if tomorrow_lower_line * k > tomorrow_upper_line:
        return
    if today_upper_line < today_body:
        return
    if yesterday_upper_line < yesterday_body:
        return
    if tomorrow_upper_line < tomorrow_body:
        return

    results[index][0] = 0
    results[index][1] = index
