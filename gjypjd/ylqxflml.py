# -*- coding: utf-8 -*-
# 医疗器械分类目录

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

    for i in range(1, 110):  # 遍历109个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=139&State=1&bcId=154804104651613033739874139064&State=1&curstart='+str(i)+'&State=1&tableName=TABLE139&State=1&viewtitleName=COLUMN1884&State=1&viewsubTitleName=COLUMN1885&State=1&tableView=%25E5%258C%25BB%25E7%2596%2597%25E5%2599%25A8%25E6%25A2%25B0%25E5%2588%2586%25E7%25B1%25BB%25E7%259B%25AE%25E5%25BD%2595&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=139&tableName=TABLE139&tableView=医疗器械分类目录&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_ylqxflml(c_bh, dt_insertTime, c_url, b_content,c_json, c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source,parse2json(browser.page_source),str(i)+'_'+str(j+1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)
def parse2json(html):
    '''
    一级类别yjlb
    二级类别ejlb
    产品描述cpms
    预期用途yqyt
    品名举例pmjl
    管理类别gllb
    产品类别cplb
    注z

    '''
    reg_dict = dict()
    result_json = dict()
    reg_dict['yjlb'] = r'一级类别</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['ejlb'] = r'二级类别</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['cpms'] = r'产品描述</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['yqyt'] = r'预期用途</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['pmjl'] = r'品名举例</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['jyyj'] = r'管理类别</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['cplb'] = r'产品类别</td>\s*<td.*>(.*)</td></tr>'
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