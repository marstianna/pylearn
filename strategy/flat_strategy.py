import talib as ta
import math

from result import Result


#平头顶
def flat_head(klines,days=7,k=0.005):
    ma = ta.MA(klines['close'], timeperiod=days)
    results = []

    for index in range(len(klines)):
        if index < days:
            continue
        today = klines.iloc[index]
        yesterday = klines.iloc[index - 1]

        # 昨天必须是一根大阳线
        if yesterday['open'] > yesterday['close']:
            continue
        # 今天必须是一根阴线
        if today['open'] < today['close']:
            continue

        if today['close'] < min(yesterday['open'],yesterday['close']):
            continue

        yesterday_upper_line = yesterday['high'] - max(yesterday['open'], yesterday['close'])
        yesterday_lower_line = min(yesterday['open'], yesterday['close']) - yesterday['low']
        yesterday_body = max(yesterday['open'], yesterday['close']) - min(yesterday['open'], yesterday['close'])

        if yesterday_body < yesterday_upper_line or yesterday_body < yesterday_lower_line:
            continue

        if today['high'] * (1 + k) > yesterday['high'] > today['high'] * (1 - k) or yesterday['high'] * (1 + k) > today['high'] > yesterday['high'] * (1 - k):
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


def flat_bottom(klines,days=7,k=0.005):
    ma = ta.MA(klines['close'], timeperiod=days)
    results = []

    for index in range(len(klines)):
        if index < days:
            continue
        today = klines.iloc[index]
        yesterday = klines.iloc[index - 1]

        # 昨天必须是一根大阴线
        if yesterday['open'] < yesterday['close']:
            continue
        # 今天必须是一根阳线
        if today['open'] > today['close']:
            continue

        if today['close'] > max(yesterday['open'], yesterday['close']):
            continue

        yesterday_upper_line = yesterday['high'] - max(yesterday['open'], yesterday['close'])
        yesterday_lower_line = min(yesterday['open'], yesterday['close']) - yesterday['low']
        yesterday_body = max(yesterday['open'], yesterday['close']) - min(yesterday['open'], yesterday['close'])

        if yesterday_body < yesterday_upper_line or yesterday_body < yesterday_lower_line:
            continue

        if today['low'] * (1 + k) > yesterday['low'] > today['low'] * (1 - k) or yesterday['low'] * (1 + k) > today['low'] > yesterday['low'] * (1 - k):
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