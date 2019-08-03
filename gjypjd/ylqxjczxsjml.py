# -*- coding: utf-8 -*-

# 医疗器械检测中心受检目录

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

    for i in range(1, 2197):  # 遍历2196个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=18&State=1&bcId=152904478731623032392756211974&State=1&curstart='+str(i)+'&State=1&tableName=TABLE18&State=1&viewtitleName=COLUMN110&State=1&viewsubTitleName=COLUMN751&State=1&tableView=%25E5%258C%25BB%25E7%2596%2597%25E5%2599%25A8%25E6%25A2%25B0%25E6%25A3%2580%25E6%25B5%258B%25E4%25B8%25AD%25E5%25BF%2583%25E5%258F%2597%25E6%25A3%2580%25E7%259B%25AE%25E5%25BD%2595&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=18&tableName=TABLE18&tableView=医疗器械检测中心受检目录&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_ylqxjczxsjml(c_bh, dt_insertTime, c_url, b_content, c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),
                                            str(i) + '_' + str(j + 1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)
def parse2json(html):
    """
    产品名称cpmc
    项目序号xmxh
    项目名称xmmc
    检测标准名称jybzmc
    检测标准编号jybzbh
    限制范围及说明xzfwjsm
    检测单位jcdw
    省市ss
    认可日期rkrq
    有效期yxq
    备注bz

    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['cpmc'] = r"产品名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['xmxh'] = r"项目序号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['xmmc'] = r"项目名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['jybzmc'] = r"检测标准名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['jybzbh'] = r"检测标准编号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['xzfwjsm'] = r"限制范围及说明</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['jcdw'] = r"检测单位</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ss'] = r"省市</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['rkrq'] = r"认可日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yxq'] = r"有效期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['bz'] = r"备注</td>\s*<td.*>(.*)</td></tr>"

    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)
if __name__ == '__main__':
    main()