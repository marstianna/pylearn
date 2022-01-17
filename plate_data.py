import time
import pandas as pd
import futu as ft

import main
import util
from result import Result
from test import test_flat, test_impale, test_hammer, test_swallow, test_star, test_pregnant


def test():
    quote_ctx = ft.OpenQuoteContext()  # 创建行情对象
    market = ft.Market.HK
    RET_OK, subplate_frame_table = quote_ctx.get_plate_list(market,ft.Plate.INDUSTRY)
    plate_ids = subplate_frame_table['plate_id']
    results = []
    # for plate_id in plate_ids.values:
    #     print("-----------------start:" + plate_id + "-------------------")
    #     RET_OK, kline_frame_table, next_page_req_key = quote_ctx.request_history_kline(code=market+"."+plate_id)
    #     tmp = []
    #     tmp.extend(test_flat(kline_frame_table))
    #     tmp.extend(test_impale(kline_frame_table))
    #     tmp.extend(test_hammer(kline_frame_table))
    #     tmp.extend(test_swallow(kline_frame_table))
    #     tmp.extend(test_star(kline_frame_table))
    #     tmp.extend(test_pregnant(kline_frame_table))
    #     # compute_profit(ma)
    #     # results.extend(util.filter_today(tmp))
    #     results.extend(util.filter_day(tmp, '2022-01-05'))
    # t = pd.DataFrame(results, columns=Result.columns)
    # values = t.sort_values(by=['stock_code', 'date'])
    print(subplate_frame_table)
    quote_ctx.close()

if __name__ == '__main__':
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.max_rows', 10000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.width', 1000)
    start = time.time()
    test()
    print(int(time.time() - start))