from bitarray import bitarray
from random import randint
import sys
import redis
import asyncio
import requests
import settings
import math
import time
import pandas as pd
import numpy as np

client = redis.Redis(host='localhost', port=6379)

name_of_group_a = "G_A"
name_of_group_b = "G_B"
name_of_group_c = "G_C"
name_of_group_d = "G_D"

all_groups = [name_of_group_a, name_of_group_b,
              name_of_group_c, name_of_group_d]

name_of_bitmap_all_zero = "G_0"
name_of_bitmap_all_one = "G_1"


stock_postion_table = {}
postion_stock_table = {}
stocks = [
    # ('688981', '中芯国际', 10337486.055, 43666041.1928),
    # ('688819', '天能股份', 476848.841697, 4363756.9),
    # ('688800', '瑞可达', 172253.29072, 846720.0),
    # ('688799', '华纳药厂', 77241.242382, 378764.4),
    # ('688798', '艾为电子', 748275.5124, 3884400.0),
    # ('688793', 'XD倍轻松', 115166.89134, 565855.2),
    # ('688789', '宏华数科', 391876.4637, 1928880.0),
    # ('688788', '科思科技', 245423.4156, 1065032.6712),
    # ('688787', '海天瑞声', 74672.61516, 367224.0),
    # ('688786', '悦安新材', 99231.923492, 487610.6456),
    # ('688779', '长远锂科', 921031.11415, 5112396.6208),
    # ('688778', '厦钨新能', 650833.553124, 3156728.806316),
    # ('688777', '中控技术', 410879.53521, 4639448.76),
    # ('688776', '国光电气', 286451.738042, 1391720.519256),
    # ('688768', '容知日新', 139617.22017, 685708.906518),
    # ('688766', '普冉股份', 268691.316218, 1257788.666242),
    # ('688728', '格科微', 503769.561246, 7644095.862207),
    # ('688718', '唯赛勃', 104153.24322, 512749.201939),
    # ('688711', '宏微科技', 191292.623614, 931155.979636),
    # ('688700', '东威科技', 194594.998608, 855820.8),
    # ('688699', '明微电子', 495165.384, 2084906.88),
    # ('688698', '伟创电气', 88051.5, 414360.0),
    # ('688696', '极米科技', 487442.64588, 2256400.0),
    # ('688690', '纳微科技', 377334.157264, 3604514.699584),
    # ('688689', '银河微电', 101836.6523, 412035.6),
    # ('688687', '凯因科技', 102172.578108, 430005.564504),
    # ('688686', '奥普特', 695411.410464, 3093827.33304),
    # ('688685', '迈信林', 62677.29139, 308192.667585),
    # ('688683', '莱尔科技', 69698.52656, 335745.6),
    # ('688682', '霍莱沃', 88664.38322, 436415.0),
    # ('688681', '科汇股份', 39188.956864, 191755.44),
    # ('688680', '海优新材', 515328.982, 2120244.7),
    # ('688679', '通源环境', 42183.889858, 176727.54385),
    # ('688678', '福立旺', 87218.0325, 410319.45),
    # ('688677', '海泰新光', 186148.215, 874583.9),
    # ('688676', '金盘科技', 87819.7815, 1033173.9),
    # ('688670', '金迪克', 163181.748291, 792088.0),
    # ('688669', '聚石化学', 69481.00004, 325733.33566),
    # ('688668', '鼎通科技', 81854.064, 331024.32),
    # ('688667', '菱电电控', 141508.64728, 590304.0),
    # ('688665', '四方光电', 202304.635866, 923020.0),
    # ('688663', '新风光', 81427.978845, 378004.95),
    # ('688662', '富信科技', 73682.920428, 315722.72),
    # ('688661', '和林微纳', 154209.644358, 757680.0),
    # ('688660', '电气风电', 504804.468168, 1848000.0924),
    # ('688659', '元琛科技', 50762.003232, 221440.0),
    # ('688658', '悦康药业', 194000.6616, 975600.0),
    # ('688656', '浩欧博', 71463.389615, 334019.963416),
    # ('688655', '迅捷兴', 58453.186584, 243970.31),
    # ('688639', '华恒生物', 151402.257411, 689796.0),
    # ('688636', '智明达', 148663.70436, 730500.0),
    # ('688633', '星球石墨', 129120.33162, 567683.67187),
    # ('688630', '芯碁微装', 153960.29517, 757416.0),
    # ('688628', '优利德', 72627.5, 305800.0),
    # ('688626', '翔宇医疗', 201915.8837, 872000.0),
    # ('688625', '呈和科技', 165602.3115, 766667.05),
    # ('688621', '阳光诺和', 253653.0129, 1176000.0),
    # ('688619', '罗普特', 102318.01101, 428140.40229),
    # ('688618', '三旺通信', 44355.73023, 195945.62561),
    # ('688617', '惠泰医疗', 538453.3358, 2504058.53),
    # ('688616', '西力科技', 53203.9191, 221850.0),
    # ('688613', '奥精医疗', 188889.884874, 919200.004596),
    # ('688611', '杭州柯林', 62154.68938, 273798.2),
    # ('688609', '九联科技', 102572.185, 635000.0),
    # ('688608', '恒玄科技', 616800.0, 3084000.0),
    # ('688607', '康众医疗', 95358.01629, 427866.426085),
    # ('688606', '奥泰生物', 143715.7415, 619897.6675),
    # ('688601', '力芯微', 191478.845942, 940736.0),
    # ('688600', '皖仪科技', 121551.13488, 241078.72),
    # ('688599', '天合光能', 6129652.668932, 10431125.0355),
    # ('688598', '金博股份', 2349775.567989, 2909094.6),
    # ('688597', '煜邦电力', 48450.71706, 228003.09016),
    # ('688596', '正帆科技', 388081.811052, 493506.0),
    # ('688595', '芯海科技', 195287.5, 919000.0),
    # ('688590', '新致软件', 71016.03936, 334192.90608),
    # ('688589', '力合微', 205566.340221, 366300.0),
    # ('688588', '凌志软件', 410850.13956, 652416.314893),
    # ('688586', '江航装备', 496451.227909, 1138963.141407),
    # ('688585', '上纬新材', 48191.6952, 469324.8),
    # ('688580', '伟思医疗', 224019.90839, 643142.13647),
    # ('688579', '山大地纬', 338117.5239, 483612.09),
    # ('688578', '艾力斯', 213859.2548, 1280700.0),
    # ('688577', '浙海德曼', 102388.44512, 302025.74512),
    # ('688575', '亚辉龙', 97742.34115, 1194750.0),
    # ('688571', '杭华股份', 68483.6992, 286720.0)
]
stocks_dict = {}


