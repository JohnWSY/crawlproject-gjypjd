# -*- coding: utf-8 -*-
# 中药提取物备案公示


import pickle
import re
from selenium import webdriver
from gjypjd.utils import *
import json

import time
def main():
    option=None
    mysql_db = DataBase()
    #配置文件中开启是否无头，生产阶段关闭
    if if_headless():
        option = webdriver.ChromeOptions()
        option.add_argument(argument='headless')
        option.add_argument('--no-sandbox')

    for i in range(1, 254):  # 遍历253个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=109&State=1&bcId=152904809034853658596912365040&State=1&curstart='+str(i)+'&State=1&tableName=TABLE109&State=1&viewtitleName=COLUMN1427&State=1&viewsubTitleName=COLUMN1429,COLUMN1428&State=1&tableView=%25E4%25B8%25AD%25E8%258D%25AF%25E6%258F%2590%25E5%258F%2596%25E7%2589%25A9%25E5%25A4%2587%25E6%25A1%2588%25E5%2585%25AC%25E7%25A4%25BA&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=109&tableName=TABLE109&tableView=中药提取物备案公示&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_zytqwbags(c_bh, dt_insertTime, c_url, b_content,c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source,parse2json(browser.page_source),
                                            str(i) + '_' + str(j + 1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)
def parse2json(html):
    """
    使用备案号sybah
    药品通用名称yptymc
    药品生产企业ypscqy
    批准文号pzwh
    备案日期barq
    备案状态bazt
    中药提取物信息zytqwxx
    注z
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['sybah'] = r"使用备案号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yptymc'] = r"药品通用名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ypscqy'] = r"药品生产企业</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['pzwh'] = r"批准文号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['barq'] = r"备案日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['bazt'] = r"备案状态</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zytqwxx'] = r"中药提取物信息</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['z'] = r"注</td>\s*<td.*>(.*)</td></tr>"


    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)

if __name__ == '__main__':
    main()