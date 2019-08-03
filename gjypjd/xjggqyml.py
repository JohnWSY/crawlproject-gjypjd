# -*- coding: utf-8 -*-
# 虚假广告企业名录

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

    for i in range(1, 7):  # 遍历6个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=119&State=1&bcId=152904650094884510370649307696&State=1&curstart='+str(i)+'&State=1&tableName=TABLE119&State=1&viewtitleName=COLUMN1584&State=1&viewsubTitleName=COLUMN1585&State=1&tableView=%25E8%2599%259A%25E5%2581%2587%25E5%25B9%25BF%25E5%2591%258A%25E4%25BC%2581%25E4%25B8%259A%25E5%2590%258D%25E5%25BD%2595&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=119&tableName=TABLE119&tableView=虚假广告企业名录&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_xjggqyml(c_bh, dt_insertTime, c_url, b_content, c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),
                                            str(i) + '_' + str(j + 1)])

                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)


def parse2json(html):
    """
    产品类别    cplb
    广告中标识产品名称   ggzbscpmc
    产品名称    cpmc
    生产企业名称  scqymc
    生产企业所在地 scqyszd
    产品批准文号  cppzwh
    违法内容简述  wfnrjs
    总局通告号   zjtgh
    总局通告时间  zjtgsj
    注   z
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['cplb'] = r"产品类别</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ggzbscpmc'] = r"广告中标识产品名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cpmc'] = r"<td.*>产品名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['scqymc'] = r"生产企业名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['scqyszd'] = r"生产企业所在地</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['cppzwh'] = r"产品批准文号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['wfnrjs'] = r"违法内容简述</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zjtgh'] = r"总局通告号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zjtgsj'] = r"总局通告时间</td>\s*<td.*>(.*)</td></tr>"
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
