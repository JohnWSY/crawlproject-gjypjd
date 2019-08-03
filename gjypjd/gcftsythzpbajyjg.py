# -*- coding: utf-8 -*-
# 国产非特殊用途化妆品备案检验机构

import pickle
import re
from selenium import webdriver
from gjypjd.utils import *
import json
import time

def main():
    mysql_db = DataBase()
    option=None
    #配置文件中开启是否无头，生产阶段关闭
    if if_headless():
        option = webdriver.ChromeOptions()
        option.add_argument(argument='headless')
        option.add_argument('--no-sandbox')

    for i in range(1, 16):  # 遍历15个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=83&State=1&bcId=152904525073687715604307579905&State=1&curstart='+str(i)+'&State=1&tableName=TABLE83&State=1&viewtitleName=COLUMN1003&State=1&tableView=%25E5%259B%25BD%25E4%25BA%25A7%25E9%259D%259E%25E7%2589%25B9%25E6%25AE%258A%25E7%2594%25A8%25E9%2580%2594%25E5%258C%2596%25E5%25A6%2586%25E5%2593%2581%25E5%25A4%2587%25E6%25A1%2588%25E6%25A3%2580%25E9%25AA%258C%25E6%259C%25BA%25E6%259E%2584&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=83&tableName=TABLE83&tableView=国产非特殊用途化妆品备案检验机构&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_gcftsythzpbajyjg(c_bh, dt_insertTime, c_url, b_content, c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),str(i)+'_'+str(j+1)])

                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)

def parse2json(html):
    """
    检验机构名称jyjgmc
    机构类别jglb
    检验项目jyxm
    传真cz
    联系地址lxdz
    联系电话lxdh
    联系人lxr
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['jyjgmc'] = r"检验机构名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['jglb'] = r"机构类别</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['jyxm'] = r"检验项目</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cz'] = r"传真</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['lxdz'] = r"联系地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['lxdh'] = r"联系电话</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['lxr'] = r"联系人</td>\s*<td.*>(.*)</td></tr>"


    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)


if __name__ == '__main__':
    main()