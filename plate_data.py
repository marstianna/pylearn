import time
import pandas as pd
import futu as ft

import main
from result import Result


def test():
    quote_ctx = ft.OpenQuoteContext()  # 创建行情对象
    plate_list = quote_ctx.get_plate_list(ft.Market.SH,ft.Plate.INDUSTRY)
    print(plate_list)
    quote_ctx.close()

if __name__ == '__main__':
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.max_rows', 10000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.width', 1000)
    start = time.time()
    test()
    print(int(time.time() - start))