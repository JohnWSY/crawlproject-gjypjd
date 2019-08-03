# -*- coding: utf-8 -*-
#药物临床试验机构名单


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

    for i in range(1, 104):  # 遍历103个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=19&State=1&bcId=152904843704682622352673850395&State=1&curstart='+str(i)+'&State=1&tableName=TABLE19&State=1&viewtitleName=COLUMN121&State=1&tableView=%25E8%258D%25AF%25E7%2589%25A9%25E4%25B8%25B4%25E5%25BA%258A%25E8%25AF%2595%25E9%25AA%258C%25E6%259C%25BA%25E6%259E%2584%25E5%2590%258D%25E5%258D%2595&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=19&tableName=TABLE19&tableView=药物临床试验机构名单&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_ywlcsyjgmd(c_bh, dt_insertTime, c_url, b_content,c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),
                                            str(i) + '_' + str(j + 1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)
def parse2json(html):
    """
    证书编号zsbh
    医疗机构名称yljgmc
    地址dz
    省市ss
    认证日期rzrq
    有效期截止日yxjzr
    认定专业rdzy
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['zsbh'] = r"证书编号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yljgmc'] = r"医疗机构名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['dz'] = r"地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ss'] = r"省市</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['rzrq'] = r"认证日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yxjzr'] = r"有效期截止日</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['rdzy'] = r"认定专业</td>\s*<td.*>(.*)</td></tr>"

    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)


if __name__ == '__main__':
    main()