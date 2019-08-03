# -*- coding: utf-8 -*-
# 国产非特殊用途化妆品备案信息(一)-列表数据

import re
from seleniumrequests import Chrome
from selenium import webdriver
from gjypjd.utils import *
import json
import time

def main():
    option = None
    mysql_db = DataBase()
    # 配置文件中开启是否无头，生产阶段关闭
    if if_headless():
        option = webdriver.ChromeOptions()
        option.add_argument(argument='headless')
        option.add_argument('--no-sandbox')

    #先调一次post请求，获取一级目录页的页数
    url = "http://125.35.6.80:8181/ftban/itownet/fwAction.do?method=getBaNewInfoPage&on=true&page=1&pageSize=15&productName=&conditionType=1&applyname=&applysn="
    browser = Chrome(chrome_options=option)
    res = browser.request("post", url)
    html = res.text
    browser.close()
    json_return = json.loads(html)
    pageCount = json_return["pageCount"]

    for i in range(1, pageCount+1): #遍历目录网页
        try :
            url_1 = "http://125.35.6.80:8181/ftban/itownet/fwAction.do?method=getBaNewInfoPage&on=true&page="+str(i)+"&pageSize=15&productName=&conditionType=1&applyname=&applysn="
            browser = Chrome(chrome_options=option)
            res = browser.request("post",url_1)
            html = res.text
            browser.close()
            json_return = json.loads(html)
            d = json_return['list'] #得到页面列表信息

            for j in range(len(d)):
                sql = "insert into t_gcftsythzpbaxx_lbsj(c_bh, dt_insertTime, c_url, b_content, c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_1, html, parse2json(d[j]),str(i) + '_' + str(j + 1)])
        except Exception as e:
            print(e)
            time.sleep(5)

def parse2json(origin): #不用解析页面信息直接处理即可
    """
    产品名称 cpmc
    备案编号 babh
    单位名称 dwmc
    备案日期  barq

    :return: json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()

    result_json['cpmc'] = origin['productName']
    result_json['babh'] = origin['applySn']
    result_json['dwmc'] = origin['enterpriseName']
    result_json['barq'] = origin['provinceConfirm']

    return json.dumps(result_json, ensure_ascii=False)

if __name__ == '__main__':
    main()