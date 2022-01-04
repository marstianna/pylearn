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


def get_result_from_cuda(klines):
    item = [-1, 0, 0]  # [0]=action,[1]=index,[2]=score
    results = [item] * len(klines)
    x = 32
    ceil = math.ceil(len(klines) / x)
    ma_5 = talib.MA(klines['close'], timeperiod=5).values
    ma_7 = talib.MA(klines['close'], timeperiod=7).values
    ma_12 = talib.MA(klines['close'], timeperiod=12).values

    strategies = 14
    stream_list = list()
    for i in range(0, strategies):
        stream_list.append(cuda.stream())

    gpu_results_flat_bottom = cuda.to_device(results.copy(), stream=stream_list[0])
    flat_strategy_cuda.flat_bottom[x, ceil, stream_list[0]](klines['open'].values, klines['close'].values,
                                                            klines['high'].values,
                                                            klines['low'].values, ma_5,
                                                            gpu_results_flat_bottom, 5, 0.005)

    gpu_results_flat_head = cuda.to_device(results.copy(), stream=stream_list[1])
    flat_strategy_cuda.flat_head[x, ceil, stream_list[1]](klines['open'].values, klines['close'].values,
                                                          klines['high'].values,
                                                          klines['low'].values, ma_5,
                                                          gpu_results_flat_head, 5, 0.005)

    gpu_results_lower_swallow_upper = cuda.to_device(results.copy(), stream=stream_list[2])
    swallow_strategy_cuda.lower_swallow_upper[x, ceil, stream_list[2]](klines['open'].values, klines['close'].values,
                                                                       klines['high'].values,
                                                                       klines['low'].values, ma_7,
                                                                       gpu_results_lower_swallow_upper)

    gpu_results_upper_swallow_lower = cuda.to_device(results.copy(), stream=stream_list[3])
    swallow_strategy_cuda.upper_swallow_lower[x, ceil, stream_list[3]](klines['open'].values, klines['close'].values,
                                                                       klines['high'].values,
                                                                       klines['low'].values, ma_7,
                                                                       gpu_results_upper_swallow_lower)

    gpu_results_define_lower_hammer = cuda.to_device(results.copy(), stream=stream_list[4])
    hammer_strategy_cuda.define_lower_hammer[x, ceil, stream_list[4]](klines['open'].values, klines['close'].values,
                                                                      klines['high'].values,
                                                                      klines['low'].values, ma_12,
                                                                      gpu_results_define_lower_hammer, 0.3)

    gpu_results_define_upper_hammer = cuda.to_device(results.copy(), stream=stream_list[5])
    hammer_strategy_cuda.define_upper_hammer[x, ceil, stream_list[5]](klines['open'].values, klines['close'].values,
                                                                      klines['high'].values,
                                                                      klines['low'].values, ma_12,
                                                                      gpu_results_define_upper_hammer, 0.4)

    gpu_results_handstand_lower_hammer = cuda.to_device(results.copy(), stream=stream_list[6])
    hammer_strategy_cuda.handstand_lower_hammer[x, ceil, stream_list[6]](klines['open'].values, klines['close'].values,
                                                                         klines['high'].values,
                                                                         klines['low'].values, ma_12,
                                                                         gpu_results_handstand_lower_hammer, 3)

    gpu_results_lower_impale = cuda.to_device(results.copy(), stream=stream_list[7])
    impale_strategy_cuda.lower_impale[x, ceil, stream_list[7]](klines['open'].values, klines['close'].values,
                                                               klines['high'].values,
                                                               klines['low'].values, ma_7, gpu_results_lower_impale, 7)

    gpu_results_upper_impale = cuda.to_device(results.copy(), stream=stream_list[8])
    impale_strategy_cuda.upper_impale[x, ceil, stream_list[8]](klines['open'].values, klines['close'].values,
                                                               klines['high'].values,
                                                               klines['low'].values, ma_7, gpu_results_upper_impale, 7)

    gpu_results_lower_pregnant = cuda.to_device(results.copy(), stream=stream_list[9])
    pregnant_strategy_cuda.lower_pregnant[x, ceil, stream_list[9]](klines['open'].values, klines['close'].values,
                                                                   klines['high'].values,
                                                                   klines['low'].values, ma_5,
                                                                   gpu_results_lower_pregnant, 5, 3)

    gpu_results_upper_pregnant = cuda.to_device(results.copy(), stream=stream_list[10])
    pregnant_strategy_cuda.upper_pregnant[x, ceil, stream_list[10]](klines['open'].values, klines['close'].values,
                                                                    klines['high'].values,
                                                                    klines['low'].values, ma_5,
                                                                    gpu_results_upper_pregnant, 5, 3)

    gpu_results_morning_star = cuda.to_device(results.copy(), stream=stream_list[11])
    star_strategy_cuda.morning_star[x, ceil, stream_list[11]](klines['open'].values, klines['close'].values,
                                                              klines['high'].values,
                                                              klines['low'].values, ma_5, gpu_results_morning_star)

    gpu_results_evening_star = cuda.to_device(results.copy(), stream=stream_list[12])
    star_strategy_cuda.evening_star[x, ceil, stream_list[12]](klines['open'].values, klines['close'].values,
                                                              klines['high'].values,
                                                              klines['low'].values, ma_5, gpu_results_evening_star)

    gpu_results_falling_star = cuda.to_device(results.copy(), stream=stream_list[13])
    star_strategy_cuda.falling_star[x, ceil, stream_list[13]](klines['open'].values, klines['close'].values,
                                                              klines['high'].values,
                                                              klines['low'].values, ma_5, gpu_results_falling_star)

    cuda.synchronize()
    results_from_gpu = []

    from_gpu_flat_bottom = gpu_results_flat_bottom.copy_to_host(stream=stream_list[0])
    results_from_gpu.extend(convert_results(from_gpu_flat_bottom, 'flat_bottom', klines))

    from_gpu_flat_head = gpu_results_flat_head.copy_to_host(stream=stream_list[1])
    results_from_gpu.extend(convert_results(from_gpu_flat_head, 'flat_head', klines))

    from_gpu_lower_swallow_upper = gpu_results_lower_swallow_upper.copy_to_host(stream=stream_list[2])
    results_from_gpu.extend(convert_results(from_gpu_lower_swallow_upper, 'lower_swallow_upper', klines))

    from_gpu_upper_swallow_lower = gpu_results_upper_swallow_lower.copy_to_host(stream=stream_list[3])
    results_from_gpu.extend(convert_results(from_gpu_upper_swallow_lower, 'upper_swallow_lower', klines))

    from_gpu_define_lower_hammer = gpu_results_define_lower_hammer.copy_to_host(stream=stream_list[4])
    results_from_gpu.extend(convert_results(from_gpu_define_lower_hammer, 'define_lower_hammer', klines))

    from_gpu_define_upper_hammer = gpu_results_define_upper_hammer.copy_to_host(stream=stream_list[5])
    results_from_gpu.extend(convert_results(from_gpu_define_upper_hammer, 'define_upper_hammer', klines))

    from_gpu_handstand_lower_hammer = gpu_results_handstand_lower_hammer.copy_to_host(stream=stream_list[6])
    results_from_gpu.extend(convert_results(from_gpu_handstand_lower_hammer, 'handstand_lower_hammer', klines))

    from_gpu_lower_impale = gpu_results_lower_impale.copy_to_host(stream=stream_list[7])
    results_from_gpu.extend(convert_results(from_gpu_lower_impale, 'lower_impale', klines))

    from_gpu_upper_impale = gpu_results_upper_impale.copy_to_host(stream=stream_list[8])
    results_from_gpu.extend(convert_results(from_gpu_upper_impale, 'upper_impale', klines))

    from_gpu_lower_pregnant = gpu_results_lower_pregnant.copy_to_host(stream=stream_list[9])
    results_from_gpu.extend(convert_results(from_gpu_lower_pregnant, 'lower_pregnant', klines))

    from_gpu_upper_pregnant = gpu_results_upper_pregnant.copy_to_host(stream=stream_list[10])
    results_from_gpu.extend(convert_results(from_gpu_upper_pregnant, 'upper_pregnant', klines))

    from_gpu_morning_star = gpu_results_morning_star.copy_to_host(stream=stream_list[11])
    results_from_gpu.extend(convert_results(from_gpu_morning_star, 'morning_star', klines))

    from_gpu_evening_star = gpu_results_evening_star.copy_to_host(stream=stream_list[12])
    results_from_gpu.extend(convert_results(from_gpu_evening_star, 'evening_star', klines))

    from_gpu_falling_star = gpu_results_falling_star.copy_to_host(stream=stream_list[13])
    results_from_gpu.extend(convert_results(from_gpu_falling_star, 'falling_star', klines))

    return results_from_gpu


def convert_results(from_gpu_results, method, klines):
    results = []
    for res in from_gpu_results:
        if res[0] == -1:
            continue
        today = klines.iloc[res[1]]
        results.append(
            Result(today['code'], 'BUY' if res[0] == 1 else 'SELL', today['close'], today['time_key'], method, 0,
                   res[2], 0).get_dict())
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