def p(value):
    print(type(value), value)


def hyphen_to_zero(x):
    for k, v in x.items():
        if v == '-':
            x[k] = 0.0
    return x


def add_market_code(x):
    y = '0.' + x
    if x.startswith('6'):
        y = '1.' + x
    return y


def calc_limit_price(pre_close):
    if pre_close == 0:
        return 0

    limit = pre_close + pre_close * 0.1
    limit = '%.2f' % limit
    # print(limit)
    return float(limit)
    # f2最新价 f3涨跌幅 f4涨跌额 f5成交量 f6成交额 f7振幅
    # f8换手率 f12 代码  f14 名称  f15最高价  f16最低  f17今开 f18昨收  f23 市净率,f10量比 f9市盈率 f20总市值


def get_data(stock_codes):
    stock_codes = list(map(add_market_code, stock_codes))
    stock_codes = ','.join(stock_codes)

    endpoint = 'http://push2.eastmoney.com/api/qt/ulist.np/get'
    var1 = '?fields=f2,f3,f14,f12,f13,f19,f20,f10,f18'
    var2 = '&invt=2&fltt=2&fid=f3'
    var3 = '&ut=bd1d9ddb04089700cf9c27f6f7426281&cb=&secids='
    url = '{0}{1}{2}{3}{4}'.format(endpoint, var1, var2, var3, stock_codes)
    # print(url)
    response = requests.get(url)
    data = response.json()
    return data['data']['diff']


def show_group_bytes(name_of_bitmap):
    client.bitop("AND", name_of_bitmap, name_of_bitmap, name_of_bitmap_all_one)
    bytes_value = client.getrange(name_of_bitmap, 0, -1)
    # print(bytes_value)
    bitarray_a = bitarray()
    bitarray_a.frombytes(bytes_value)
    print(len(bitarray_a), bitarray_a)
    stocks_in_group = []
    pos = 0
    while pos < len(bitarray_a):
        if bitarray_a[pos] == 1:
            stocks_in_group.append(postion_stock_table[pos])
        pos = pos + 1
    for stock in stocks_in_group:
        print(stock)


def showResult():
    start = time.perf_counter()
    for group_name in all_groups:
        print("--------------", group_name, "--------------\n")
        show_group_bytes(group_name)
    duration = time.perf_counter() - start
    print(f"Run showResult {duration:0.4f} seconds")


