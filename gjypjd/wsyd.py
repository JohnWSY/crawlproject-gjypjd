# -*- coding: utf-8 -*-
# 网上药店

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
    for i in range(1, 48):  # 遍历47个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=96&State=1&bcId=152912074294836217897912479856&State=1&curstart='+str(i)+'&State=1&tableName=TABLE96&State=1&viewtitleName=COLUMN1229&State=1&viewsubTitleName=COLUMN1227&State=1&tableView=%25E7%25BD%2591%25E4%25B8%258A%25E8%258D%25AF%25E5%25BA%2597&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=96&tableName=TABLE96&tableView=网上药店&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_wsyd(c_bh, dt_insertTime, c_url, b_content, c_json,c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
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
    服务范围fwfw
    单位名称dwmc
    法定代表人fddbr
    单位地址dwdz
    省份sf
    网站名称wzmc
    IP地址ipdz
    域名ym
    发证日期fzrq
    有效截至日期yxjzrq
    邮编yb
    注z
    :return:json
    """
    # 初始化，避免取不到的情况下为空值
    result_json = dict()
    # 批准文号
    reg_dict = dict()
    reg_dict['zsbh'] = r"证书编号</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fwfw'] = r"服务范围</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['dwmc'] = r"单位名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fddbr'] = r"法定代表人</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['dwdz'] = r"单位地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['sf'] = r"省份</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['wzmc'] = r"网站名称</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ipdz'] = r"IP地址</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['ym'] = r"域名</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['fzrq'] = r"发证日期</td>\s*<td.*>(.*)</td></tr>"
    reg_dict['yxjzrq'] = r"有效截至日期</td>\s*<td.*>(.*)</td></tr>"
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
