# -*- coding: utf-8 -*-
# 中药保护品种
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

    for i in range(1, 194):  # 遍历193个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=22&State=1&bcId=152911916125733631389542363535&State=1&curstart='+str(i)+'&State=1&tableName=TABLE22&State=1&viewtitleName=COLUMN141&State=1&viewsubTitleName=COLUMN140,COLUMN148,COLUMN143&State=1&tableView=%25E4%25B8%25AD%25E8%258D%25AF%25E4%25BF%259D%25E6%258A%25A4%25E5%2593%2581%25E7%25A7%258D&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=22&tableName=TABLE22&tableView=中药保护品种&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_zybhpz(c_bh, dt_insertTime, c_url, b_content,c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source, parse2json(browser.page_source),
                                            str(i) + '_' + str(j + 1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)


def parse2json(html):
    """
    保护品种编号bhpzbh
    药品名称ypmc
    公告号ggh
    药品批准文号yppzwh
    保护级别bhjb
    规格gg
    保护起始日bhqsr
    保护终止日bhzzr
    生产企业scqy
    剂型jx
    保护期限bhqx
    注z
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['bhpzbh'] = r"保护品种编号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ypmc'] = r"药品名称</td>\s*<td.*><a.*>(.*)</a></td></tr>"
    reg_dict['ggh'] = r"公告号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yppzwh'] = r"药品批准文号</td>\s*<td.*><a.*>(.*)</a></td></tr>"
    reg_dict['bhjb'] = r"保护级别</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['gg'] = r"规格</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['bhqsr'] = r"保护起始日</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['bhzzr'] = r"保护终止日</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['scqy'] = r"生产企业</td>\s*<td.*><a.*>(.*)</a></td></tr>"
    reg_dict['jx'] = r"剂型</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['bhqx'] = r"保护期限</td>\s*<td.*>(.*)</td></tr>"
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