import talib
import pandas as pd

def kdj(klines):
    dw = pd.DataFrame()

    # KDJ 值对应的函数是 STOCH
    dw['slowk'], dw['slowd'] = talib.STOCH(klines['high'].values,
                                           klines['low'].values,
                                           klines['close'].values,
                                           fastk_period=9,
                                           slowk_period=3,
                                           slowk_matype=0,
                                           slowd_period=3,
                                           slowd_matype=0)

    # 求出J值，J = (3*K)-(2*D)
    dw['slowj'] = list(map(lambda x,y: 3*x-2*y, dw['slowk'], dw['slowd']))
    dw.index = range(len(dw))
    return dw['slowk'], dw['slowd'],dw['slowj']