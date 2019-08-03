# -*- coding: utf-8 -*-
# 执业药师注册人员

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

    for i in range(1, 24637):  # 遍历24636个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=122&State=1&bcId=152912087124325608102345261418&State=1&curstart='+str(i)+'&State=1&tableName=TABLE122&State=1&viewtitleName=COLUMN1630&State=1&viewsubTitleName=COLUMN1633,COLUMN1631&State=1&tableView=%25E6%2589%25A7%25E4%25B8%259A%25E8%258D%25AF%25E5%25B8%2588%25E6%25B3%25A8%25E5%2586%258C%25E4%25BA%25BA%25E5%2591%2598&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=122&tableName=TABLE122&tableView=执业药师注册人员&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_zyyszcry(c_bh, dt_insertTime, c_url, b_content, c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),
                                            str(i) + '_' + str(j + 1)])

                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)


def parse2json(html):
    """
    姓名xm
    注册证编号zczbh
    执业地区zydq
    执业类别zylb
    执业范围zyfw
    执业单位zydw
    有效期yxq
    注z
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['xm'] = r"姓名</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zczbh'] = r"注册证编号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zydq'] = r"执业地区</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zylb'] = r"执业类别</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zyfw'] = r"执业范围</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zydw'] = r"执业单位</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yxq'] = r"有效期</td>\s*<td.*>(.*)</td></tr>"
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
