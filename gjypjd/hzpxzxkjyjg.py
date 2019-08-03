# -*- coding: utf-8 -*-
# 化妆品行政许可检验机构

import pickle
import re
from selenium import webdriver
from gjypjd.utils import *
import json
import time

def main():
    option=None
    mysql_db=DataBase()
    #配置文件中开启是否无头，生产阶段关闭
    if if_headless():
        option = webdriver.ChromeOptions()
        option.add_argument(argument='headless')
        option.add_argument('--no-sandbox')

    for i in range(1, 4):  # 遍历3个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=108&State=1&bcId=152904558282171636476541922479&State=1&curstart='+str(i)+'&State=1&tableName=TABLE108&State=1&viewtitleName=COLUMN1416&State=1&viewsubTitleName=COLUMN1421&State=1&tableView=%25E5%258C%2596%25E5%25A6%2586%25E5%2593%2581%25E8%25A1%258C%25E6%2594%25BF%25E8%25AE%25B8%25E5%258F%25AF%25E6%25A3%2580%25E9%25AA%258C%25E6%259C%25BA%25E6%259E%2584&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=108&tableName=TABLE108&tableView=化妆品行政许可检验机构&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_hzpxzxkjyjg(c_bh, dt_insertTime, c_url, b_content, c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),str(i)+'_'+str(j+1)])

                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)

def parse2json(html):
    """
    检验机构名称jyjgmc
    联系地址lxdz
    联系人lxr
    联系电话lxdh
    传真cz
    机构类别jglb
    检验项目jyxm
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['jyjgmc'] = r"检验机构名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['lxdz'] = r"联系地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['lxr'] = r"联系人</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['lxdh'] = r"联系电话</td>\s*<td.*>(.*\s*.*)</td></tr>"
    reg_dict['cz'] = r"传真</td>\s*<td.*>(.*\s*.*)</td></tr>"
    reg_dict['jglb'] = r"机构类别</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['jyxm'] = r"检验项目</td>\s*<td.*>(.*)</td></tr>"



    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)


if __name__ == '__main__':
    main()