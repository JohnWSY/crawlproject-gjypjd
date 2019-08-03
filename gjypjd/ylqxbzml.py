# -*- coding: utf-8 -*-
# 医疗器械标准目录


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
    for i in range(1, 107):  # 遍历106个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=21&State=1&bcId=152904437880111023387499337007&State=1&curstart='+str(i)+'&State=1&tableName=TABLE21&State=1&viewtitleName=COLUMN132&State=1&tableView=%25E5%258C%25BB%25E7%2596%2597%25E5%2599%25A8%25E6%25A2%25B0%25E6%25A0%2587%25E5%2587%2586%25E7%259B%25AE%25E5%25BD%2595&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=21&tableName=TABLE21&tableView=医疗器械标准目录&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_ylqxbzml(c_bh, dt_insertTime, c_url, b_content,c_json, c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source,parse2json(browser.page_source),str(i)+'_'+str(j+1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)


def parse2json(html):
    '''
    标准名称 bzmc
    标准编号bzbh
    归口单位 gkdw
    一致性程度标识 yzxcdbs
    代替号 dth
    实施日期 ssrq
    发布日期fbrq
    国际标准gjbz
    注z
'''
    reg_dict = dict()
    result_json = dict()
    reg_dict['bzmc'] = r'标准名称</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['bzbh'] = r'标准编号</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['gkdw'] = r'归口单位</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['yzxcdbs'] = r'一致性程度标识</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['dth'] = r'代替号</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['ssrq'] = r'实施日期</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['fbrq'] = r'发布日期</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['gjbz'] = r'国际标准</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['z'] = r'注</td>\s*<td.*><span.*>(.*)</span></td></tr>'
    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)
if __name__ == '__main__':
    main()