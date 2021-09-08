#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author shen.charles@hotmail.com

import time
import subprocess
import pandas as pd
import requests
import prettytable
import settings
import concurrent.futures
import math

def add_market_code(x):
    y = '0.' + x
    if x.startswith('6'):
        y = '1.' + x
    return y

    # f2最新价 f3涨跌幅 f4涨跌额 f5成交量 f6成交额 f7振幅
    # f8换手率 f12 代码  f14 名称  f15最高价  f16最低  f17今开 f18昨收  f23 市净率,f10量比 f9市盈率 f20总市值
    
def get_data(stock_codes):
    stock_codes = list(map(add_market_code, stock_codes))
    stock_codes = ','.join(stock_codes)

    endpoint = 'http://push2.eastmoney.com/api/qt/ulist.np/get'
    var1 = '?fields=f2,f3,f14,f12,f13,f19,f20,f10'
    var2 = '&invt=2&fltt=2&fid=f3'
    var3 = '&ut=bd1d9ddb04089700cf9c27f6f7426281&cb=&secids='
    url = '{0}{1}{2}{3}{4}'.format(endpoint, var1, var2, var3, stock_codes)
    # print(url)
    response = requests.get(url)
    data = response.json()
    return data['data']['diff']


def speak(text):
    text = text.replace('-', '负').replace('.', '点')
    cmd = 'espeak -vzh {}'.format(text)
    subprocess.call(cmd, shell=True, stderr=subprocess.PIPE)
    return True


def hyphen_to_zero(x):
    for k, v in x.items():
        if v == '-':
            x[k] = 0.0
    return x


def Calc():
    tb = prettytable.PrettyTable()
    tb.field_names = ['股票代码', '股票名称', '最新价', '涨跌幅', '警报']

    settings.init()
    stocks_d = pd.read_csv(settings.config['selected_file'], dtype=str)
    stocks_d.code = (stocks_d['code']).astype(str)
    stocks_d.maxp5 = (stocks_d['maxp5']).astype(float)
    stocks_dict = stocks_d.set_index('code')['maxp5'].to_dict()
    stocks = pd.read_csv(settings.config['selected_file'], dtype=str)
    pages = math.ceil(len(stocks)/100)
    
    for page in range(1,pages):
        stock_codes = stocks.loc[(page-1)*100:page *
                                 100, 'code'].values.astype(str).tolist()
        stock_list = get_data(stock_codes)
        stock_list = list(map(hyphen_to_zero, stock_list))
        stock_list = sorted(stock_list, key=lambda x: x['f3'], reverse=True)
        alarms = []
        # print(stocks_dict['000009'])
        for stock in stock_list:
            msg = ''
            # 针对所有自选股票的判断条件
            stock_c = stock['f12']
            if stock['f3'] >= settings.config['alarm_at'] and stock['f3'] <= 9.5:
                if stock['f12'] not in []:
                    if settings.config['max_total'] <= stock['f20'] <= settings.config['min_total']:
                        if stock['f2'] > stocks_dict[stock_c]:
                            msg = '{}即将涨停'.format(stock['f14']) 

            if msg:
                alarms.append(msg)
                row = [stock['f12'], stock['f14'], stock['f2'], stock['f3']]
                row.append(msg)
                tb.add_row(row)

    print(tb)
    
    for alarm in alarms:
        speak(alarm)

if __name__ == '__main__':
    while True:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        try:
            Calc()
        except:
            print('Failed')
        time.sleep(3)
