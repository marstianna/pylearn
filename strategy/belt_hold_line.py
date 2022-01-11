import talib as ta

from result import Result


def upper_belt_hold_line(klines, k_upper_shadow_line=0.005, k_lower_shadow_line=0.005):
    days = 7
    ma = ta.MA(klines['close'], timeperiod=days)
    results = []

    for index in range(len(klines)):
        if index < days:
            continue
        today = klines.iloc[index]

        if today['close'] < today['open']:
            continue

        if today['open'] * (1+0.05) > today['close']:
            continue

        if today['open'] * (1 - k_lower_shadow_line) <= today['low'] and today['close'] * (1 + k_upper_shadow_line) >= \
                today['high']:
            satisfy_ma = True
            # 连续days天ma趋势线都是下跌形态
            for ma_index in range(days):
                if ma_index == 0:
                    continue
                satisfy_ma = ma[index - ma_index] < ma[index - ma_index - 1]
                if not satisfy_ma:
                    break
            if satisfy_ma:
                satisfy_low = True
                for body_index in range(days):
                    if body_index == 0:
                        continue
                    satisfy_low = today['low'] < klines.iloc[index - body_index]['low']
                    if not satisfy_low:
                        break
                if satisfy_low:
                    results.append(
                        Result(today['code'], 'BUY', today['close'], today['time_key'],
                               'upper_belt_hold_line').get_dict())
    return results


def lower_belt_hold_line(klines, k_upper_shadow_line=0.005, k_lower_shadow_line=0.005):
    days = 7
    ma = ta.MA(klines['close'], timeperiod=days)
    results = []

    for index in range(len(klines)):
        if index < days:
            continue
        today = klines.iloc[index]

        if today['open'] < today['close']:
            continue

        if today['open'] * (1-0.05) < today['close']:
            continue

        if today['close'] * (1 - k_lower_shadow_line) <= today['low'] and today['open'] * (1 + k_upper_shadow_line) >= \
                today['high']:
            satisfy_ma = True
            # 连续days天ma趋势线都是上涨形态
            for ma_index in range(days):
                if ma_index == 0:
                    continue
                satisfy_ma = ma[index - ma_index] > ma[index - ma_index - 1]
                if not satisfy_ma:
                    break
            if satisfy_ma:
                satisfy_high = True
                for body_index in range(days):
                    if body_index == 0:
                        continue
                    satisfy_high = today['high'] > klines.iloc[index - body_index]['high']
                    if not satisfy_high:
                        break
                if satisfy_high:
                    results.append(Result(today['code'], 'SELL', today['close'], today['time_key'],
                                          'lower_belt_hold_line').get_dict())
    return results
