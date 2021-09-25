# -*- encoding: UTF-8 -*-

import talib as tl
import pandas as pd
import logging
import push

#市值2000-50亿
#价格>5
#5天的平均成交量
#昨收 不涨停
#股价创近10天新高

# 最后一个交易日收市价为指定区间内最高价


def results_maxp5(code_name, data, end_date=None, threshold=5):

    max_price = 0
    if end_date is not None:
        mask = (data['date'] <= end_date)
        data = data.loc[mask]
    if data is None:
        return False
    data = data.tail(n=threshold)
    if len(data) < threshold:
        return False
    for index, row in data.iterrows():
        if row['high'] > max_price:
            max_price = float(row['high'])
    return max_price


def calc_limit_price(pre_close):
    if pre_close == 0:
        return 0

    limit = pre_close + pre_close*0.1
    limit = '%.2f' % limit
    # print(limit)
    return float(limit)

def check(code_name, data, end_date=None, threshold=10):
    origin_data = data
    if len(data) < threshold:
        logging.debug("{0}:样本小于{1}天...\n".format(code_name, threshold))
        return
    # data['ma60'] = pd.Series(
    #     tl.MA(data['close'].values, 60), index=data.index.values)

    begin_date = data.iloc[0].date
    if end_date is not None:
        if end_date < begin_date:  # 该股票在end_date时还未上市
            logging.debug("{}在{}时还未上市".format(code_name, end_date))
            return False


    last_close = data.iloc[-1]['close']
    if last_close < 5:
        return False

    if data.iloc[-1]['p_change'] >= calc_limit_price(last_close):
        return False

    #  市值2000-50亿
    # mktcap = data.iloc[-1]['mktcap']
    # if code_name[3] > 22222222 or code_name[3] < 4545450:
    #     return False

    # if not check_enter(code_name, data, end_date=None, threshold=10):
    #     return False
    if 'ST' in code_name[1]:
        return False
    # print(data.iloc[-1]['code'])
    # if data.iloc[-1]['code'].startswith('^68'):
    #     return False
    
    # if data.iloc[-1]['code'].startswith('^300'):
    #     return False
    # push.strategy("股票{0} ".format(code_name))
    return True
