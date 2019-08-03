# -*- coding: utf-8 -*-
# 药品注册批件发送信息

import time
import pickle
import re
from selenium import webdriver
from gjypjd.utils import *
import json


def main():
    option=None
    mysql_db = DataBase()
    #配置文件中开启是否无头，生产阶段关闭
    if if_headless():
        option = webdriver.ChromeOptions()
        option.add_argument(argument='headless')
        option.add_argument('--no-sandbox')

    for i in range(1, 291):  # 遍历290个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=15&State=1&bcId=152911907292630602758823122400&State=1&curstart='+str(i)+'&State=1&tableName=TABLE15&State=1&viewtitleName=COLUMN88&State=1&tableView=%25E8%258D%25AF%25E5%2593%2581%25E6%25B3%25A8%25E5%2586%258C%25E6%2589%25B9%25E4%25BB%25B6%25E5%258F%2591%25E9%2580%2581%25E4%25BF%25A1%25E6%2581%25AF&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=15&tableName=TABLE15&tableView=药品注册批件发送信息&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_ypzcpjfsxx(c_bh, dt_insertTime, c_url, b_content,c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),
                                            str(i) + '_' + str(j + 1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()

        except Exception as e:
            print(e)
            time.sleep(5)

def parse2json(html):
    """
    药品通用名yptym
    英文名ywm
    申请分类sqfl
    申请限制sqxz
    限制到期日xzdqr
    备注bz
    批准日期pzrq
    注z
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['yptym'] = r"药品通用名</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ywm'] = r"英文名</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['sqfl'] = r"申请分类</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['sqxz'] = r"申请限制</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['xzdqr'] = r"限制到期日</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['bz'] = r"备注</td>\s*<td.*?>(.*)</td></tr>"
    reg_dict['pzrq'] = r"批准日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['z'] = r"注</td>\s*<td.*><span.*>(.*)</span></td></tr>"


    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)

if __name__ == '__main__':
    main()