import talib as ta

from result import Result

#吞没形态还需要考虑命中当天的成交量的情况,如果出现对应的放量,那么认为形态有效

def upper_swallow_lower(klines):
    days = 26
    ma = ta.MA(klines['close'], timeperiod=days)
    results=[]

    for index in range(len(klines)):
        if index < days:
            continue
        today = klines.iloc[index]
        yesterday = klines.iloc[index - 1]

        if today['close'] > max(yesterday['open'],yesterday['close']) and today['open'] < min(yesterday['open'],yesterday['close']):

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
                    results.append(Result(today['code'],'BUY',today['close'],today['time_key'],'swallow').get_dict())
    return results

def lower_swallow_upper(klines):
    days = 26
    ma = ta.MA(klines['close'], timeperiod=days)
    results = []

    for index in range(len(klines)):
        if index < days:
            continue
        today = klines.iloc[index]
        yesterday = klines.iloc[index - 1]

        if today['open'] > max(yesterday['open'], yesterday['close']) and today['close'] < min(yesterday['open'],
                                                                                               yesterday['close']):

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
                    results.append(Result(today['code'],'SELL',today['close'],today['time_key'],'swallow').get_dict())

    return results