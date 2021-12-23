from result import Result
import talib as ta


def morning_star(klines,k=0.0005):
    days = 12
    ma = ta.MA(klines['close'], timeperiod=days)
    results = []

    for index in range(len(klines)):
        if index < days:
            continue
        today = klines.iloc[index]

        if today['open'] * (1+k) > today['close'] > today['open'] * (1-k):

            satisfy_ma = True
            # 连续days天ma趋势线都是下跌形态
            for ma_index in range(days):
                if ma_index == 0:
                    continue
                satisfy_ma = ma[index] < ma[index - ma_index]
                if not satisfy_ma:
                    break;
            if satisfy_ma:
                satisfy_low = True;
                for body_index in range(days):
                    if body_index == 0:
                        continue
                    satisfy_low = today['open'] < min(klines.iloc[index - body_index]['close'],
                                                      klines.iloc[index - body_index]['open'])
                    if not satisfy_low:
                        break;
                if satisfy_low:
                    results.append(
                        Result(today['code'], 'BUY', today['close'], today['time_key'], 'morning_star').get_dict())
    return results

def evening_star(klines,k=0.0005):
    days = 12
    ma = ta.MA(klines['close'], timeperiod=days)
    results = []

    for index in range(len(klines)):
        if index < days:
            continue
        today = klines.iloc[index]

        if today['open'] * (1+k) > today['close'] > today['open'] * (1-k):

            satisfy_ma = True
            # 连续days天ma趋势线都是上涨形态
            for ma_index in range(days):
                if ma_index == 0:
                    continue
                satisfy_ma = ma[index] > ma[index - ma_index]
                if not satisfy_ma:
                    break;
            if satisfy_ma:
                satisfy_high = True;
                for body_index in range(days):
                    if body_index == 0:
                        continue
                    satisfy_high = today['open'] > max(klines.iloc[index - body_index]['close'],
                                                       klines.iloc[index - body_index]['open'])
                    if not satisfy_high:
                        break;
                if satisfy_high:
                    results.append(
                        Result(today['code'], 'SELL', today['close'], today['time_key'], 'evening_star').get_dict())

    return results