def initialize_bitwise_operator(stock_count):
    print("initialize_bitwise_operator")
    global stock_postion_table
    global postion_stock_table
    global stocks
    client.delete(name_of_bitmap_all_zero, name_of_bitmap_all_one)
    for group_name in all_groups:
        client.delete(group_name)
    for i in range(0, stock_count):
        client.setbit(name_of_bitmap_all_zero, i, 0)
        client.setbit(name_of_bitmap_all_one, i, 1)
    for i, v in enumerate(stocks):
        stock_value = v[0] + ":" + v[1]
        stock_postion_table[stock_value] = i
        postion_stock_table[i] = stock_value


def moveStock(stock_name, move_to_group_name):
    global stock_postion_table
    # print("stock_name", stock_name)
    # stock_name 605117:德业股份

    # print("move_to_group_name", move_to_group_name)
    # move_to_group_name G_D

    if move_to_group_name is None:
        return
    postion_of_stock = stock_postion_table[stock_name]
    for group_name in all_groups:
        if(group_name == move_to_group_name):
            client.setbit(group_name, postion_of_stock, 1)
        else:
            client.setbit(group_name, postion_of_stock, 0)


async def process(num_of_task, stocks, stock_count, part_num):
    # 获取处理围区间
    # print("part_num", part_num)
    # print("stock_count", stock_count)
    # split workload into parts
    more = stock_count % num_of_task
    avg = (stock_count - more) // num_of_task
    start = part_num * avg
    end = (part_num + 1) * avg
    if(part_num == num_of_task - 1):
        end = end + more
    # print(f"num_of_task:{num_of_task}, part_num:{part_num}, avg:{avg}, more:{more}, start:{start}, end:{end}")

    # 根据股票代码,批量获取数据
    target_part = stocks[start:end]
    # print(target_part)
    np_array = np.array(target_part)
    stock_codes = np_array[:, 0]
    # print(stock_codes)
    stock_data_list = get_data(stock_codes)
    # print(stock_data_list)
    stock_data_list = list(map(hyphen_to_zero, stock_data_list))
    stock_data_list = sorted(stock_data_list, key=lambda x: x['f3'], reverse=True)

    for stock in stock_data_list:
        # print(stock)
        # {'f2': 28.46, 'f3': 0.71, 'f10': 1.47, 'f12': '605259', 'f13': 1, 'f14': '绿田机械', 'f18': 28.26, 'f19': 2, 'f20': 2504480000}
        group_x = calc(stock)
        # print(stock['f12'], stock['f14'], f"group_x={group_x}")
        # 605117 德业股份 group_x=G_D
        moveStock(stock['f12'] + ":" + stock['f14'], group_x)


def calc(stock):
    global stocks_dict
    # print("stocks_dict", stocks_dict)
    # print("stock['f2'] ", stock['f2'])

    limit_price = calc_limit_price(stock['f18'])
    limit_percent = (limit_price - stock['f18']) / stock['f18'] * 100
    limit_percent = '%.2f' % limit_percent

    if settings.config['max_total'] <= stock['f20'] <= settings.config['min_total']:
        if stock['f2'] > stocks_dict[stock['f12']]:
            if stock['f3'] >= settings.config['alarm_a'] and stock['f3'] < settings.config['alarm_b']:
                return name_of_group_a
            if stock['f3'] >= settings.config['alarm_b'] and stock['f3'] < settings.config['alarm_c']:
                return name_of_group_b
            if stock['f3'] >= settings.config['alarm_c'] and stock['f3'] < float(limit_percent):
                return name_of_group_c
            if stock['f3'] == float(limit_percent):
                return name_of_group_d


async def main():
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
    stock_count = len(stocks)
    # print("stock_count", stock_count)
    num_of_task = math.ceil(stock_count / 600)
    # print("num_of_task", num_of_task)
    initialize_bitwise_operator(stock_count)
    task_list = []
    start = time.perf_counter()
    for part_num in range(num_of_task):  # num_of_task
        task = asyncio.create_task(
            process(num_of_task, stocks, stock_count, part_num))
        task_list.append(task)
    print(f"{num_of_task} tasks are going to run")
    done, pending = await asyncio.wait(task_list, timeout=None)
    duration = time.perf_counter() - start
    print(f"Run task {duration:0.4f} seconds")

# moveStock("688800:瑞可达", name_of_group_c)
# moveStock("688799:华纳药厂", name_of_group_c)
# moveStock("688981:中芯国际", name_of_group_a)
# moveStock("688571:杭华股份", name_of_group_c)
# moveStock("688981:中芯国际", name_of_group_c)
# moveStock("688800:瑞可达", name_of_group_b)
# moveStock("688799:华纳药厂", name_of_group_d)

asyncio.run(main())
# showResult()
