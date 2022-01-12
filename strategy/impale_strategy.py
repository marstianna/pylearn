from result import Result
import talib as ta

from strategy.score import impale_score


def upper_impale(klines, days=7):
    ma = ta.MA(klines['close'], timeperiod=days)
    results = []

    for index in range(len(klines)):
        if index < days:
            continue
        today = klines.iloc[index]
        yesterday = klines.iloc[index - 1]

        if yesterday['open'] < yesterday['close']:
            continue
        if today['open'] > today['close']:
            continue;

        if max(yesterday['open'], yesterday['close']) > today['close'] > (
                0.5 * (yesterday['open'] + yesterday['close'])) \
                and today['open'] < yesterday['low']:

            satisfy_ma = True
            # 连续days天ma趋势线都是下跌形态
            for ma_index in range(days):
                satisfy_ma = ma[index - ma_index] < ma[index - ma_index - 1]
                if not satisfy_ma:
                    break
            if satisfy_ma:
                satisfy_low = True;
                for body_index in range(days):
                    if body_index == 0:
                        continue
                    satisfy_low = today['open'] < min(klines.iloc[index - body_index]['close'],
                                                      klines.iloc[index - body_index]['open'])
                    if not satisfy_low:
                        break
                if satisfy_low:
                    score = impale_score.upper_impale_score(index, klines)
                    results.append(
                        Result(today['code'], 'BUY', today['close'], today['time_key'], 'upper_impale',
                               intension=score).get_dict())
    return results


def lower_impale(klines, days=7):
    ma = ta.MA(klines['close'], timeperiod=days)
    results = []

    for index in range(len(klines)):
        if index < days:
            continue
        today = klines.iloc[index]
        yesterday = klines.iloc[index - 1]

        if yesterday['open'] > yesterday['close']:
            continue
        if today['open'] < today['close']:
            continue

        if today['open'] > yesterday['high'] \
                and (0.5 * (yesterday['open'] + yesterday['close'])) > today['close'] > min(yesterday['open'],
                                                                                            yesterday['close']):

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
                    satisfy_high = today['open'] > max(klines.iloc[index - body_index]['close'],
                                                       klines.iloc[index - body_index]['open'])
                    if not satisfy_high:
                        break
                if satisfy_high:
                    score = impale_score.lower_impale_score(index, klines)
                    results.append(
                        Result(today['code'], 'SELL', today['close'], today['time_key'], 'lower_impale',
                               intension=score).get_dict())

    return results
