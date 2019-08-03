# -*- coding: utf-8 -*-

# 互联网药品交易服务
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

    for i in range(1, 68):  # 遍历67个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=33&State=1&bcId=152912035808486317999702746820&State=1&curstart='+str(i)+'&State=1&tableName=TABLE33&State=1&viewtitleName=COLUMN312&State=1&viewsubTitleName=COLUMN310&State=1&tableView=%25E4%25BA%2592%25E8%2581%2594%25E7%25BD%2591%25E8%258D%25AF%25E5%2593%2581%25E4%25BA%25A4%25E6%2598%2593%25E6%259C%258D%25E5%258A%25A1&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=33&tableName=TABLE33&tableView=互联网药品交易服务&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_hlwypjyfw(c_bh, dt_insertTime, c_url, b_content, c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
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
    单位名称dwmc
    法定代表人fddbr
    网站名称wzmc
    服务范围fwfw
    域名ym
    IP地址ipdz
    发证日期fzrq
    有效截至日期yxjzrq
    单位地址dwdz
    邮编yb
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['zsbh'] = r"证书编号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['dwmc'] = r"单位名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fddbr'] = r"法定代表人</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['wzmc'] = r"网站名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fwfw'] = r"服务范围</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ym'] = r"域名</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ipdz'] = r"IP地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fzrq'] = r"发证日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yxjzrq'] = r"有效截至日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['dwdz'] = r"单位地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yb'] = r"邮编</td>\s*<td.*>(.*)</td></tr>"


    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)


if __name__ == '__main__':
    main()
