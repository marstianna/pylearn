from result import Result
import talib as ta


def upper_pregnant(klines,days=5,k=3):
    ma = ta.MA(klines['close'], timeperiod=days)
    results = []
    for index in range(len(klines)):
        if index < days:
            continue
        today = klines.iloc[index]
        yesterday = klines.iloc[index - 1]

        today_body = max(today['open'],today['close']) - min(today['open'],today['close'])
        yesterday_body = max(yesterday['open'], yesterday['close']) - min(yesterday['open'], yesterday['close'])

        if yesterday['open'] < yesterday['close']:
            continue

        if yesterday_body > today_body * k and min(yesterday['open'], yesterday['close']) < min(today['open'],today['close']) and  max(yesterday['open'], yesterday['close']) > max(today['open'],today['close']):
            satisfy_ma = True
            # 连续days天ma趋势线都是下跌形态
            for ma_index in range(days):
                satisfy_ma = ma[index - ma_index] < ma[index - ma_index - 1]
                if not satisfy_ma:
                    break;
            if satisfy_ma:
                results.append(
                    Result(today['code'], 'BUY', today['close'], today['time_key'], 'upper_pregnant'))
    return results

def lower_pregnant(klines,days=5,k=3):
    ma = ta.MA(klines['close'], timeperiod=days)
    results = []

    for index in range(len(klines)):
        if index < days:
            continue
        today = klines.iloc[index]
        yesterday = klines.iloc[index - 1]

        today_body = max(today['open'], today['close']) - min(today['open'], today['close'])
        yesterday_body = max(yesterday['open'], yesterday['close']) - min(yesterday['open'], yesterday['close'])

        if yesterday['open'] > yesterday['close']:
            continue

        if yesterday_body > today_body * k and min(yesterday['open'], yesterday['close']) < min(today['open'],today['close']) and  max(yesterday['open'], yesterday['close']) > max(today['open'],today['close']):
            satisfy_ma = True
            # 连续days天ma趋势线都是上涨形态
            for ma_index in range(days):
                satisfy_ma = ma[index - ma_index] > ma[index - ma_index - 1]
                if not satisfy_ma:
                    break;
            if satisfy_ma:
                results.append(
                    Result(today['code'], 'SELL', today['close'], today['time_key'], 'lower_pregnant'))
    return results