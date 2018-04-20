# -*- coding: utf-8 -*-
import requests
import traceback
from lxml import etree
import time


class Gu:
    # 类初始化
    def __init__(self, Gu_id, fluctuate = 4):
        self.gu_id = Gu_id  # id，即需要我们输入的数字，如昵称为“中国平安”的id为sh601318
        self.gu_name = []  # 股名，如“中国平安”
        self.gu_content = [] #抓得股价
        self.gu_fr = []#抓得浮动
        self.gu_fluctuate = fluctuate #浮动警示点

    # 获取价格
    def get_gu_info(self):
        try:
            url = "http://gu.qq.com/%s?gu_id/"% (
                self.gu_id)
            html = requests.get(url).content
            selector = etree.HTML(html.decode('utf-8'))
            # selector = etree.tostring(html, encoding="gb2312", pretty_print=True, method="html")
            price = selector.xpath("//span[@class='data']")
            name = selector.xpath("//h1[@class='col-1-1']")
            fluctuate = selector.xpath("//span[@class='fr']")
            gu_content = price[0].text
            gu_name = name[0].text
            gu_fr = fluctuate[0].text.strip("%")
            self.gu_content.append(gu_content)
            self.gu_name.append(gu_name)
            self.gu_fr.append(gu_fr)

        except Exception, e:
            print "Error1: ", e
            traceback.print_exc()

    def notification(self,price=0,name='',fluctaute=0,gu_fluctuate=0):

        if fluctaute > gu_fluctuate or price < -gu_fluctuate:
            print(name + u"波动较大，注意交易! 浮动：" + self.gu_fr[0])#send notification

    # 运行爬虫
    def start(self):
        try:
            self.get_gu_info()
            # print u"信息抓取完毕"
            print u"股名：" + self.gu_name[0] + u"  最新价格：" + self.gu_content[0] + u" 涨幅:" + self.gu_fr[0]
            self.notification(float(self.gu_content[0]),self.gu_name[0],float(self.gu_fr[0]),float(self.gu_fluctuate[0]))
        except Exception, e:
            print "Error: ", e
            traceback.print_exc()

def main():
    try:
        f1 = open('fluctaute.txt','r')
        g_fluctaute = f1.readline()
        f1.close()

        f = open('stock.txt', 'r')
        gu_id = f.readlines()
        f.close()

    except Exception, e:
        print "Error: ", e
        traceback.print_exc()
    while 1 :
        for gu_id1 in gu_id:
            gj = Gu(gu_id1.strip('\n'),g_fluctaute.strip('\n'))  # 调用Gu类，创建实例gj
            gj.start()  # 爬取信息
        time.sleep(1)
if __name__ == "__main__":
    main()