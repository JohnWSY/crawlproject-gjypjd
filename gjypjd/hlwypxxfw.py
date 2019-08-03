# -*- coding: utf-8 -*-
# 互联网药品信息服务

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

    for i in range(1, 1041):  # 遍历1040个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=28&State=1&bcId=152912030752488832300204864740&State=1&curstart='+str(i)+'&State=1&tableName=TABLE28&State=1&viewtitleName=COLUMN212&State=1&viewsubTitleName=COLUMN210&State=1&tableView=%25E4%25BA%2592%25E8%2581%2594%25E7%25BD%2591%25E8%258D%25AF%25E5%2593%2581%25E4%25BF%25A1%25E6%2581%25AF%25E6%259C%258D%25E5%258A%25A1&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=28&tableName=TABLE28&tableView=互联网药品信息服务&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_hlwypxxfw(c_bh, dt_insertTime, c_url, b_content, c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
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
    服务性质fwxz
    机构名称jgmc
    法定代表fddb
    网站负责人wzfzr
    变更历史记录bglsjl
    网站域名wzym
    发证机关fzjg
    有效起始日期yxqsrq
    有效截至日期yxjzrq
    证书状态zszt
    地址邮编dzyb
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['zsbh'] = r"证书编号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fwxz'] = r"服务性质</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['jgmc'] = r"机构名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fddb'] = r"法定代表</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['wzfzr'] = r"网站负责人</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['bglsjl'] = r"变更历史记录</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['wzym'] = r"网站域名</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fzjg'] = r"发证机关</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yxqsrq'] = r"有效起始日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yxjzrq'] = r"有效截至日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['zszt'] = r"证书状态</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['dzyb'] = r"地址邮编</td>\s*<td.*>(.*)</td></tr>"


    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)


if __name__ == '__main__':
    main()
