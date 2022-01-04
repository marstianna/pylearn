import math

import numpy
import pandas as pd
import futu as ft
import talib

from indicator import ma_strategy
import main
import util
from result import Result
from strategy.cuda import flat_strategy_cuda, hammer_strategy_cuda, swallow_strategy_cuda, impale_strategy_cuda, \
    star_strategy_cuda, pregnant_strategy_cuda
from numba import cuda
import time


def test_hammer(klines):
    result = hammer_strategy_cuda.define_upper_hammer(klines)
    result.extend(hammer_strategy_cuda.define_lower_hammer(klines))
    result.extend(hammer_strategy_cuda.handstand_lower_hammer(klines))
    return result


def test_swallow(klines):
    result = swallow_strategy_cuda.upper_swallow_lower(klines)
    result.extend(swallow_strategy_cuda.lower_swallow_upper(klines))
    return result


def test_impale(klines):
    upper_result = impale_strategy_cuda.upper_impale(klines)
    upper_result.extend(impale_strategy_cuda.lower_impale(klines))
    return upper_result


def test_star(klines):
    result = star_strategy_cuda.morning_star(klines)
    result.extend(star_strategy_cuda.evening_star(klines))
    result.extend(star_strategy_cuda.falling_star(klines))
    return result
    # print(pd.DataFrame(lower_result, columns=Result.columns))


def test_ma(klines):
    ma = []
    ma.extend(ma_strategy.multi_ma(klines, short_day=12, long_day=26))
    # ma.extend(ma_strategy.single_ma2(klines,days=26))
    # ma.extend(ma_strategy.single_ma(klines,days=26))
    compute_profit(ma)
    return ma


def test_pregnant(klines):
    result = pregnant_strategy_cuda.lower_pregnant(klines)
    result.extend(pregnant_strategy_cuda.upper_pregnant(klines))
    return result


