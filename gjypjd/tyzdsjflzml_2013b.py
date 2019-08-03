# -*- coding: utf-8 -*-
# 体外诊断试剂分类子目录（2013版）

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

    for i in range(1, 53):  # 遍历52个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=105&State=1&bcId=152904458543766919803166212682&State=1&curstart='+str(i)+'&State=1&tableName=TABLE105&State=1&viewtitleName=COLUMN1398&State=1&viewsubTitleName=COLUMN1397,COLUMN1396&State=1&tableView=%25E4%25BD%2593%25E5%25A4%2596%25E8%25AF%258A%25E6%2596%25AD%25E8%25AF%2595%25E5%2589%2582%25E5%2588%2586%25E7%25B1%25BB%25E5%25AD%2590%25E7%259B%25AE%25E5%25BD%2595%25EF%25BC%25882013%25E7%2589%2588%25EF%25BC%2589&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=105&tableName=TABLE105&tableView=体外诊断试剂分类子目录（2013版）&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_twzdsjflzml_2013(c_bh, dt_insertTime, c_url, b_content,c_json, c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source,parse2json(browser.page_source),str(i)+'_'+str(j+1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)


def parse2json(html):
    '''

    分类编码 flbm
    管理类别 gllb
    产品分类 cpfl
    产品分类名称 cpflmc
    预期用途 yqyt
    目录版本 mlbb

    '''
    reg_dict = dict()
    result_json = dict()
    reg_dict['flbm'] = r'分类编码</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['gllb'] = r'管理类别</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['cpfl'] = r'产品分类</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['cpflmc'] = r'产品分类名称</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['yqyt'] = r'预期用途</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['mlbb'] = r'目录版本</td>\s*<td.*>(.*)</td></tr>'

    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)
if __name__ == '__main__':
    main()