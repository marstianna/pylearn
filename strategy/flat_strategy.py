import talib as ta
import math

from result import Result


#平头顶
def flat_head(klines,days=5,k=0.005):
    ma = ta.MA(klines['close'], timeperiod=days)
    results = []

    for index in range(len(klines)):
        if index < days:
            continue
        today = klines.iloc[index]
        yesterday = klines.iloc[index - 1]

        if today['high'] * (1 + k) > yesterday['high'] > today['high'] * (1 - k):
            satisfy_ma = True
            # 连续days天ma趋势线都是上涨形态
            for ma_index in range(days):
                satisfy_ma = ma[index - ma_index] > ma[index - ma_index - 1]
                if not satisfy_ma:
                    break;
            if satisfy_ma:
                satisfy_low = True;
                highest = max(today['high'],yesterday['high'])
                for idx in range(days):
                    if idx <= 1:
                        continue;
                    if highest < klines.iloc[index - idx]['high']:
                        satisfy_low = False
                        break
                if satisfy_low:
                    results.append(
                        Result(today['code'], 'SELL', today['close'], today['time_key'], 'flat_head').get_dict())
    return results


def flat_bottom(klines,days=5,k=0.005):
    ma = ta.MA(klines['close'], timeperiod=days)
    results = []

    for index in range(len(klines)):
        if index < days:
            continue
        today = klines.iloc[index]
        yesterday = klines.iloc[index - 1]

        if today['low'] * (1 + k) > yesterday['low'] > today['low'] * (1 - k):
            satisfy_ma = True
            # 连续days天ma趋势线都是上涨形态
            for ma_index in range(days):
                satisfy_ma = ma[index - ma_index] < ma[index - ma_index - 1]
                if not satisfy_ma:
                    break;
            if satisfy_ma:
                satisfy_low = True;
                lowest = min(today['low'], yesterday['low'])
                for idx in range(days):
                    if idx <= 1:
                        continue;
                    if lowest > klines.iloc[index - idx]['low']:
                        satisfy_low = False
                        break
                if satisfy_low:
                    results.append(
                        Result(today['code'], 'BUY', today['close'], today['time_key'], 'flat_bottom').get_dict())
    return results