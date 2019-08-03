# -*- coding: utf-8 -*-
#批准的药包材
import time
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

    for i in range(1, 389):  # 遍历388个一级目录网页
        try:
            browser = webdriver.Chrome(chrome_options=option)
            url_1 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=6&State=1&bcId=152911879644285069080737494111&State=1&curstart='+str(i)+'&State=1&tableName=TABLE6&State=1&viewtitleName=COLUMN35&State=1&viewsubTitleName=COLUMN37,COLUMN36&State=1&tableView=%25E6%2589%25B9%25E5%2587%2586%25E7%259A%2584%25E8%258D%25AF%25E5%258C%2585%25E6%259D%2590&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1'
            browser.get(url_1)
            s = browser.page_source.replace('amp;', '')
            m = re.findall(r'content.jsp\?tableId=6&tableName=TABLE6&tableView=批准的药包材&Id=\d+', s, re.M)
            browser.close()

            for j in range(len(m)):
                url_2 = 'http://app1.sfda.gov.cn/datasearchcnda/face3/' + m[j]
                browser = webdriver.Chrome(chrome_options=option)
                browser.get(url_2)
                sql = "insert into t_pzdycb(c_bh, dt_insertTime, c_url, b_content,c_json, c_page) VALUES (REPLACE(UUID(),\"-\",\"\"), sysdate(), %s,%s,%s,%s)"
                mysql_db.exetcute_sql(sql, [url_2, browser.page_source,parse2json(browser.page_source),str(i)+'_'+str(j+1)])
                # pickle.loads(s) 可用该方法将乱码汉字转换
                browser.close()
        except Exception as e:
            print(e)
            time.sleep(5)


def parse2json(html):
    '''
    品种名称 pzmc
    注册证号 zczh
    企业名称 qymc
    产品来源 cply
    批准日期 pzrq
    规格 gg
    '''
    reg_dict = dict()
    result_json = dict()
    reg_dict['pzmc'] = r'品种名称</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['zczh'] = r'注册证号</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['qymc'] = r'企业名称</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['cply'] = r'产品来源</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['pzrq'] = r'批准日期</td>\s*<td.*>(.*)</td></tr>'
    reg_dict['gg'] = r'规格</td>\s*<td.*>(.*)</td></tr>'
    for i, v in reg_dict.items():
        reg_search = re.search(v, html)
        if reg_search is not None:
            result_json[i] = reg_search.group(1)
        else:
            result_json[i] = ''
    return json.dumps(result_json, ensure_ascii=False)
if __name__ == '__main__':
    main()