import talib as ta
import pandas as pd

# 当前upper和lower都存在一个如果实体(body)过小的情况下会导致命中逻辑不够精确的问题
import constant
from result import Result
from strategy.score import hammer_score


def define_upper_hammer(klines, k=0.4):
    hammers = []
    ma = ta.MA(klines['close'], timeperiod=5)
    for index in range(len(klines)):
        if index < 5:
            continue
        # 实体长度
        body = 0
        # 上影线
        upper_line = 0
        # 下影线
        lower_line = 0
        if klines.iloc[index]['open'] < klines.iloc[index]['close']:
            body = klines.iloc[index]['open'] - klines.iloc[index]['close']
            upper_line = klines.iloc[index]['high'] - klines.iloc[index]['open']
            lower_line = klines.iloc[index]['close'] - klines.iloc[index]['low']
        else:
            body = klines.iloc[index]['close'] - klines.iloc[index]['open']
            upper_line = klines.iloc[index]['high'] - klines.iloc[index]['close']
            lower_line = klines.iloc[index]['open'] - klines.iloc[index]['low']
            # 上影线是实体的2倍,下影线是上影线的k,当前设定k=0.4
        if lower_line > 2 * body and upper_line < k * lower_line:
            # 上涨锤子线出现之前的MA5连续5天下跌,
            if ma[index - 5] > ma[index - 4] and ma[index - 4] > ma[index - 3] and ma[index - 3] > ma[index - 2] and ma[
                index - 2] > ma[index - 1] and ma[index - 1] > ma[index]:
                # 锤子线的实体不能超过前一天的实体
                if max(klines.iloc[index]['close'], klines.iloc[index]['open']) < max(klines.iloc[index - 1]['close'],
                                                                                      klines.iloc[index - 1]['open']):
                    # 锤子线的最低点要低于前5天的最低价,且下影线越长约好
                    if klines.iloc[index]['low'] < klines.iloc[index - 1]['low'] and klines.iloc[index]['low'] < \
                            klines.iloc[index - 2]['low'] and klines.iloc[index]['low'] < klines.iloc[index - 3][
                        'low'] and klines.iloc[index]['low'] < klines.iloc[index - 4]['low'] and klines.iloc[index][
                        'low'] < klines.iloc[index - 5]['low']:
                        score = hammer_score.hammer_score(index, klines)
                        hammers.append(Result(klines.iloc[index]['code'], 'BUY', klines.iloc[index]['close'],
                                              klines.iloc[index]['time_key'], 'hammer', intension=score))
    return hammers


def define_lower_hammer(klines, k=0.3):
    hammers = []
    days = constant.day_mid
    ma = ta.MA(klines['close'], timeperiod=days)
    for index in range(len(klines)):
        if index < days:
            continue
        # 实体长度
        body = 0
        # 上影线
        upper_line = 0
        # 下影线
        lower_line = 0
        if klines.iloc[index]['open'] < klines.iloc[index]['close']:
            body = klines.iloc[index]['open'] - klines.iloc[index]['close']
            upper_line = klines.iloc[index]['high'] - klines.iloc[index]['open']
            lower_line = klines.iloc[index]['close'] - klines.iloc[index]['low']
        else:
            body = klines.iloc[index]['close'] - klines.iloc[index]['open']
            upper_line = klines.iloc[index]['high'] - klines.iloc[index]['close']
            lower_line = klines.iloc[index]['open'] - klines.iloc[index]['low']
            # 上影线是实体的2倍,下影线是上影线的k,当前设定k=0.4
        if lower_line > 2 * body and upper_line < k * lower_line:
            satisfy_ma = True
            # 连续12天ma趋势线都是上涨形态
            for ma_index in range(days):
                if ma_index == 0:
                    continue
                satisfy_ma = ma[index] > ma[index - ma_index]
                if not satisfy_ma:
                    break
            if satisfy_ma:
                if max(klines.iloc[index]['close'], klines.iloc[index]['open']) > max(klines.iloc[index - 1]['close'],
                                                                                      klines.iloc[index - 1]['open']):
                    satisfy_high = True
                    for body_index in range(days):
                        if body_index == 0:
                            continue
                        satisfy_high = klines.iloc[index]['high'] > max(klines.iloc[index - body_index]['close'],
                                                                        klines.iloc[index - body_index]['open'])
                        if not satisfy_high:
                            break
                    if satisfy_high:
                        score = hammer_score.hammer_score(index, klines)
                        hammers.append(Result(klines.iloc[index]['code'], 'SELL', klines.iloc[index]['close'],
                                              klines.iloc[index]['time_key'], 'hammer', intension=score))
    return hammers


def handstand_lower_hammer(klines, k=3):
    hammers = []
    days = 12
    ma = ta.MA(klines['close'], timeperiod=days)
    for index in range(len(klines)):
        if index < days:
            continue

        today = klines.iloc[index]

        today_upper_line = today['high'] - max(today['open'], today['close'])
        today_lower_line = min(today['open'], today['close']) - today['low']
        today_body = max(today['open'], today['close']) - min(today['open'], today['close'])

        if today_lower_line * k < today_upper_line and today_upper_line > today_body:
            satisfy_ma = True
            for ma_index in range(days):
                if ma_index == 0:
                    continue
                satisfy_ma = ma[index] > ma[index - ma_index]
                if not satisfy_ma:
                    break
            if satisfy_ma:
                satisfy_high = True
                for body_index in range(days):
                    if body_index == 0:
                        continue
                    satisfy_high = klines.iloc[index]['high'] > klines.iloc[index - body_index]['high']
                    if not satisfy_high:
                        break
                if satisfy_high:
                    score = hammer_score.handstand_hammer_score(index, klines)
                    hammers.append(Result(klines.iloc[index]['code'], 'SELL', klines.iloc[index]['close'],
                                          klines.iloc[index]['time_key'], 'handstand_hammer',
                                          intension=score))
    return hammers
