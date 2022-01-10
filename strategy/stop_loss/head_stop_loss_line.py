from indicator import calculate
from strategy.stop_loss import recall


def head_stop_loss_line(today_result, total_results, klines,timeperiod, recall_days=26, k=0.05):
    stop_loss_price = 0.0

    for k_idx in range(len(klines)):
        if klines.iloc[k_idx]['time_key'] == today_result['date']:

            # 第一优先级,如果有强力的反转信号,那么以对应所有图形的平均值为止损位
            buy = recall.recall_sell(klines.iloc[k_idx], total_results, recall_days)
            if buy != -1:
                stop_loss_price = buy * (1 + k)
                break;
            else:
                # 第二优先级,上涨压力线和之前计算的结果进行比较,取较小值作为止损线
                stop_loss_price = calculate.calculate_press_line(today_result,klines,timeperiod) * (1 + k)
                break

    today_result['stop_loss_line'] = stop_loss_price