def get_result_from_cuda(klines):
    item = [-1, 0, 0]  # [0]=action,[1]=index,[2]=score
    results = [item] * len(klines)
    x = 32
    ceil = math.ceil(len(klines) / x)
    ma_5 = talib.MA(klines['close'], timeperiod=5).values
    ma_7 = talib.MA(klines['close'], timeperiod=7).values
    ma_12 = talib.MA(klines['close'], timeperiod=12).values

    gpu_results_flat_bottom = cuda.to_device(results.copy())
    flat_strategy_cuda.flat_bottom[x, ceil](klines['open'].values, klines['close'].values, klines['high'].values,
                                            klines['low'].values, ma_5,
                                            gpu_results_flat_bottom, 5, 0.005)

    gpu_results_flat_head = cuda.to_device(results.copy())
    flat_strategy_cuda.flat_head[x, ceil](klines['open'].values, klines['close'].values, klines['high'].values,
                                          klines['low'].values, ma_5,
                                          gpu_results_flat_head, 5, 0.005)

    gpu_results_lower_swallow_upper = cuda.to_device(results.copy())
    swallow_strategy_cuda.lower_swallow_upper[x, ceil](klines['open'].values, klines['close'].values,
                                                       klines['high'].values,
                                                       klines['low'].values, ma_7, gpu_results_lower_swallow_upper)

    gpu_results_upper_swallow_lower = cuda.to_device(results.copy())
    swallow_strategy_cuda.upper_swallow_lower[x, ceil](klines['open'].values, klines['close'].values,
                                                       klines['high'].values,
                                                       klines['low'].values, ma_7, gpu_results_upper_swallow_lower)

    gpu_results_define_lower_hammer = cuda.to_device(results.copy())
    hammer_strategy_cuda.define_lower_hammer(klines['open'].values, klines['close'].values, klines['high'].values,
                                             klines['low'].values, ma_12, gpu_results_define_lower_hammer, 0.3)

    gpu_results_define_upper_hammer = cuda.to_device(results.copy())
    hammer_strategy_cuda.define_upper_hammer(klines['open'].values, klines['close'].values, klines['high'].values,
                                             klines['low'].values, ma_12, gpu_results_define_upper_hammer, 0.4)

    gpu_results_handstand_lower_hammer = cuda.to_device(results.copy())
    hammer_strategy_cuda.handstand_lower_hammer(klines['open'].values, klines['close'].values, klines['high'].values,
                                                klines['low'].values, ma_12, gpu_results_handstand_lower_hammer, 3)

    gpu_results_lower_impale = cuda.to_device(results.copy())
    impale_strategy_cuda.lower_impale(klines['open'].values, klines['close'].values, klines['high'].values,
                                                klines['low'].values, ma_7,gpu_results_lower_impale,7)

    gpu_results_upper_impale = cuda.to_device(results.copy())
    impale_strategy_cuda.upper_impale(klines['open'].values, klines['close'].values, klines['high'].values,
                                                klines['low'].values, ma_7,gpu_results_upper_impale,7)

    gpu_results_lower_pregnant = cuda.to_device(results.copy())
    pregnant_strategy_cuda.lower_pregnant(klines['open'].values, klines['close'].values, klines['high'].values,
                                                klines['low'].values, ma_5,gpu_results_lower_pregnant,5,3)

    gpu_results_upper_pregnant = cuda.to_device(results.copy())
    pregnant_strategy_cuda.upper_pregnant(klines['open'].values, klines['close'].values, klines['high'].values,
                                                klines['low'].values, ma_5,gpu_results_upper_pregnant,5,3)

    gpu_results_morning_star = cuda.to_device(results.copy())
    star_strategy_cuda.morning_star(klines['open'].values, klines['close'].values, klines['high'].values,
                                                klines['low'].values, ma_5,gpu_results_morning_star)

    gpu_results_evening_star = cuda.to_device(results.copy())
    star_strategy_cuda.evening_star(klines['open'].values, klines['close'].values, klines['high'].values,
                                                klines['low'].values, ma_5,gpu_results_evening_star)

    gpu_results_falling_star = cuda.to_device(results.copy())
    star_strategy_cuda.falling_star(klines['open'].values, klines['close'].values, klines['high'].values,
                                                klines['low'].values, ma_5,gpu_results_falling_star)

    cuda.synchronize()
    results_from_gpu = []
    from_gpu_flat_bottom = gpu_results_flat_bottom.copy_to_host()
    results_from_gpu.extend(convert_results(from_gpu_flat_bottom, 'flat_bottom', ma_5))

    from_gpu_flat_head = gpu_results_flat_head.copy_to_host()
    results_from_gpu.extend(convert_results(from_gpu_flat_head, 'flat_head', ma_5))

    from_gpu_lower_swallow_upper = gpu_results_lower_swallow_upper.copy_to_host()
    results_from_gpu.extend(convert_results(from_gpu_lower_swallow_upper, 'lower_swallow_upper', ma_5))

    from_gpu_upper_swallow_lower = gpu_results_upper_swallow_lower.copy_to_host()
    results_from_gpu.extend(convert_results(from_gpu_upper_swallow_lower, 'upper_swallow_lower', ma_5))

    from_gpu_define_lower_hammer = gpu_results_define_lower_hammer.copy_to_host()
    results_from_gpu.extend(convert_results(from_gpu_define_lower_hammer, 'define_lower_hammer', ma_5))

    from_gpu_define_upper_hammer = gpu_results_define_upper_hammer.copy_to_host()
    results_from_gpu.extend(convert_results(from_gpu_define_upper_hammer, 'define_upper_hammer', ma_5))

    from_gpu_handstand_lower_hammer = gpu_results_handstand_lower_hammer.copy_to_host()
    results_from_gpu.extend(convert_results(from_gpu_handstand_lower_hammer, 'handstand_lower_hammer', ma_5))

    from_gpu_lower_impale = gpu_results_lower_impale.copy_to_host()
    results_from_gpu.extend(convert_results(from_gpu_lower_impale, 'lower_impale', ma_5))

    from_gpu_upper_impale = gpu_results_upper_impale.copy_to_host()
    results_from_gpu.extend(convert_results(from_gpu_upper_impale, 'upper_impale', ma_5))

    from_gpu_lower_pregnant = gpu_results_lower_pregnant.copy_to_host()
    results_from_gpu.extend(convert_results(from_gpu_lower_pregnant, 'lower_pregnant', ma_5))

    from_gpu_upper_pregnant = gpu_results_upper_pregnant.copy_to_host()
    results_from_gpu.extend(convert_results(from_gpu_upper_pregnant, 'upper_pregnant', ma_5))

    from_gpu_morning_star = gpu_results_morning_star.copy_to_host()
    results_from_gpu.extend(convert_results(from_gpu_morning_star, 'morning_star', ma_5))

    from_gpu_evening_star = gpu_results_evening_star.copy_to_host()
    results_from_gpu.extend(convert_results(from_gpu_evening_star, 'evening_star', ma_5))

    from_gpu_falling_star = gpu_results_falling_star.copy_to_host()
    results_from_gpu.extend(convert_results(from_gpu_falling_star, 'falling_star', ma_5))

    return results_from_gpu


def convert_results(from_gpu_results, method, klines):
    results = []
    for res in from_gpu_results:
        if res[0] == -1:
            continue
        today = klines.iloc[res[1]]
        results.append(
            Result(today['code'], 'BUY' if res[0] == 1 else 'SELL', today['close'], today['time_key'], method, 0, res[2], 0).get_dict())
    return results


def test_group():
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.max_rows', 10000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.width', 1000)
    quote_ctx = ft.OpenQuoteContext()  # 创建行情对象
    RET_OK, ret_frame = quote_ctx.get_user_security("target")
    results = []
    for code in ret_frame['code']:
        RET_OK, kline_frame_table, next_page_req_key = quote_ctx.request_history_kline(code=code)
        results.extend(get_result_from_cuda(kline_frame_table))
    t = pd.DataFrame(results, columns=Result.columns)
    values = t.sort_values(by=['stock_code', 'date'])
    print(values)
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
    start = time.time()
    test_group()
    print(int(time.time() - start))
