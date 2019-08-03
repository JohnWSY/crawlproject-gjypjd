# -*- coding: utf-8 -*-
# 国家基本药物（2018年版）


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

    for i in range(1, 47):  # 遍历46个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=138&State=1&bcId=152911951192978460689645865168&State=1&curstart='+str(i)+'&State=1&tableName=TABLE138&State=1&viewtitleName=COLUMN1879&State=1&viewsubTitleName=COLUMN1876,COLUMN1878,COLUMN1877&State=1&tableView=%25E5%259B%25BD%25E5%25AE%25B6%25E5%259F%25BA%25E6%259C%25AC%25E8%258D%25AF%25E7%2589%25A9%25EF%25BC%25882018%25E5%25B9%25B4%25E7%2589%2588%25EF%25BC%2589&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=138&tableName=TABLE138&tableView=国家基本药物（2018年版）&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_gjjbyw2018nb(c_bh, dt_insertTime, c_url, b_content,c_json, c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source,parse2json(browser.page_source),str(i)+'_'+str(j+1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)
def parse2json(html):
    '''
    一级目录  yjml
    二级目录  ejml
    三级目录  sjml
    备注      bz
    英文名    ywm
    剂型、规格 jxgg
    品种名称   pzmc
    注 z
    '''
    reg_dict=dict()
    result_json=dict()
    reg_dict['yjml']=r'一级目录</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['ejml'] = r'二级目录</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['sjml']=r'三级目录</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['bz']=r'备注</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['ywm'] = r'英文名</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['jxgg'] = r'规格</td>\s*<td.*>(.*\s*.*)</td></tr>'
    reg_dict['pzmc'] = r'品种名称</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['z'] = r'说\s*明</p><p>(.*)</p><p></p></span></td>'
    for i,v in reg_dict.items():
        reg_search=re.search(v,html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)


if __name__ == '__main__':
    main()