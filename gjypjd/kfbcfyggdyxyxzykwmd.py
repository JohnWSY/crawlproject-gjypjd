# -*- coding: utf-8 -*-
# 可发布处方药广告的医学药学专业刊物名单
import pickle
import re
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

    for i in range(1, 39):  # 遍历38个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=9&State=1&bcId=152904631433672228463752540473&State=1&curstart='+str(i)+'&State=1&tableName=TABLE9&State=1&viewtitleName=COLUMN50&State=1&tableView=%25E5%258F%25AF%25E5%258F%2591%25E5%25B8%2583%25E5%25A4%2584%25E6%2596%25B9%25E8%258D%25AF%25E5%25B9%25BF%25E5%2591%258A%25E7%259A%2584%25E5%258C%25BB%25E5%25AD%25A6%25E8%258D%25AF%25E5%25AD%25A6%25E4%25B8%2593%25E4%25B8%259A%25E5%2588%258A%25E7%2589%25A9%25E5%2590%258D%25E5%258D%2595&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=9&tableName=TABLE9&tableView=可发布处方药广告的医学药学专业刊物名单&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_kfbcfyggdyxyxzykwmd(c_bh, dt_insertTime, c_url, b_content, c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),
                                            str(i) + '_' + str(j + 1)])

                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)

def parse2json(html):
    """
    登记地 djd
    CN号 cnh
    刊物中文名称  kwzwmc
    广告经营许可证号    ggjyxkzh
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['djd'] = r"登记地</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cnh'] = r"CN号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['kwzwmc'] = r"刊物中文名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ggjyxkzh'] = r"广告经营许可证号</td>\s*<td.*>(.*)</td></tr>"


    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)


if __name__ == '__main__':
    main()
