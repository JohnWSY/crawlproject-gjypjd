# -*- coding: utf-8 -*-

# 医疗器械广告

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

    for i in range(1, 5292):  # 遍历5293个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=40&State=1&bcId=152904606190314452995556113153&State=1&curstart='+str(i)+'&State=1&tableName=TABLE40&State=1&viewtitleName=COLUMN428&State=1&viewsubTitleName=COLUMN427,COLUMN424&State=1&tableView=%25E5%258C%25BB%25E7%2596%2597%25E5%2599%25A8%25E6%25A2%25B0%25E5%25B9%25BF%25E5%2591%258A&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=40&tableName=TABLE40&tableView=医疗器械广告&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_ylqxgg(c_bh, dt_insertTime, c_url, b_content, c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),
                                            str(i) + '_' + str(j + 1)])

                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)

def parse2json(html):
    """
    医疗器械广告批准文号ylqxggpzwh
    单位名称dwmc
    地址dz
    邮政编码yzbm
    通用名称tymc
    备注bz
    商标名称sbmc
    广告类别gglb
    时长sc
    广告有效期ggyxq
    广告发布内容ggfbnr
    注册证号zczh
    商品名称spmc
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['ylqxggpzwh'] = r"医疗器械广告批准文号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['dwmc'] = r"单位名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['dz'] = r"地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yzbm'] = r"邮政编码</td>\s*<td.*>(.*\s*.*)</td></tr>"
    reg_dict['tymp'] = r"通用名称</td>\s*<td.*>(.*\s*.*)</td></tr>"
    reg_dict['bz'] = r"备注</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['sbmc'] = r"商标名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['gglb'] = r"广告类别</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['sc'] = r"时长</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ggyxq'] = r"广告有效期</td>\s*<td.*>(.*\s*.*)</td></tr>"
    reg_dict['ggfbnr'] = r"广告发布内容</td>\s*<td><a href=\"(.*)\" target.*>.*</a></td></tr>"
    reg_dict['zczh'] = r"注册证号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['spmc'] = r"商品名称</td>\s*<td.*>(.*)</td></tr>"


    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    result_json['ggfbnr'] = 'http://app1.sfda.gov.cn' + result_json['ggfbnr']
    return json.dumps(result_json, ensure_ascii=False)


if __name__ == '__main__':
    main()
