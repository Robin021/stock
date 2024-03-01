# from bitarray import bitarray
# from random import randint
import sys
import redis
import asyncio
import settings
import pandas as pd
import numpy as np
import tushare  as ts


client = redis.Redis(host='localhost', port=6379,db=0)

name_of_group_a = "Buy"
global stocks_dict
global stocks
settings.init()
stocks_d = pd.read_csv(settings.config['selected_file'], dtype=str)
stocks_d.code = (stocks_d['code']).astype(str)
stocks_d.maxp5 = (stocks_d['maxp5']).astype(float)

stocks_dict = stocks_d.set_index('code')['maxp5'].to_dict()
# print("stocks_dict", p(stocks_dict))
stocks_dataframe = pd.read_csv(settings.config['selected_file'], dtype=str)
stocks = stocks_dataframe.values.tolist()
task_list_add = []
# print(stocks_d.code)
stock_code = []
def process():
    
    asyncio.run(add())
    # asyncio.run(remove())

async def add_calc(stock):
    df = ts.get_realtime_quotes(stock)
   
    # print(float(df[['pre_close'][0]]),float(df[['price'][0]]),stocks_dict[stock])
    p_change = (float(df[['price'][0]]) - float(df[['pre_close'][0]]))/float(df[['pre_close'][0]])*100
    p_change = '%.2f' % p_change
    # limit_price = calc_limit_price(df[['price'][0]])
    # print(p_change)
    if float(df[['price'][0]]) > stocks_dict[stock]:
        print("p_change",p_change,type(p_change))
        if float(p_change) >= 9:
            print(stock,p_change)
            client.set(stock,p_change)

        

async def add():
    # print(len(stocks_d.code))
    for i in range(len(stocks_d.code)):
        task = asyncio.create_task(
                add_calc(stocks_d.code.iloc[i]))
        task_list_add.append(task)
        # print(task_list_add)

    # asyncio.run(task_list_add)
    done, pending = await asyncio.wait(task_list_add, timeout=None)

async def read_from_tushare(stocks_d):
    df = ts.get_realtime_quotes(stocks_d)
    return df

async def calc_limit_price(pre_close):
    if pre_close == 0:
        return 0

    limit = pre_close + pre_close * 0.1
    limit = '%.2f' % limit
    # print(limit)
    return float(limit)


# asyncio def remove():
#     client.remove()

process()
